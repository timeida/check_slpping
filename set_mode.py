import cv2
import numpy as np
def set_night_mode(capture):


    # # Set a moderate exposure time
    # capture.set(prop_exposure, 0.000001) 카메라 노출값 증가

    capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    print("야간모드 필터로 전환합니다.")

    return True
    
def reset_camera_settings(capture):
    # 자동 노출을 다시 활성화
    capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    return False
