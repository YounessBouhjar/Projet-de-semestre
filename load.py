import cv2
import face_recognition
import numpy as np
import win32api
from keras.preprocessing import image
from keras.models import model_from_json
from keras.models import load_model
import mysql.connector
import easygui

mydb = mysql.connector.connect(host="localhost", user="root", password="", database="mydababase")
mycursor = mydb.cursor()
def Load():

    cascadePath = "haarcascade_frontalface_default.xml"
    emotion_model_path = '_mini_XCEPTION.106-0.65.hdf5'
    emotion_classifier = load_model(emotion_model_path, compile=False)

    faceCascade = cv2.CascadeClassifier(cascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX

    emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')

    imagePath = easygui.fileopenbox(msg="Select image file", default=r"C:\Users\youne\Desktop\Nouveau dossier\*", filetypes=["*.jpeg"])
    if imagePath is None:
        return
    else:
        img = cv2.imread(imagePath)
        resized = cv2.resize(img, (640,480), interpolation = cv2.INTER_AREA)
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(64, 48)
        )
        print("Found {0} faces!".format(len(faces)))
        if len(faces) > 0:
            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(resized, (x, y), (x + w, y + h), (0, 255, 0), 2)
                roi_gray = gray[y:y + w, x:x + h]  # cropping region of interest i.e. face area from  image

                roi_gray = cv2.resize(roi_gray, (48, 48))
                img_pixels = image.img_to_array(roi_gray)
                img_pixels = np.expand_dims(img_pixels, axis=0)
                img_pixels /= 255
                predictions = emotion_classifier.predict(img_pixels)

                # find max indexed array
                max_index = np.argmax(predictions[0])
                predicted_emotion = emotions[max_index]
                cv2.putText(resized, predicted_emotion, (x + 5, y + h - 5), font, 1, (255, 255, 255), 2)

                cv2.imshow('Emotion', resized)
        else:
            win32api.MessageBox(0, 'no face found', 'Info')


cv2.waitKey(0)

