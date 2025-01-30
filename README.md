# 1. 설명

# 2. 환경설정

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