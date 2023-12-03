check_slpping
파이썬을 활용한 졸음감지 프로그램

Index
---
* 개요
* 개발 환경 설정
* S/W
* 눈 및 입 영역 추출
* 졸음 측정
* 참고자료

개요
---
실시간 영상 처리 기술을 활용하여 운전자의 졸음 여부를 판펼하고 졸음운전 중이라면 시각 신호와 음성 신호의 경고가 울리게 하는 프로그램을 제작하였습니다. opencv와 dlib라이브러리를 활용하여 영상처리를 하였고, 야간과 주간상황에 적합한 카메라 모드를 적용하여 더욱 안정적으로 작동하게 구현하였습니다.

개발 환경 설정
---
Ubuntu 20.04버전에서 작동하였으며 다음과 같은 라이브러리가 사용됐습니다.
>sudo apt update
>
>sudo apt install python-pip

* cv2
  >sudo apt install libopencv-dev python3-opencv
* argparse
  >sudo apt-get install -y python-argparse
* dlib
* cmake
* imutils
* numpy
  >sudo apt install numpy
* pygame
  > 
  >
  > pip install pygame
* pwn

눈 및 입 영역 추출
---
오픈소스 dlib와 cv2를 이용하여 얼굴의 특징점을 만들고, 얼굴의 전체 영역을 68개의 점을 표시해 눈, 입에 face landmark을 찍는다.
눈은 각각 37 ~ 42 / 43 ~ 48, 입은 49 ~ 67
![1701576859561](https://github.com/timeida/check_slpping/assets/78420869/33f9d463-f569-4a75-b1b2-e75bf35007d5)



졸음 측정
---
눈이 감기고 일정 시간이 지나도 눈을 뜨지안았을때 잠을 깨우는 경고 알람과 문구가 출력이 되도록 하였습니다. 또한 하품을 하는 상황을 고려해 일정 시간만큼 크게 입을 벌리면 경고 알람이 울리게 설계하였습니다.




참고자료
---

