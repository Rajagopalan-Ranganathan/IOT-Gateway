import cv2
import sys

# Get user supplied values
imagePath = "/usr/src/app/abba.png"
cascPath = "/usr/src/app/haarcascade_frontalface_default.xml"

# Create the haar cascade
faceCascade = cv2.CascadeClassifier(cascPath)

# Read the image
image = cv2.imread(imagePath,0)
#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = faceCascade.detectMultiScale(
    image,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30),
)

print("Found {0} faces!".format(len(faces)))
camIP = raw_input("Insert your android camera's IP: ")

print(camIP)
#cv2.imshow("Faces found", image)
#cv2.waitKey(0)
