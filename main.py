from eye_mouth_check import eye_aspect_ratio, eye_is_close, mouth_is_close, mouth_open_ratio
from set_mode import set_night_mode,reset_camera_settings,is_night_mode   

import cv2
import time
import argparse
import dlib
import imutils
import numpy as np 
import timeit
import pygame

from pwn import *
from imutils import face_utils
# from imutils.video import FileVideoStream, VideoStream
from scipy.spatial import distance as dist

def main():
    # 얼굴, 눈 cascade 검출기 객체 선언
    face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('./haarcascade_eye.xml')
    face_detected = False
    # 루프 50번 돌때마다 모드 체크
    check_night_mode_counter = 49
    night_mode_check_interval = 50
    start = 0
 
    # 시간 측정을 위한 변수
    start_time = time.time()
    start_time2 = time.time()
    #눈 깜빡임 , 입 벌림 횟수
    eye_blink_total= 0
    mouth_open_total= 0

    pygame.mixer.init()
    WarningSound = pygame.mixer.Sound("Original_Beep.wav") #알람 소리
    
    (lstart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    (mstart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--shape-predictor", default="./shape_predictor_68_face_landmarks.dat", help="path to facial landmark predictor")
    args = vars(ap.parse_args())
    ap.add_argument("-v", "--video", type=str, default="./ddd.mp4", help="path to input video file")
    args = vars(ap.parse_args())

    print("[INFO] 얼굴 인식기 로딩중...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(args["shape_predictor"])

    print("[INFO] 카메라 정보 로딩 중...")

    capture = cv2.VideoCapture(0,cv2.CAP_V4L2)


    eye_blink_counter = 0
    mouth_open_counter = 0
    Sleep_Start = 0
    Open_Start = 0
#---------------------------------start here----------------------------------
    while True:
        #ret 성공적으로 읽어온지 여부 , frame 현재 읽은 프레임이 저장된 변수. 이 변수에는 이미지 데이터가 포함되어 있다.
        
        ret, frame = capture.read()  
        
        if ret: #영상 성공적으로 읽음
            
            check_night_mode_counter += 1
            # if check_night_mode_counter%10 == 0:  #10번 돌아갈때마다 카운터 출력
            #     print(check_night_mode_counter
            
            if check_night_mode_counter == night_mode_check_interval: #루프 50번 돌때마다 모드 체크해서 낮,밤 확인
                if is_night_mode(frame):
                    set_night_mode(capture)
                    print("야간모드입니다.")
                    mode = 1
                else:
                    reset_camera_settings(capture)
                    print("주간모드입니다.")
                    mode = 0

                check_night_mode_counter = 0  

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=3, minSize=(20, 20))
        eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=3, minSize=(10, 10))
        #---------------주간모드 코드---------------
        if not(mode):  
            # print("주간모드일때 출력되야해")
            if len(faces):
                for x, y, w, h in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2, cv2.LINE_4)
                    
                    if not face_detected:  # face_detected가 False일 때만 출력
                        start = 1
                        print("운전자 탑승: 졸음운전 감지를 시작합니다.")
                        face_detected = True  # 얼굴이 감지되었음을 표시
#-----------------------------------end here----------------------------------    

            if ret is None: #웹캠 꺼지거나 비디오 꺼지면 종료
                break
            frame = imutils.resize(frame, width=800)
            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            rects = detector(gray, 0)
            #루프 시작
            for rect in rects:
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)

                leftEye = shape[lstart:lEnd]
                rightEye = shape[rStart:rEnd]
                mouth = shape[mstart:mEnd]

                leftEAR = eye_aspect_ratio(leftEye)
                rightEAR = eye_aspect_ratio(rightEye)

                ear = (leftEAR + rightEAR) / 2.0 # 양쪽 눈 종횡비 평균 계산
                mouth_ratio = mouth_open_ratio(mouth)

                #컨벡스헐 만드는 부분
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                mouthHull = cv2.convexHull(mouth)

                cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
                cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
                cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)

                eye_blink_total, eye_blink_counter, Sleep_Start = eye_is_close(ear, eye_blink_counter,Sleep_Start,eye_blink_total,WarningSound,frame)
       
                    
                mouth_open_total, mouth_open_counter, Open_Start = mouth_is_close(mouth_ratio, mouth_open_counter,Open_Start,mouth_open_total,WarningSound,frame,1.0,15)
                
                #위 함수 2개, 눈 감은지, 하품하는지 판단하고, 카운트해줌, 값들 계속 루프돌면서 업데이트함
                cv2.putText(frame, "EAR : " + str(ear), (300, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, "MOUTH_RATIO : " + str(mouth_ratio), (300, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
               

            cv2.imshow("Driver", frame)

            key = cv2.waitKey(1)

            if cv2.waitKey(1) == ord('q'):
                print("운전 종료. 프로그램을 종료합니다.")
                break
        #---------------야간 모드 코드---------------
        
        else:       
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=3, minSize=(20, 20))
            eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=3, minSize=(10, 10))
    #----------------------start here------------------------  
            if not(is_night_mode(frame)):
                if len(faces):
                    for x, y, w, h in faces:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2, cv2.LINE_4)
                        
                    if not face_detected:  # face_detected가 False일 때만 출력
                        start = 1
                        print("운전자 탑승: 졸음운전 감지를 시작합니다.")
                        face_detected = True  # 얼굴이 감지되었음을 표시
                        
            if len(eyes):
                for x, y, w, h in eyes:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2, cv2.LINE_4)    
     
                    start_time = time.time()  # 눈이 감지되면 시간을 초기화
                    
          
            if start == 1:#운전자 탑승 확인 되면 졸음 여부 판단 시작
                elapsed_time = time.time() - start_time  #눈이 4초간 감지 안된다면
                if elapsed_time > 2.5:
                    WarningSound.play(loops=1)

                    print("운전자 졸음 감지: 운전자 눈 감고있음.")
     #----------------------end here------------------------  
        
            frame = imutils.resize(frame, width=800)
            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            
            
            rects = detector(gray, 0)
            #루프 시작
            for rect in rects:
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)
                
                mouth = shape[mstart:mEnd]

                mouth_ratio = mouth_open_ratio(mouth)

                #컨벡스헐 만드는 부분
                mouthHull = cv2.convexHull(mouth)
                
                cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)
                                    
                mouth_open_total, mouth_open_counter, Open_Start = mouth_is_close(mouth_ratio, mouth_open_counter,Open_Start,mouth_open_total,WarningSound,frame,0.9,4)
                
                #위 함수 2개 눈 감는지, 하품하는지 판단하고, 카운트해줌, 값들 계속 루프돌면서 업데이트함
                
                cv2.putText(frame, "MOUTH_RATIO: " + str(mouth_ratio), (300, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
               
              
                
            frame = cv2.medianBlur(frame,5) 
            cv2.imshow("Driver",frame)

            key = cv2.waitKey(1)

        if cv2.waitKey(1) == ord('q'):
            print("운전 종료. 프로그램을 종료합니다.")
            break
     
                           
 
    capture.release()
    cv2.destroyAllWindows()


main()