import cv2
import numpy as np
import face_recognition
import os
from datetime import  datetime

# for storing the images into separate classes

path = 'imageatt'
images = []
classnames= []
mylist = os.listdir(path)
print(mylist)
for cls in mylist:
    curimg =cv2.imread(f'{path}/{cls}')
    images.append(curimg)
    classnames.append(os.path.splitext(cls)[0])
print(classnames)

# To detect the faces in the img and find the encoding of the faces

def findencodings(images):
    encodelist = []
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist

# to create an excel sheet and store the data of the person(here name_id and time)

def detprisoner(name):
    with open('prison.csv','r+') as f:
        mydatalist = f.readlines()
        namelist = []
        for line in mydatalist:
            entry = line.split(',')
            namelist.append(entry[0])
        if name not in namelist:
            now = datetime.now()
            dtstring = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtstring}')

encodelistknown = findencodings(images)
print('encoding complete')

# to turn on the webcam

cap = cv2.VideoCapture(0)

# to detect and encode the faces seen in the webcam

while True:
    success, img = cap.read()
    imgs = cv2.resize(img,(0,0),None,0.25,0.25)
    imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

    facescurframe = face_recognition.face_locations(imgs)
    encodescurframe = face_recognition.face_encodings(imgs,facescurframe)

    for encodeface,faceloc in zip(encodescurframe,facescurframe):
        matches = face_recognition.compare_faces(encodelistknown,encodeface)
        facedis = face_recognition.face_distance(encodelistknown,encodeface)
        #print(facedis)
        matchindex = np.argmin(facedis)

    # face of the person with their name is displayed in the webcam

        if matches[matchindex]:
            name = classnames[matchindex].upper()
            #print(name)
            y1,x2,y2,x1 = faceloc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            detprisoner(name)

    cv2.imshow('webcam',img)
    cv2.waitKey(10)
    
