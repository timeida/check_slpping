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
Ubuntu 20.04버전에서 작동하였으며 다음과 같은 라이브러리가 사용됐습니다. 위에서 아래로 순차적으로 설치해야 합니다.
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

눈 및 입 영역 추출
---
오픈소스 dlib와 cv2를 이용하여 얼굴의 특징점을 만들고, 얼굴의 전체 영역을 68개의 점을 표시해 눈, 입에 face landmark을 찍습니다.
눈은 각각 37 ~ 42 / 43 ~ 48, 입은 49 ~ 67의 점으로 표시합니다.
![1701576859561](https://github.com/timeida/check_slpping/assets/78420869/33f9d463-f569-4a75-b1b2-e75bf35007d5)


졸음 측정
---
눈이 감고 또는 실눈을 뜬채로 일정 시간이 지나면 잠을 깨우는 경고 알람과 문구가 출력이 되도록 하였습니다. 피로를 감지하기 위해 하품을 하는 상황을 고려해 일정 시간만큼 크게 입을 벌린상태로 일정 시간이 경과하면 경고 알람이 울리게 설계하였습니다.




참고자료
---

