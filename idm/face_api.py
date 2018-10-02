# import the necessary packages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import base64
from PIL import Image
from io import StringIO
import numpy as np
import urllib.request
import uuid, random, cv2, os, json, time
from .models import CustomUser as User
from .models import Product, Face
import requests
from io import BytesIO


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# define the path to the face detector and smile detector
FACE_DETECTOR_PATH = "{base_path}/cascades/haarcascade_frontalface_default.xml".format(
	base_path=os.path.abspath(os.path.dirname(__file__)))

SMILE_DETECTOR_PATH = "{base_path}/cascades/haarcascade_smile.xml".format(
	base_path=os.path.abspath(os.path.dirname(__file__)))

# path to trained faces and labels
TRAINED_FACES_PATH = "{base_path}/faces".format(
	base_path=os.path.abspath(os.path.dirname(__file__)))

# maximum distance between face and match
THRESHOLD = 75

server = 'http://127.0.0.1:8000'

def get_images_and_labels():
	# images will contains face images
	images = []
	# labels will contains the label that is assigned to the image
	labels = []
	# create the cascade classifiers
	detector = cv2.CascadeClassifier(FACE_DETECTOR_PATH)
	all_users = User.objects.all()
	for each_user in all_users:
		face_pics = Face.objects.filter(userr=each_user)
		for face_pic in face_pics:
			faces = []
			# Read the image and convert to grayscale
			url = server + face_pic.pic.url
			response = requests.get(url)
			image_pil = Image.open(BytesIO(response.content)).convert('L')
			# image_pil = Image.open(server + face_pic.pic.url).convert('L')
			# Convert the image format into numpy array
			image = np.array(image_pil, 'uint8')
			# Detect the face in the image
			faces = detector.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
			# If face is detected, append the face to images and the label to labels
			if len(faces) > 0:
				for (x, y, w, h) in faces:
					images.append(image[y: y + h, x: x + w])
					labels.append(each_user.pk)
					# cv2.imshow("Adding faces to traning set...", image[y: y + h, x: x + w])
					# cv2.waitKey(50)
					print('Adding faces to traning set..')
		# return the images list and labels list
	return images, labels


# Detect
def recognize_face(face_image):
	detected = 0
	faceDetector = cv2.CascadeClassifier(FACE_DETECTOR_PATH)
	# creating recognizer
	rec = cv2.face.LBPHFaceRecognizer_create()
	# loading the training data
	rec.read(BASE_DIR + '/trained/trainedData.yml')
	getId = 0
	t_end = time.time() + 60 * 2  # Run this loop for 2 minutes
	faces = []
	gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
	faces = faceDetector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
	if len(faces) > 0:
		for(x,y,w,h) in faces:
			# cv2.rectangle(img,(x,y),(x+w,y+h), (0,255,0), 2)
			getId, conf = rec.predict(gray[y:y+h, x:x+w]) #This will predict the id of the face
			print('{0} {1}'.format(conf, getId))
			if conf < 50:
				detected = getId
			else:
				detected = 0
	return detected

# Old Method
def recognize_face_old():
	detected = None
	faceDetector = cv2.CascadeClassifier(FACE_DETECTOR_PATH)
	cam = cv2.VideoCapture(0)
	# creating recognizer
	rec = cv2.face.LBPHFaceRecognizer_create()
	# loading the training data
	rec.read(BASE_DIR + '/trained/trainedData.yml')
	getId = 0
	t_end = time.time() + 60 * 2  # Run this loop for 2 minutes
	faces = []
	while(time.time() < t_end):
		ret, img = cam.read()
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces = faceDetector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
		if len(faces) > 0:
			for(x,y,w,h) in faces:
				# cv2.rectangle(img,(x,y),(x+w,y+h), (0,255,0), 2)
				getId, conf = rec.predict(gray[y:y+h, x:x+w]) #This will predict the id of the face
				#print conf
				if conf < 35:
					detected = getId
					cam.release()
					return detected
				else:
					detected = None
	cam.release()
	return detected



def train_faces():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    images, labels = get_images_and_labels()
    if len(labels) > 0:
        recognizer.train(images, np.array(labels))
        recognizer.save(BASE_DIR + '/trained/trainedData.yml')
        return 'Trained Successfully!'
    return 'An Error Occured!, Maybe the face dataset is empty.'
