# 1. 설명
- faster whisper를 통해 STT를 구현하고, VAD 기술을 추가하여 Speech to Text 프로그램을 구현하였습니다.  
- 녹음 시작(START) 버튼을 누르면 녹음이 시작되고, 4초간의 고정된 녹음 이후 VAD로 발화 종료를 자동으로 감지하여 녹음이 종료됩니다.  
- faster whisper가 해당 녹음 파일을 통해 text로 변환하여 프로그램에 출력합니다.  

# 2. 환경설정
Ubuntu 22.04에서 개발되었습니다.
### 2.0 레퍼지토리 클론
```bash
git clone https://github.com/SHIN-DONG-UK/stt_and_vad.git
cd stt_and_vad
```

### 2.1. 파이썬 가상환경

- 파이썬 3.10  버전(우분투 기본)으로 가상환경 만들려면 python3.10-venv 깔아야 함

```bash
sudo apt install python3.10-venv
```

- 가상환경 만들기

```bash
python3.10 -m venv [가상환경이름]
```

- 가상환경 실행

```bash
source [가상환경이름]/bin/activate
```

### 2.2 webrtcvad 설치

```bash
pip install webrtcvad
```

- VAD 관련

### 2.3 pyaudio 설치

```bash
pip install pyaudio
```

- 녹음 관련

### 2.4 PyQt5 설치

```bash
pip install PyQt5 PyQt5-tools PyQt5-sip PyQt5-Qt5
```

- gui

### 2.5 faster-whisper 설치

```bash
pip install faster-whisper
```

- STT

### 2.6 cuBLAS, cuDNN

```bash
pip install nvidia-cublas-cu12 nvidia-cudnn-cu12==9.*

export LD_LIBRARY_PATH=`python3 -c 'import os; import nvidia.cublas.lib; import nvidia.cudnn.lib; print(os.path.dirname(nvidia.cublas.lib.__file__) + ":" + os.path.dirname(nvidia.cudnn.lib.__file__))'`
```

# 3. 프로그램 실행 방법
```bash
python stt_and_vad_gui.py
```
![image](https://github.com/user-attachments/assets/9edc47c7-778c-495d-b85b-76cf43f44a88)
