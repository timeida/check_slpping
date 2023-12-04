# check_slpping
#### 파이썬을 활용한 졸음감지 프로그램

Index
---
* 개요
* 개발 환경 설정
* System Diagram
* 눈 및 입 영역 추출
* 졸음 측정
* 참고자료

개요
---
실시간 영상 처리 기술을 활용하여 운전자의 졸음 여부를 판별하고 졸음운전 중이라면 시각, 음성 경고가 울리게 하는 프로그램을 제작하였습니다. opencv와 dlib라이브러리를 활용하여 영상처리를 하였고, 야간과 주간상황에 적합한 카메라 모드를 적용하여 더욱 안정적으로 작동하게 구현하였습니다.


개발 환경 설정
---
Ubuntu 20.04버전에서 작동하였으며 python3를 이용하였습니다. 다음과 같은 라이브러리가 사용됐습니다. 위에서 아래로 순차적으로 설치해야 합니다.
>sudo apt update
>
>sudo apt-get install python3-pip
>
>pip install --upgrade pip
* numpy
  >sudo pip3 install numpy
* pygame
  > pip3 install pygame
* cv2
  >sudo apt install libopencv-dev python3-opencv
* argparse
  >sudo apt-get install -y python-argparse
* imutils
  >pip3 install imutils
* pwn
  >pip3 install pwntools
* cmake
  >sudo apt-get install cmake
* boost
  >sudo apt-get install libboost-all-dev
* dlib
  >pip3 install dlib

System Diagram
---
### Block Diagram
<img src="https://github.com/timeida/check_slpping/assets/78420869/a86f6f5b-f2f8-4d86-8ffc-5fd577502316"  width="500" height="400">

### Class Diagram
<img src="https://github.com/timeida/python/assets/78420869/e5cab70b-eb83-41a9-95da-5b8b104eb840"  width="800" height="200">

### Sequence Diagram
<img src="https://github.com/timeida/python/assets/78420869/8a8c8a3b-d133-4cec-bac4-a3e809487131"  width="400" height="200">


눈 및 입 영역 추출
---
오픈소스 dlib와 cv2를 이용하여 얼굴의 특징점을 만들었습니다. dlib의 얼굴 검출기는 높은 정확도를 제공하며, 다양한 각도와 크기의 얼굴을 원활히 검출할 수 있습니다. 

__1. 얼굴 검출__

얼굴의 전체 영역을 68개의 점을 표시해 눈, 입에 face landmark을 찍습니다.

__3. 눈 검출__

검출된 얼굴 영역에서 눈을 검출합니다. 눈은 각각 37 ~ 42 / 43 ~ 48번입니다.

__4. 입 검출__

검출된 얼굴 영역에서 눈을 검출합니다. 입은 49 ~ 67의 점으로 표시합니다.

__5. 눈 상태 분류__

눈 영역에서 눈이 열려 있는지 닫혀 있는지를 분류하는 모델을 사용합니다. 머신 러닝 기술을 활용하여 훈련된 모델을 사용하였습니다.

<img src="https://github.com/timeida/python/assets/78420869/ba7a4321-10b5-43f5-aa84-b17c29509f75"  width="600" height="500">



졸음 측정
---
두 눈과 입사이에 표시된 face landmark사이에 길이를 측정하여 운전자의 상태를 감지합니다.

<img src="https://github.com/timeida/python/assets/78420869/d1d24c2e-df97-4b2e-b33c-004a5469d06f"  width="200" height="100">

<img src="https://github.com/timeida/python/assets/78420869/3236a3ea-a6e7-47cf-b62e-4b2a09df522d"  width="200" height="100">

<img src="https://github.com/timeida/python/assets/78420869/eaf92431-6047-49f2-a10a-34078bd2f358"  width="200" height="100">

<img src="https://github.com/timeida/python/assets/78420869/fb6e9b14-05fd-4362-9961-17bc2399009a"  width="200" height="100">


참고자료
---
Detect Drowsy_Driver

http://www.nefus.kr/2021_Demonstration/Drowsy_Driver/index.html

https://github.com/NEFUS18/Dont_Drowsy_Drive
