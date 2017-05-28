import cv2
import sys
import urllib
import time
import json
from firebase.firebase import FirebaseApplication, FirebaseAuthentication
from camera import Camera
import datetime
import threading
#from google.appengine.ext import vendor
#vendor.add('lib')
#from twisted.internet import reactor
# Get user supplied values
cameraList = []
firebase = FirebaseApplication('https://facedetection-f5595.firebaseio.com', None)

##################################
def datafetcher():
    #i=10
    while(1):
        print "Fetching data"
        del cameraList[:]
        cameras_json = firebase.get('/cameras', None, params= {'print': 'pretty'})
        for d in cameras_json:
            id = d
            ip = cameras_json[d]["IP"]
            name = cameras_json[d]["name"]
            camera = Camera(ip, name, id)
            cameraList.append(camera)
        time.sleep(10)
        #i-=1


def worker():
    # path - /usr/src/app
    imagePath = "./"
    cascPath = "./haarcascade_frontalface_default.xml"

    cameraFaces = {}
    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)
    i = 50
    data = {'IP': '192.168.1.103',
    'name': 'camera2'}
    # while(i):
    #     print "working"
    #     print len(cameraList)
    #     # for camera in cameraList:
    #     #     print camera
    #     time.sleep(1)
    #     i-=1


    while(1):
        print "worker thread running"
        #i = i+1
        for camera in cameraList:
            imageFullPath = imagePath+camera.id+".jpg"
            try:
                getFrame(camera.ipaddress, imageFullPath)
            except:
                print "Unable to connect to camera @ " + camera.ipaddress
                continue
            img = cv2.imread(imageFullPath, 0)
            faces = faceCascade.detectMultiScale(img, 1.3, 5)
            print("Found {0} faces! ".format(len(faces)))
            if cameraFaces.has_key(camera.ipaddress):
                if cameraFaces[camera.ipaddress] == len(faces):
                    continue
            cameraFaces[camera.ipaddress] = len(faces)
            data = {'faces': len(faces),
                'created_at': datetime.datetime.now()}
            firebase.post('/faces/'+camera.id+"/",data)
        print len(cameraList)
        #reactor.callInThread(getCameras)
        print len(cameraList)
        time.sleep(1)


def main():
    workerthread = threading.Thread(name='worker', target=worker)
    datathread= threading.Thread(name='data', target=datafetcher)
    #w2 = threading.Thread(target=worker) # use default name

    workerthread.start()
    #w2.start()
    datathread.start()
    # # path - /usr/src/app
    # imagePath = "./"
    # cascPath = "./haarcascade_frontalface_default.xml"

    # cameraFaces = {}
    # # Create the haar cascade
    # faceCascade = cv2.CascadeClassifier(cascPath)
    # i = 0
    # data = {'IP': '192.168.1.103',
    # 'name': 'camera2'}

    # #firebase.post('/cameras',data)
    
    # #loadcameras(cameras_json)
    # # Read the image
    # while(i < 5):
    #     i = i+1
    #     for camera in cameraList:
    #         imageFullPath = imagePath+camera.id+".jpg"
    #         try:
    #             getFrame(camera.ipaddress, imageFullPath)
    #         except:
    #             print "Unable to connect to camera @ " + camera.ipaddress
    #             continue
    #         img = cv2.imread(imageFullPath, 0)
    #         faces = faceCascade.detectMultiScale(img, 1.3, 5)
    #         print("Found {0} faces! ".format(len(faces)))
    #         if cameraFaces.has_key(camera.ipaddress):
    #             if cameraFaces[camera.ipaddress] == len(faces):
    #                 continue
    #         cameraFaces[camera.ipaddress] = len(faces)
    #         data = {'faces': len(faces),
    #             'created_at': datetime.datetime.now()}
    #         firebase.post('/faces/'+camera.id+"/",data)
    #     print len(cameraList)
    #     #reactor.callInThread(getCameras)
    #     print len(cameraList)
    #     time.sleep(1)
    # authentication = FirebaseAuthentication('GtxD03WernNP8k0RF4SAbqaXzJNxzLQx77vCmEO6', 'sunilkumarmohanty@gmail.com',None)
    # user = authentication.get_user()
    # # print user.firebase_auth_token

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def getCameras():
     cameras_json = firebase.get('/cameras', None, params= {'print': 'pretty'})
     print camera_json

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
