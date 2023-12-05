import cv2

def is_night_mode(frame):
    # 프레임의 밝기 평균 계산
    average_brightness = cv2.mean(frame)[0]
    
    # 야간 모드로 판단할 임계값 설정 (계속 실험해보고 바꿔)
    threshold_brightness = 100
    
    return average_brightness < threshold_brightness #(임계값보다 작으면 야간모드로    0이면 주간 1이면 야간)
