import cv2
import numpy as np
from win32api import GetSystemMetrics

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, GetSystemMetrics(0))
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, GetSystemMetrics(1))

while True:
    logo_name = input("Enter The Image Name: ")
    logo = cv2.imread(logo_name + '.png')
    size = 533

    logo = cv2.resize(logo, (size, size))

    img2gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 0, 255, cv2.THRESH_BINARY)

    placex = int(input("Enter The X Value Where The Image Should Placed: "))
    placey = int(input("Enter The Y Value Where The Image Should Placed: "))

    while cap.isOpened():

        ret, frame = cap.read()
        if ret:

            frame = cv2.flip(frame, 1)

            roi = frame[-size - placex:-placex, -size - placey:-placey]

            roi[np.where(mask)] = 0
            roi += logo

            cv2.imshow('AR TEACH CAM', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    cv2.destroyAllWindows()