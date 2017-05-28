import cv2
import sys
import urllib
import time
import json
from firebase.firebase import FirebaseApplication, FirebaseAuthentication
from camera import Camera
import datetime
import threading
import logging

#from google.appengine.ext import vendor
#vendor.add('lib')
#from twisted.internet import reactor
# Get user supplied values

# Global Camera List
cameraList = []

#firebase object defined
SECRET = 'GtxD03WernNP8k0RF4SAbqaXzJNxzLQx77vCmEO6'
DSN = 'https://facedetection-f5595.firebaseio.com'
EMAIL = 'sunilkumarmohanty@gmail.com'
authentication = FirebaseAuthentication(SECRET,EMAIL, True, True)
firebase = FirebaseApplication(DSN, authentication)
#firebase = FirebaseApplication('https://facedetection-f5595.firebaseio.com', None)


##################################

"""
@Method Datafetcher
@desc the method used in the data fetcher thread, runs every 30 seconds.
connects to the firebase DB and retrieves a list of cameras from the cloud and 
stores it in the global camera list
"""


def datafetcher():
    logging.debug("Data fetching thread started")
    while(1):
        # Delete the camera list and put the data to a fresh list everytime
        del cameraList[:] 
        cameras_json = firebase.get('/cameras', None, params= {'print': 'pretty'})
        for d in cameras_json:
            id = d
            ip = cameras_json[d]["IP"]
            name = cameras_json[d]["name"]
            camera = Camera(ip, name, id)
            cameraList.append(camera)
        
        #Make the thread sleep for 30 seconds
        time.sleep(30)

"""
@Method worker
@desc: main worker method, gets the list of cameras, connects to each camera, takes a picture, applies face recognition 
using opencv, gets the count of faces, pushes the data to the cloud
thread sleeps for one second, after the above mentioned cycle and repeats the same thing again.
"""

def worker():
    logging.debug("Worker thread started")
    apppath = "/usr/src/app/"
    cascPath = apppath+"haarcascade_frontalface_default.xml"

    cameraFaces = {}
    
    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)
    i = 50
    data = {'IP': '192.168.1.103',
    'name': 'camera2'}

    while(1):
        for camera in cameraList:
            imageFullPath = apppath+camera.id+".jpg"
            try:
                getFrame(camera.ipaddress, imageFullPath)
            except:
                logging.error("Unable to connect to camera @ " + camera.ipaddress)
                continue
            img = cv2.imread(imageFullPath, 0)
            faces = faceCascade.detectMultiScale(img, 1.3, 5)
            logging.warning("Found {0} faces! ".format(len(faces)))
            if cameraFaces.has_key(camera.ipaddress):
                if cameraFaces[camera.ipaddress] == len(faces):
                    logging.debug("No change in values, so dont post to cloud")
                    continue
            cameraFaces[camera.ipaddress] = len(faces)
            data = {'faces': len(faces),
                'created_at': (datetime.datetime.utcnow()- datetime.datetime(1970,1,1)).total_seconds()}
            firebase.post('/faces/'+camera.id+"/",data)
        
        #Thread sleeps for 1 second
        time.sleep(1)


"""
@method main
@desc: main method for the program
starts the threads - main worker thread,
and data retreival thread
"""
def main():
    logging.warning("Starting main...")
    workerthread = threading.Thread(name='worker', target=worker)
    datathread= threading.Thread(name='data', target=datafetcher)

    logging.warning("Starting worker thread...")
    workerthread.start()
    
    logging.warning("Starting data retrieval thread...")
    datathread.start()

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def getCameras():
     cameras_json = firebase.get('/cameras', None, params= {'print': 'pretty'})
     logging.debug(camera_json)

def loadcameras(cameras_json):
    for d in cameras_json:
        id = d
        ip = cameras_json[d]["IP"]
        name = cameras_json[d]["name"]
        camera = Camera(ip, name, id)
        cameraList.append(camera)

def getFrame(Camera_IP, imageFullPath):
    imageFile = urllib.URLopener()
    imageFile.retrieve("http://"+ Camera_IP + ":8080/photo.jpg", imageFullPath)

if __name__ == '__main__':
    main()
