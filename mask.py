import warnings
warnings.filterwarnings('ignore')
import numpy as np
import cv2
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import imutils

def mask():
	detection_model_path = 'haarcascade_frontalface_default.xml'
	emotion_model_path = '_mini_XCEPTION.106-0.65.hdf5'

	# hyper-parameters for bounding boxes shape
	# loading models
	face_detection = cv2.CascadeClassifier(detection_model_path)



	emotion_classifier = load_model(emotion_model_path, compile=False)
	EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised",
				"neutral"]


	facedetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	threshold=0.90
	cap=cv2.VideoCapture(0)
	cap.set(3, 640)
	cap.set(4, 480)
	font=cv2.FONT_HERSHEY_COMPLEX
	model = load_model('MyTrainingModel.h5')


	while True:
		sucess, imgOrignal=cap.read()
		faces = facedetect.detectMultiScale(imgOrignal,1.3,5)
		imgOrignal = imutils.resize(imgOrignal, width=600)
		imgOrignal = imgOrignal.copy()
		for x,y,w,h in faces:
			crop_img=imgOrignal[y:y+h,x:x+h]
			img=cv2.resize(crop_img, (32,32))
			img = img.astype("uint8")
			img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			img = cv2.equalizeHist(img)
			img = img / 255
			img=img.reshape(1, 32, 32, 1)
			prediction=model.predict(img)
			classIndex=model.predict_classes(img)
			probabilityValue=np.amax(prediction)
			if probabilityValue>threshold:
				if classIndex==0:
					classIndex="mask"
					cv2.rectangle(imgOrignal,(x,y),(x+w,y+h),(0,255,0),2)
					cv2.rectangle(imgOrignal, (x,y-40),(x+w, y), (0,255,0),-2)
					cv2.putText(imgOrignal, classIndex,(x,y-10), font, 0.75, (255,255,255),1, cv2.LINE_AA)
				elif classIndex==1:
					classIndex="No Mask"
					cv2.rectangle(imgOrignal,(x,y),(x+w,y+h),(50,50,255),2)
					cv2.rectangle(imgOrignal, (x,y-40),(x+w, y), (50,50,255),-2)
					cv2.putText(imgOrignal, classIndex,(x,y-10), font, 0.75, (255,255,255),1, cv2.LINE_AA)

			if len(faces) > 0:
				faces = sorted(faces, reverse=True,
							key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
				(fX, fY, fW, fH) = faces
				# Extract the ROI of the face from the grayscale image, resize it to a fixed 48x48 pixels, and then prepare
				# the ROI for classification via the CNN
				gray = cv2.cvtColor(imgOrignal, cv2.COLOR_BGR2GRAY)
				roi = gray[fY:fY + fH, fX:fX + fW]
				roi = cv2.resize(roi, (48, 48))
				roi = roi.astype("float") / 255.0
				roi = img_to_array(roi)
				roi = np.expand_dims(roi, axis=0)

				preds = emotion_classifier.predict(roi)[0]
				emotion_probability = np.max(preds)
				label = EMOTIONS[preds.argmax()]
				cv2.putText(imgOrignal, label, (fX, fY + 10),
						cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 0, 0), 2)
				# cv2.putText(imgOrignal,str(round(probabilityValue*100, 2))+"%" ,(180, 75), font, 0.75, (255,0,0),2, cv2.LINE_AA)
		cv2.imshow("Result",imgOrignal)
		k=cv2.waitKey(1)
		if k==ord('q'):
			break


	cap.release()
	cv2.destroyAllWindows()














