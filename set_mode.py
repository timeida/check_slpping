import cv2
import numpy as np
#----------start here-----------
def is_night_mode(frame):  #야간환경인지 아닌지 
    # 프레임의 밝기 평균 계산
    average_brightness = cv2.mean(frame)[0]
    
    # 야간 모드로 판단할 임계값 설정 (계속 실험해보고 바꿔)
    threshold_brightness = 100
    
    return average_brightness < threshold_brightness #(임계값보다 작으면 야간모드로    0이면 주간 1이면 야간)


def set_night_mode(capture):


    # 노출시간, iso 야간환경에 맞게 조절  
    # 웹캠마다 지원이 안되는 경우가 있어 주석 처리 하겠습니다.
    
    capture.set(cv2.CAP_PROP_EXPOSURE, 0.000005) #노출값 길게 빛 많이 받도록
    capture.set(cv2.CAP_PROP_ISO_SPEED, 800) #iso조절

     
    # capture.set(cv2.CAP_PROP_AUTO_EXPOSURE,1)
    print("야간모드 필터로 전환합니다.")


    return True
    
def reset_camera_settings(capture):
    # 자동 노출 다시 활성화
    capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    return False
#---------------end here---------------

