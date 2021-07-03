import csv

import cv2
import numpy as np
import os
import time, datetime
from keras.preprocessing import image
from keras.models import model_from_json
import mysql.connector
from keras.models import load_model

mydb = mysql.connector.connect(host="localhost", user="root", password="", database="mydababase")
mycursor = mydb.cursor()


def Realtime():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX

    emotion_model_path = '_mini_XCEPTION.106-0.65.hdf5'
    emotion_classifier = load_model(emotion_model_path, compile=False)
    id = 0
    # names related to ids: example ==> Marcelo: id=1,  etc
    emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # set video widht
    cam.set(4, 480)  # set video height
    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)
    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            roi_gray = gray[y:y + w, x:x + h]  # cropping region of interest i.e. face area from  image

            roi_gray = cv2.resize(roi_gray, (48, 48))
            img_pixels = image.img_to_array(roi_gray)
            img_pixels = np.expand_dims(img_pixels, axis=0)
            img_pixels /= 255
            predictions = emotion_classifier.predict(img_pixels)

            # find max indexed array
            max_index = np.argmax(predictions[0])
            predicted_emotion = emotions[max_index]

            # If confidence is less them 100 ==> "0" : perfect match
            if (confidence < 75):
                mycursor.execute("""SELECT name FROM student WHERE id ="""+ str(id))
                data = mycursor.fetchall()
                for row in data:
                    id=row[0]
            else:
                id = "unknown"
                print(confidence)


            cv2.putText(img,id, (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, predicted_emotion, (x + 5, y + h - 5), font, 1, (255, 255, 255), 2)

        cv2.imshow('AMEI System', img)
        k = cv2.waitKey(3) & 0xff  # Press 'ESC' for exiting video
        if k == 27:
            break

    # Do a bit of cleanup
    print("\n [INFO] Exiting Program")
    cam.release()
    cv2.destroyAllWindows()
