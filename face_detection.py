import numpy as np
import cv2
import serial
import time

#CENTER OF WEBCAM
originx = 300
originy = 250

#takes position and sends to arduino serial port
def servo_write(position):
    arduinoData.write(str(position).encode())

#returns distance in smaller integers (scaled around 0-10)
def convert_data(data):
    return int(data/56 + 5)
    
#returns distance from origin
def return_dist(point,origin):
    return point-origin

#creates an instance for video to capture
cap = cv2.VideoCapture(0)

#face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#creates an instance for serial data
arduinoData = serial.Serial('COM3', 9600)

#gives time for serial to catchup
time.sleep(3)

#loops for checking faces
while True:

    #START OF FACE DETECTION#
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    #creates dot at center of webcam
    cv2.circle(frame, (originx,originy), radius=0, color=(255, 0, 0), thickness=3)

    #when a face is detected:
    for (x, y, w, h) in faces:

        #calculating center of face center of face
        servo_x = int(x+w/2)
        servo_y = int(y+h/2)

        #creates dot in center of face
        cv2.circle(frame, (servo_x,servo_y), radius=0, color=(0, 0, 255), thickness=3)
        
        #prints distance from face to center of webcam
        print("x: " + str(return_dist(servo_x,originx)))
        
        #sends the arduino amount to move servo
        servo_write(convert_data(return_dist(servo_x,originx)))
        time.sleep(4)
        
    #stops program when "q" is pressed 
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break
    #END OF FACE DETECTION#

    #prints arduino's serial data
    if arduinoData.inWaiting() > 0:
        serialData = arduinoData.readline().decode().strip()
        print(serialData)

cap.release()
cv2.destroyAllWindows()