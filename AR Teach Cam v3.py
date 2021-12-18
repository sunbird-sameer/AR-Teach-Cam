import cv2
import numpy as np
import pyautogui
import requests
import os

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
width, height = pyautogui.size()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

cd = os.getcwd()

apikey = input("Enter Your remove.bg API Key: ")

while True:

    logo_name = input("Enter The Image Name: ")

    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open(cd + "\\" + logo_name + '.jpg', 'rb')},
        data={'size': 'auto'},
        headers={'X-Api-Key': apikey},
    )
    if response.status_code == requests.codes.ok:
        with open('no-bg' + logo_name+ '.png', 'wb') as out:
            out.write(response.content)
    else:
        pass

    logo = cv2.imread('no-bg' + logo_name + '.png')


    sizex = np.shape(logo)[0]
    sizey = np.shape(logo)[1]

    if sizey > sizex:
        sizex = 360
        sizey = 640
    elif sizex > sizex:
        sizex = 640
        sizey = 360

    logo = cv2.resize(logo, (sizey, sizex))


    img2gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 0, 255, cv2.THRESH_BINARY)

   
    while cap.isOpened():

        ret, frame = cap.read()
        if ret:

            frame = cv2.flip(frame, 1)

            roi = frame[-sizex-33:-33, -sizey-44:-44]
            roi[np.where(mask)] = 0
            roi += logo

            cv2.imshow('AR Teach Cam', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            pass
        

    cv2.destroyAllWindows()
