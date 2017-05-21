import cv2
import sys
import urllib
import time
import json
from firebase.firebase import FirebaseApplication, FirebaseAuthentication
# Get user supplied values

def main():
    imagePath = "/usr/src/app/photo.jpg"
    cascPath = "/usr/src/app/haarcascade_frontalface_default.xml"
    camIP = "192.168.1.100"
    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)
    i = 0
    firebase = FirebaseApplication('https://facedetection-f5595.firebaseio.com', None)
    # Read the image
    while(i < 5):
        i = i+1
        getFrame(camIP)
        img = cv2.imread(imagePath,0)
        faces = faceCascade.detectMultiScale(img, 1.3, 5)
        print("Found {0} faces! ".format(len(faces)))
        firebase.post('/camera1','{faces:1}')
        time.sleep(1)
    authentication = FirebaseAuthentication('GtxD03WernNP8k0RF4SAbqaXzJNxzLQx77vCmEO6', 'sunilkumarmohanty@gmail.com',None)

    user = authentication.get_user()
    print user.firebase_auth_token
    result = firebase.get('/cameras', None, params= {'print': 'pretty'})
    print result

def getFrame(Camera_IP):
        imageFile = urllib.URLopener()
        #print("http://"+ Camera_IP + ":8080/photo.jpg")
        imageFile.retrieve("http://"+ Camera_IP + ":8080/photo.jpg", '/usr/src/app/photo.jpg')
if __name__ == '__main__':
    main()
