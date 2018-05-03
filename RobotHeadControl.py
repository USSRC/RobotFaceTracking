import cv2
import sys
import serial
import time
import imutils

timing = 0;
emptyCount = 0

ser = serial.Serial('COM7', 115200, timeout=1)

cascPath = "haarcascade_frontalface_alt2.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

video_capture.set(3,400)
video_capture.set(4,320)

width = video_capture.get(3)
height = video_capture.get(4)

font = cv2.FONT_HERSHEY_DUPLEX
ser.write('5')
print(width)
print(height)

screenCenter = int(width / 2)

#640 x 480
while True:
    
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    frame = imutils.resize(frame, width=400)

    cv2.line(frame, (screenCenter, 0), (screenCenter, 480), (255,0,0), 2)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    if len(faces)  == 0:
        emptyCount += 1
        if(timing == 0):
            startMillis = int(round(time.time() * 1000))
            timing = 1
            print("Timing Started")
        elif(timing == 1):
            curMillis = int(round(time.time() * 1000))
            print("Curr: " + str(curMillis))
            print("Total: " + str(curMillis - startMillis))
            if(((curMillis - startMillis) >= 3000) and (emptyCount > 10)):
                timing = 0
                if emptyCount >= 10:
                    ser.write('5')
                    print("Turning Back")
                    timing = 0
    else:
        emptyCount = 0

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        faceCenter = ((x+w)-x)/2 #find the center of the face
        cv2.line(frame, (x+faceCenter, y), (x+faceCenter, y+h), (255,0,0), 2)
        diff = screenCenter-(x+faceCenter)
        #cv2.putText(frame ,str(diff),(20,300), font, 1,(0,0,255),2,cv2.LINE_AA)
        if(diff > 1):
            if(((diff - 1) > 50) or (diff - 1 == 0)):
                cv2.putText(frame ,"Turn Left Large",(20,50), font, 1,(0,0,255),2,cv2.LINE_AA)
                ser.write('2')
            elif(((diff - 1) > 20) or (diff - 1 == 0)):
                cv2.putText(frame ,"Turn Left Small",(20,50), font, 1,(0,0,255),2,cv2.LINE_AA)
                ser.write('1')
            else:
                cv2.putText(frame ,"Good",(20,50), font, 1,(0,255,0),2,cv2.LINE_AA)
        elif(diff < 1):
            if(((1 - diff) > 50) or (1 - diff == 0)):
                cv2.putText(frame ,"Turn Right Large",(20,50), font, 1,(0,0,255),2,cv2.LINE_AA)
                ser.write('4')
            elif(((1 - diff) > 20) or (1 - diff == 0)):
                cv2.putText(frame ,"Turn Right Small",(20,50), font, 1,(0,0,255),2,cv2.LINE_AA)
                ser.write('3')
            else:
                cv2.putText(frame ,"Good",(20,50), font, 1,(0,255,0),2,cv2.LINE_AA)
            
    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
