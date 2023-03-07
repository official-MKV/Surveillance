import torch
import cv2 as cv
import datetime
from playsound import playsound
from time import time
from datetime import datetime
from functions import draw_box
import socket
import cv2
import pickle
import asyncio
import struct



# Set Surveillance parameters
#----------------------------------------------------------------------
time_limit = datetime.strptime('11::07::00', '%H::%M::%S').time()
alarm_time_wait = 60
alarm_timer = 0
stream = True
command_active = True
connected = False
check_weapon_locally = False
#-------------------------------------------------------------------------



detect_person_model_path =r'C:\Users\user\Dev\AISurveillance\yolov5\yolov5n_openvino_model'
model = torch.hub.load('ultralytics/yolov5', 'custom', path=detect_person_model_path) # PyTorch
model.cpu()
model.classes = [0] #find only persons
capture = cv.VideoCapture(0)
while capture.isOpened():
    _,frame = capture.read()
    HEIGHT,WIDTH,_ = frame.shape
    img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    img_resized = cv.resize(img,(640,640))
    results = model(img_resized)
    output = draw_box(img_resized,results.pandas().xyxy[0],[255,0,255])
    if len(results)!=0:
        if time_limit<datetime.now().time() and alarm_timer==0:
            alarm_timer = time()
            playsound(r'C:\Users\user\Dev\AISecurity\Resources\machine-gun-01.wav')
        if time()-alarm_timer>alarm_time_wait:
            alarm_timer =0
    final_frame = cv.resize(output,(WIDTH,HEIGHT))
    cv.imshow('Web-feed',final_frame )

    ###
    if stream & command_active:
        if not connected:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host_name = socket.gethostname()
            print("host name", host_name)
            host_ip = socket.gethostbyname(host_name)
            print('HOST IP:', host_ip)
            port = 9999
            socket_address = (host_ip, port)
            server_socket.bind(socket_address)
            server_socket.listen(5)
            print("LISTENING AT:", socket_address)
            client_socket, addr =server_socket.accept()
            print('GOT CONNECTION FROM:', addr)
            connected = True
        if client_socket:
            # while(final_frame):
                a = pickle.dumps(final_frame)
                message = struct.pack("Q", len(a)) + a
                print(len(message))
                client_socket.sendall(message)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    client_socket.close()
    print('sent')
    if cv.waitKey(1) & 0xFF==ord('q'):
        break

cv.waitKey(0)


##----detect weapon function
###-----load weapon-detection model
weapon_detect_model_path =r'C:\Users\user\Dev\AISurveillance\models\weapon_detect_openvino_model'
weapon_model = torch.hub.load('ultralytics/yolov5', 'custom', path=weapon_detect_model_path)
weapon_model.cpu()
weapon_model.classes =[0,2]

def detect_weapon(f):
    pass
