import csv
import cv2
import time, datetime
import win32api

import mysql.connector

ts = time.time()
Date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
mydb = mysql.connector.connect(host="localhost", user="root", password="", database="mydababase")
mycursor = mydb.cursor()




def Attendance():

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX



    # initiate id counter
    id = 0

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # set video width
    cam.set(4, 480)  # set video height
    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )
    if len(faces)==0:
        win32api.MessageBox(0, 'User cant be seen', 'Error')
    else:
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            # If confidence is less them 100 ==> "0" : perfect match
            if (confidence < 80):
                mycursor.execute("""SELECT name FROM student  WHERE id ="""+ str(id))
                data = mycursor.fetchall()
                idd=id
                for row in data:
                    id=row[0]
                    print(id)
                    cv2.putText(img, id, (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                    row = [str(id), Date, Time]
                    cv2.imshow('camera', img)
                    win32api.MessageBox(0, 'Taking attendance for user '+id, 'Info')
                    sql = "select * from attendance where id_student = %s and Attendance = %s"
                    mycursor.execute(sql, (idd, Date))
                    result = mycursor.fetchall()
                    number=len(result)
                    print(len(result))
                    if number == 0:
                        sql="INSERT INTO attendance (id_student, Attendance, time) VALUES (%s, %s, %s)"
                        mycursor.execute(sql, (idd, Date, Time))
                        mydb.commit()
                        with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
                                    writer = csv.writer(csvFile, delimiter=',')
                                    writer.writerow(row)
                                    csvFile.close()
                    else:
                        win32api.MessageBox(0, 'this user already took attendance' , 'Info')
                    cam.release()
                    cv2.destroyAllWindows()
            else:
                win32api.MessageBox(0, 'User not found in database please register', 'Info')


