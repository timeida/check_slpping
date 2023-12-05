# check_slpping
#### 파이썬을 활용한 졸음감지 프로그램



Index
---
* 개요
* 개발 환경 설정
* System Diagram
* 눈 및 입 영역 추출
* 졸음 측정
* 주간야간 모드
* 참고자료



개요
---
실시간 영상 처리 기술을 활용하여 운전자의 졸음 여부를 판별하고 졸음운전 중이라면 시각, 음성 경고가 울리게 하는 프로그램을 제작하였습니다. opencv와 dlib라이브러리를 활용하여 영상처리를 하였고, 야간과 주간상황에 적합한 카메라 모드를 적용하여 더욱 안정적으로 작동하게 구현하였습니다.



개발 환경 설정
---
Ubuntu 20.04버전에서 작동하였으며 python3를 이용하였습니다. 다음과 같은 라이브러리가 사용됐습니다. 위에서 아래로 순차적으로 설치해야 합니다.
>sudo apt-get update
>
>sudo apt-get upgrade
>
>sudo apt-get install python3-pip
>
>pip install --upgrade pip
* numpy
  >sudo pip3 install numpy
* pygame
  > pip3 install pygame
*scipy
  > pip3 install scipy
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
  >
  >wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2 # DOWNLOAD LINK
  >
  >다운로드한 shape_predictor_68_face_landmarks.dat.bz2을 Extract합니다.(만약 Extract가 안될시 [7-zip]설치후 Extract)
  >
  >Extract한 shape_predictor_68_face_landmarks.dat파일을 main.py파일이 있는 장소로 복사합니다.
* opencv
  >[here]로 이동해서 opencv를 설치 합니다.
  >
  >22, 23라인의 xml파일들의 경로를 설치된 위치로 지정합니다.



System Diagram
---
### Block Diagram
<img src="https://github.com/timeida/check_slpping/assets/78420869/a86f6f5b-f2f8-4d86-8ffc-5fd577502316"  width="500" height="400">

### Class Diagram
<img src="https://github.com/timeida/check_slpping/assets/78420869/1b3d8e72-021d-4caf-acaa-ab6abaa4c07a"  width="800" height="200">

### Sequence Diagram
<img src="https://github.com/timeida/check_slpping/assets/78420869/130204e8-c7a4-42a6-9932-325f23b6718a"  width="400" height="200">


눈 및 입 영역 추출
---
오픈소스 dlib와 cv2를 이용하여 얼굴의 특징점을 만들었습니다. dlib의 얼굴 검출기는 높은 정확도를 제공하며, 다양한 각도와 크기의 얼굴을 원활히 검출할 수 있습니다. 

__1. 얼굴 검출__

얼굴의 전체 영역을 68개의 점을 표시해 눈, 입에 face landmark을 찍습니다.

__3. 눈 검출__

검출된 얼굴 영역에서 눈을 검출합니다. 눈은 각각 37 ~ 42 / 43 ~ 48번입니다.

__4. 입 검출__

검출된 얼굴 영역에서 눈을 검출합니다. 입은 49 ~ 67의 점으로 표시합니다.

[5. 눈 상태 분류]

눈 영역에서 눈이 열려 있는지 닫혀 있는지 눈의 종횡비를 계산하여 함수를 깃허브에서 참고하여 사용하였다.눈을 감게 되면 눈의 세로 비율이 작아지고, EAR 비율 역시 작아진다. 사람이 깜박이면 눈의 종횡비가 급격히 감소하여 0에 가까워진다. 이처럼 사람이 졸리면 눈을 감거나 눈을 조그마하게 뜨는 행동을 하게 되므로 EAR값의 임계치를 설정하면,이를 이용하여 눈 감김 여부를 판단할 수 있다. Frame을 계속 돌리면서 EAR 비율을 계산하고, 이 비율이 특정 비율 보다 작아지면 그 frame을 계속 카운트하여 저장한다. 그러다가, 일정 카운트 값 이상이 되면, 즉, 일정 시간 이상 눈이 감겨있다고 인식되면 알람을 통해 운전자에게 경고를 준다.
<img src="https://github.com/timeida/check_slpping/assets/78420869/c2e69d08-e545-40d0-8cfb-004bdd3eb980"  width="606" height="500">
<img src="https://github.com/timeida/check_slpping/assets/78420869/1e45f6ac-eded-4560-9b99-a52683905294"  width="606" height="168">

__6.입 상태 분류__

입 영역에서 입이 열려있는지 닫혀있는지를 판단하는 알고리즘을 눈이 닫혀있는지 열려있는지 판단하는 알고리즘과 유사하게 직접 설계하였다. 입의 왼쪽 끝 지점과 입술 정중앙 지점까지의 길이(2)와 입술 오른쪽 제일 높은 곳과 입술 오른쪽 중간 사이의 길이(3)에서 길이(2)와 길이(3)의 평균을 세로로 지정한다. 이후 세로/가로의 비를 계산하는데, 입을 벌리게 되면 입의 가로길이에 대한 세로 길이의 비가 더 커지게 된다. 이 세로/가로 값이 일정시간 커지면 입이 열려있다고 판단한다. 5번과 비슷하게,  frame을 계속 돌리면서 mouth_ratio 비율을 계산하고, 이 비율이 특정 비율 보다 커지면 그 frame을 계속 카운트하여 저장한다. 그러다가, 일정 카운트 값 이하가 되면, 즉, 일정 시간 이상 입이 열려 있어 운전자가 하품을 한다고 인식되면 알람을 통해 운전자에게 경고를 준다.

<img src="https://github.com/timeida/check_slpping/assets/78420869/98ea67f0-ef59-4b31-a004-afa81b9975a7"  width="600" height="500">



졸음 측정
---
두 눈과 입사이에 표시된 face landmark사이에 길이를 측정하여 운전자의 상태를 감지합니다.

<img src="https://github.com/timeida/python/assets/78420869/d1d24c2e-df97-4b2e-b33c-004a5469d06f"  width="200" height="100">
<img src="https://github.com/timeida/python/assets/78420869/3236a3ea-a6e7-47cf-b62e-4b2a09df522d"  width="200" height="100">
<img src="https://github.com/timeida/python/assets/78420869/eaf92431-6047-49f2-a10a-34078bd2f358"  width="200" height="100">
<img src="https://github.com/timeida/python/assets/78420869/fb6e9b14-05fd-4362-9961-17bc2399009a"  width="200" height="100">



주간야간 모드
---
야간모드는 웹캠 프레임의 밝기의 평균이 기준치 이하로 떨어졌을 시 작동하도록 만들었다. 빛이 적은 야간모드 시에는 카메라의 노출시간을 증가시켜 더 많은 빛을 받아와 저조도 환경에서도 운전자의 얼굴을 인식할 수 있게 만들었다. 그러나 노출시간을 증가시킨 만큼 프레임이 바뀌는데 걸리는 시간이 증가하였다. 따라서 하품 인식 프레임 수를 주간은 15, 야간은 5로 설정하여 보정하였다.  그리고 야간모드에는 눈을 감는 시간을 인식하는 방법을 프레임에서 시간으로 변동한다.  야간모드는 노출시간의 문제로 버벅일 수 밖에 없음으로 심한 저조도 환경이 아닌 이상 작동하지 않도록 설정하였다. 그리고 만약 노출시간 조정을 지원하지 않는 웹캠이라면 set_mode.py 20, 21 line을 주석처리하고 24 line 을 주석 해제하면 noise 를 줄여주는 median filter만 적용된 채 작동하게 된다. 

<img src="https://github.com/timeida/check_slpping/assets/78420869/7ed499da-3918-4d19-995d-1d2dcb951398"  width="400" height="400">
<img src="https://github.com/timeida/check_slpping/assets/78420869/e84c13ba-be82-487a-b1ac-fd47f3a9db38"  width="400" height="400">


### 주간모드 졸음인식 방법
주간모드에서 운전자 졸음을 인식하는 방법은 눈이 일정시간 이상 감겨있거나 하품을 일정시간 이상 하게 되면 졸음 위험이 있다고 판단하여 경고음을 출력한다. 이때 눈의 감고 뜸 여부를 인식하는 방법은 dlib를 사용해 눈이 감긴 정도를 판단해,만약 임계치 이하로 운전자의 눈이 감긴다면 그 프레임부터 연속적으로 10 프레임동안 눈이 감겨있다면 졸음 위험이라 판단해 알람이 울리게 된다. 그리고 하품은 마찬가지로 입이 임계치 이상으로 벌려져 있는 프레임을 시작으로 연속적으로 15프레임 이상 입이 벌려져 있다면 졸음 위험이라고 판단해 알람이 울린다.

<img src="https://github.com/timeida/check_slpping/assets/78420869/47b934c4-c0f0-4c90-99d5-824442b11dc1"  width="500" height="400">

### 야간모드 졸음인식 방법
야간모드에서는 주간모드와 동일한 요소를 판단하지만 방식이 조금 다르다. 앞서 말했던 것처럼 야간모드에서는 노출시간이 길어져 영상에서 다음 프레임으로 넘어가는 시간이 길어지므로 하품 인식 프레임을 기존 15에서 5로 낮추었다. 그리고 눈이 감긴 정도를 기존 프레임 단위에서 시간 단위로 변동한다. 그리고 눈을 인식하는 방법을 dlib에서 open cv haarcascade_eye로 변동하였다. 사진에서 보이는 것 처럼 눈부분이 초록색(dlib)에서 붉은색(haarcascade_eye.xml)으로 바뀐다. 

<img src="https://github.com/timeida/check_slpping/assets/78420869/157147ac-ab7c-4e65-bd41-a36effa0ce12"  width="500" height="400">


참고자료
---
[7-zip]: https://www.7-zip.org/download.html
[here]: https://velog.io/@minukiki/Ubuntu-20.04%EC%97%90-OpenCV-4.4.0-%EC%84%A4%EC%B9%98
[5. 눈 상태 분류]: https://ultrakid.tistory.com/12

Detect Drowsy_Driver

http://www.nefus.kr/2021_Demonstration/Drowsy_Driver/index.html

https://github.com/NEFUS18/Dont_Drowsy_Drive
