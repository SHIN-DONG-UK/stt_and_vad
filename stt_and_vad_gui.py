# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import pyaudio
import wave
import webrtcvad
import time
from faster_whisper import WhisperModel

class RecorderThread(QtCore.QThread):
    data_recorded = QtCore.pyqtSignal(bytes)  # 녹음된 데이터를 전달하는 시그널

    def __init__(self, chunk, format, channels, rate, parent=None):
        super().__init__(parent)
        self.chunk = chunk
        self.format = format
        self.channels = channels
        self.rate = rate
        self.running = False
        self.frames = []

    def run(self):
        # PyAudio 초기화
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.format,
                                  channels=self.channels,
                                  rate=self.rate,
                                  input=True,
                                  frames_per_buffer=self.chunk)

        self.frames = []
        self.running = True
        while self.running:
            data = self.stream.read(self.chunk)
            self.frames.append(data)
            self.data_recorded.emit(data)  # 데이터가 녹음될 때마다 시그널로 전달

        # 스트림 종료
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def stop(self):
        self.running = False

    def save_audio(self, filename="./output/output.wav"):
        # 녹음된 데이터를 파일로 저장
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()


class Ui_Dialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        # STT
        self.model_size = "large-v2"
        # Run on GPU with FP16
        self.model = WhisperModel(self.model_size, device="cuda", compute_type="int8")

        # VAD 설정
        self.vad = webrtcvad.Vad()
        self.vad.set_mode(1)  
        self.speeching = True

        # timer 설정
        self.start_time = None

        # PyAudio 설정
        self.CHUNK = 320                # 20ms
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000

        self.recorder = None  # RecorderThread 초기화

        # log 색상 관련
        self.color_map = {
            "INFO": "black",
            "SYSTEM": "red",
            "OUTPUT": "blue",
        }

        # UI 설정
        self.setWindowTitle("Voice Recorder with STT")
        self.resize(600, 500)  # 창 크기 설정

        # 레이아웃 설정 (반응형 적용)
        self.layout = QtWidgets.QVBoxLayout(self)

        # Start 버튼 추가
        self.start_btn = QtWidgets.QPushButton("Start")
        self.start_btn.setObjectName("start_btn")

        # QTextBrowser (반응형 설정)
        self.textBrowser = QtWidgets.QTextBrowser()
        self.textBrowser.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # 위젯 추가
        self.layout.addWidget(self.start_btn)
        self.layout.addWidget(self.textBrowser)

        # 버튼 클릭 이벤트 연결
        self.start_btn.clicked.connect(self.start_button_click)

    def add_log(self, level, message):
        """로그를 QTextBrowser에 추가 (HTML 색상 적용)"""
        current_time = QtCore.QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        color = self.color_map.get(level, "black")

        log_text = f'<span style="color: gray;">[{current_time}]</span> ' \
                   f'<span style="color: {color};">[{level}]</span> ' \
                   f'<span>{message}</span>'

        self.textBrowser.append(log_text)

    def start_button_click(self):
        """녹음 시작"""
        if not self.recorder or not self.recorder.isRunning():
            self.add_log("INFO", "Start recording...")
            self.recorder = RecorderThread(self.CHUNK, self.FORMAT, self.CHANNELS, self.RATE)
            self.recorder.data_recorded.connect(self.on_data_recorded)
            self.recorder.start()
            self.start_time = time.time()

    # 20ms 마다 호출 
    def on_data_recorded(self, data):
        """음성 데이터를 받아서 처리"""
        if self.recorder:  # 녹음이 진행 중인지 확인
            now = time.time()
            self.add_log("SYSTEM", f"Elapsed time : {(now - self.start_time):.3f}")

            if now - self.start_time >= 4:
                self.speeching = self.vad.is_speech(data, self.RATE)
                if not self.speeching:
                    self.recorder.stop()
                    self.recorder.wait()  # 스레드 종료 대기
                    self.recorder.save_audio()
                    self.add_log("INFO", "Recording stopped. Converting the saved audio to text...")
                    self.recorder = None
                    self.stt()

    def stt(self):
        """음성을 텍스트로 변환"""
        start_time = time.time()
        segments, info = self.model.transcribe("./output/output.wav", beam_size=5, language='ko')
        end_time = time.time()
        #self.add_log("OUTPUT", "Detected language '%s' with probability %.2f" % (info.language, info.language_probability))

        for segment in segments:
            self.add_log("OUTPUT", "[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

        self.add_log("OUTPUT", "걸린 시간 : %.2fs" % (end_time - start_time))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = Ui_Dialog()
    Dialog.show()
    sys.exit(app.exec_())
