import time
import cv2
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

def eye_aspect_ratio(eye): # 눈을 어느정도 감고 있는지 받아주는 함수, 종횡비 계산
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    EAR = (A + B) / (2.0 * C)
    return EAR

def mouth_open_ratio(mouth): ## (진우)입을 어느 정도 벌렸는지 받아주는 함수, 가로 길이와 세로 길이를 계산해서 세로/가로의 값을 받음(진우)
    
    # 입의 가로 길이와 세로 길이 계산
    mouth_width = dist.euclidean(mouth[0], mouth[-1]) #입의 왼쪽 끝과 입술 중간
    mouth_height =(dist.euclidean(mouth[2], mouth[-3]) +
                    dist.euclidean(mouth[4], mouth[-5])) / 2.0
    # (입술의 왼쪽 제일 높은 곳과 입술 왼쪽의 중간사이 길이), (입술의 오른쪽 제일 높은 곳과 입술 오른쪽의 중간사이 길이)의 평균

    mouth_ratio = mouth_height / mouth_width # 입의 세로/가로 값
    return mouth_ratio


def eye_is_close(ear, eye_blink_counter, Sleep_Start, eye_blink_total,WarningSound,frame):
    EYE_AR_THRESH = 0.2 # 원하는 눈 감기 정도에 조절
    EYE_AR_CONSEC_FRAMES = 3
    #눈이 감겼는지 확인하고, 감겼으면 감긴 시간 체크하고, 감긴횟수 최신화함
    if ear < EYE_AR_THRESH: #눈의 종횡비함수가 임계값보다 작으면(감기면)
        Sleep_Start += 1 
        eye_blink_counter += 1 

        if Sleep_Start > 10: #75프레임 이상 눈감고 있으면
            print("졸음운전 감지 -- 운전자 눈 감고있음 by Dlib")
            cv2.putText(frame, "Wake up!!!", (300, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            WarningSound.play(loops=1)

            # log.info("Sleep Time : " + str(Sleep_Start))
            Sleep_Start = 0 # 눈 감는 누적시간 초기화함

    else:
        Sleep_Start = 0
        if eye_blink_counter >= EYE_AR_CONSEC_FRAMES:
            eye_blink_total += 1 #감은 횟수 증가

        eye_blink_counter = 0 # 초기화

    return eye_blink_total, eye_blink_counter, Sleep_Start

def mouth_is_close(mouth_ratio, mouth_open_counter, Open_Start, mouth_open_total,WarningSound,frame,mouth_at_tresh):
    
    # mouth_at_tresh 입 벌린 정도 야간=(주간)*0.7
    
    MOUTH_AR_CONSEC_FRAMES = 3 #프레임 임계값(진우)
    #(진우), 하품하는지 확인하고, 하품하면 하품하는 시간 체크하고, 하품횟수 최신화함
    if mouth_ratio > mouth_at_tresh:
        Open_Start += 1
        mouth_open_counter += 1
        # print(Open_Start)
        cv2.putText(frame, str(Open_Start), (300, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        if Open_Start > 10: #값은 나중에 조절하자
            
            WarningSound.play(loops=1)
            if WarningSound.play(loops=1):
                print("졸음 경고 : 하품 기준치 이상 by Dlib")
                
            # log.info("Open Time : " + str(Open_Start))
            Open_Start = 0

    else:
        Open_Start = 0
        if mouth_open_counter >= MOUTH_AR_CONSEC_FRAMES:
            mouth_open_total += 1

        mouth_open_counter = 0
    # print(Open_Start)

    return mouth_open_total, mouth_open_counter, Open_Start
