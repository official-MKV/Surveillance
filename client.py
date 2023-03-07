import socket
import cv2
import pickle
import torch
import struct
import time



client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.194.214'
port = 9999
connected = False
while connected!=True:
    try:
        client_socket.connect((host_ip, port))
        connected=True
        print('Connnected: ',connected)
    except Exception as e:
        print(e)
        time.sleep(3)
data = b""
payload_size = struct.calcsize("Q")
print('payload_size',payload_size)
while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4*1024)
        if not packet:
            break
        data += packet


    print('len of data:',len(data))

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]

    print('packed_msg_size:',packed_msg_size)
    msg_size = struct.unpack("Q", packed_msg_size)[0]
    print('msg_size: ',msg_size)


    while len(data) < msg_size:
        data += client_socket.recv(4*1024)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data)
    # time.sleep(3)
    cv2.imshow("RECEIVING VIDEO", frame)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        client_socket.close()
        break

