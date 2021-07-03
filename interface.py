import win32api
import mysql.connector
import cv2
from PyQt5 import QtCore, QtWidgets

from table import Ui_MainWindowT
from Realtime import Realtime
from TrainImages import TrainImages
from attendance import Attendance
from load import Load
from mask import mask
mydb = mysql.connector.connect(host="localhost", user="root", password="", database="mydababase")
mycursor = mydb.cursor()


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        MainWindow.setStyleSheet(
                                 "QWidget\n"
                                 "{\n"
                                 "    color: #b1b1b1;\n"
                                 "    background-color: #323232;\n"
                                 "}\n"
                                 "\n"
                                 "QLineEdit\n"
                                 "{\n"
                                 "    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0 #646464, stop: 1 #5d5d5d);\n"
                                 "    padding: 1px;\n"
                                 "    border-style: solid;\n"
                                 "    border: 1px solid #1e1e1e;\n"
                                 "    border-radius: 5;\n"
                                 "}\n"
                                 "\n"
                                 "QPushButton\n"
                                 "{\n"
                                 "    color: #b1b1b1;\n"
                                 "    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);\n"
                                 "    border-width: 1px;\n"
                                 "    border-color: #1e1e1e;\n"
                                 "    border-style: solid;\n"
                                 "    border-radius: 6;\n"
                                 "    padding: 3px;\n"
                                 "    font-size: 12px;\n"
                                 "    padding-left: 5px;\n"
                                 "    padding-right: 5px;\n"
                                 "}\n"
                                 "\n"
                                 "QPushButton:pressed\n"
                                 "{\n"
                                 "    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);\n"
                                 "}\n"
                                 "\n"
                                 "QPushButton:hover\n"
                                 "{\n"
                                 "    border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
                                 "}\n"
                                 "\n"
                                 "\n"
                                 "QProgressBar\n"
                                 "{\n"
                                 "    border: 2px solid grey;\n"
                                 "    border-radius: 5px;\n"
                                 "    text-align: center;\n"
                                 "}\n"
                                 "\n"
                                 "QProgressBar::chunk\n"
                                 "{\n"
                                 "    background-color: #d7801a;\n"
                                 "    width: 2.15px;\n"
                                 "    margin: 0.5px;\n"
                                 "}\n"
                                 "\n")
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(20, 40, 761, 521))
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.groupBox = QtWidgets.QGroupBox(self.groupBox_4)
        self.groupBox.setGeometry(QtCore.QRect(30, 40, 701, 131))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(60, 35, 71, 31))
        self.label.setObjectName("label")
        self.train = QtWidgets.QPushButton(self.groupBox)
        self.train.setGeometry(QtCore.QRect(480, 30, 161, 81))
        self.train.setObjectName("train")
        self.addstudent = QtWidgets.QPushButton(self.groupBox)
        self.addstudent.setGeometry(QtCore.QRect(280, 30, 161, 81))
        self.addstudent.setObjectName("addstudent")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(180, 35, 31, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.label1 = QtWidgets.QLabel(self.groupBox)
        self.label1.setGeometry(QtCore.QRect(50, 75, 80, 31))
        self.label1.setObjectName("label1")

        self.lineEdit1 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit1.setGeometry(QtCore.QRect(150, 75, 100, 31))
        self.lineEdit1.setObjectName("lineEdit1")
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox_4)
        self.groupBox_2.setGeometry(QtCore.QRect(30, 190, 701, 131))
        self.groupBox_2.setObjectName("groupBox_2")
        self.realtime = QtWidgets.QPushButton(self.groupBox_2)
        self.realtime.setGeometry(QtCore.QRect(60, 30, 161, 81))
        self.realtime.setObjectName("realtime")
        self.load = QtWidgets.QPushButton(self.groupBox_2)
        self.load.setGeometry(QtCore.QRect(270, 30, 161, 81))
        self.load.setObjectName("load")
        self.mask = QtWidgets.QPushButton(self.groupBox_2)
        self.mask.setGeometry(QtCore.QRect(480, 30, 161, 81))
        self.mask.setObjectName("mask")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_4)
        self.groupBox_3.setGeometry(QtCore.QRect(30, 340, 701, 131))
        self.groupBox_3.setObjectName("groupBox_3")
        self.attendance = QtWidgets.QPushButton(self.groupBox_3)
        self.attendance.setGeometry(QtCore.QRect(110, 30, 161, 81))
        self.attendance.setObjectName("attendance")
        self.table = QtWidgets.QPushButton(self.groupBox_3)
        self.table.setGeometry(QtCore.QRect(430, 30, 161, 81))
        self.table.setObjectName("table")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.realtime.clicked.connect(Realtime)
        self.addstudent.clicked.connect(self.ADDStudent)
        self.train.clicked.connect(TrainImages)
        self.attendance.clicked.connect(Attendance)
        self.load.clicked.connect(Load)
        self.table.clicked.connect(self.loadTable)
        self.mask.clicked.connect(mask)

    def loadTable(self):
        self.window= QtWidgets.QMainWindow()
        self.ui = Ui_MainWindowT()
        self.ui.setupUi(self.window)
        self.window.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AMEI System"))
        self.realtime.setText(_translate("MainWindow", "Real time"))
        self.load.setText(_translate("MainWindow", "Load "))
        self.attendance.setText(_translate("MainWindow", "Attendance"))
        self.groupBox.setTitle(_translate("MainWindow", "Info"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Detection"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Attendance"))
        self.label.setText(_translate("MainWindow", "Student ID"))
        self.label1.setText(_translate("MainWindow", "Student Name"))
        self.train.setText(_translate("MainWindow", "Train images"))
        self.addstudent.setText(_translate("MainWindow", "ADD Student"))
        self.table.setText(_translate("MainWindow","Attendance Report"))
        self.mask.setText(_translate("MainWindow","Mask"))

    def ADDStudent(self):
        try:
            face_id = int(self.lineEdit.text())
        except:
            face_id = None
        face_name = self.lineEdit1.text()

        if not face_id or face_name == "":
            win32api.MessageBox(0, 'Please Enter Valid ID And Name', 'Error')

        elif isinstance(face_id, int):
            mycursor.execute(
                            """
             SELECT name, COUNT(*)
             FROM student
             WHERE id ="""+str(face_id)
            )
            data = mycursor.fetchall()
            for row in data:
                if row[1] == 0:
                    win32api.MessageBox(0, 'Your Camera Will Run Please Stand Still', 'Info')
                    cam = cv2.VideoCapture(0)
                    cam.set(3, 640)  # set video width
                    cam.set(4, 480)  # set video height
                    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
                    # For each person, enter one numeric face id
                    print("\n [INFO] Initializing face capture. Look the camera and wait ...")
                    # Initialize individual sampling face count
                    count = 0
                    while (True):
                        ret, img = cam.read()
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        faces = face_detector.detectMultiScale(gray, 1.3, 5)
                        for (x, y, w, h) in faces:
                            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                            count += 1
                            # Save the captured image into the datasets folder
                            cv2.imwrite("dataset/User." + str(face_id) + '.' +
                                        str(count) + ".jpg", gray[y:y + h, x:x + w])
                            cv2.imshow('image', img)

                        k = cv2.waitKey(3) & 0xff  # Press 'ESC' for exiting video
                        if k == 27:
                            break
                        elif count >= 50:  # Take 50 face sample and stop video
                            break
                    # Do a bit of cleanup
                    print("\n [INFO] Exiting Program and cleanup stuff")
                    cam.release()
                    cv2.destroyAllWindows()
                    sql = "INSERT INTO student (id, name) VALUES (%s, %s)"
                    var = (face_id, face_name)
                    mycursor.execute(sql, var)
                    mydb.commit()
                else:
                    win32api.MessageBox(0, 'ID already exists', 'Error')



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
