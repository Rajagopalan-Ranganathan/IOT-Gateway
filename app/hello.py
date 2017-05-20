import cv2
import sys
import urllib
import time
from firebase import firebase
# Get user supplied values
def main():
    imagePath = "/usr/src/app/photo.jpg"
    cascPath = "/usr/src/app/haarcascade_frontalface_default.xml"
    camIP = "192.168.1.100"
    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)
    i = 0
    # Read the image
    while(i < 1):
        i = i+1
        getFrame(camIP)
        img = cv2.imread(imagePath,0)
        faces = faceCascade.detectMultiScale(img, 1.3, 5)
        print("Found {0} faces!".format(len(faces)))
        time.sleep(1)
    firebase = firebase.FirebaseApplication('https://facedetection-f5595.firebaseio.com/', None)
    result = firebase.get('/test', None)
    print result

# image = cv2.imread(imagePath,0)
#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
# faces = faceCascade.detectMultiScale(
#     image,
#     scaleFactor=1.1,
#     minNeighbors=5,
#     minSize=(30, 30),
# )


# print(camIP)
#cv2.imshow("Faces found", image)
#cv2.waitKey(0)
def getFrame(Camera_IP):
        imageFile = urllib.URLopener()
        #print("http://"+ Camera_IP + ":8080/photo.jpg")
        imageFile.retrieve("http://"+ Camera_IP + ":8080/photo.jpg", '/usr/src/app/photo.jpg')

main()
