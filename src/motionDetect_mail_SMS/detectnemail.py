#-*- coding: utf-8-*-
import cv2
import numpy as np
import motion
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from smsSender import twilioSMS


smtp_server = "smtp.gmail.com"
port = 587
portssl = 465
userid = "jsh05042@gmail.com"
passwd = ""

def sendmail(image):
    to=[userid]
    imageByte=cv2.imencode(".jpeg", image)[1].tostring()
    msg = MIMEMultipart()
    imageMime=MIMEImage(imageByte)
    msg.attach(imageMime)
    msg["From"] = 'me'
    msg["To"] = to[0]
    msg["Subject"] = "움직임이 감지되었습니다!!"

    #server = smtplib.SMTP_SSL(smtp_server, portssl)
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo_or_helo_if_needed()
    server.starttls()
    server.ehlo_or_helo_if_needed()
    ret, m = server.login(userid, passwd)
    if ret != 235:
        print ("login fail")
        return
    server.sendmail(userid,userid, msg.as_string())
    server.quit()

if __name__ == "__main__":
    thresh = 16
    cam = cv2.VideoCapture(0)
    cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
    cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
    if cam.isOpened() == False:
        print ("Cam isn't opened")
        exit()
    i = [None, None, None]
    for n in range(3):
        i[n] = motion.getGrayCameraImage(cam)
    flag = False
    checkFlag = 0
    import time
    count = 0
    SMSsender = twilioSMS()
    while True:
        diff = motion.diffImage(i)
        ret,thrimg=cv2.threshold(diff, thresh, 1, cv2.THRESH_BINARY)
        maxCnt = count
        count = cv2.countNonZero(thrimg)

        #time.sleep(1)
        # if invader is checked
        # print checkFlag, count
        if (abs(maxCnt-count) > 150):
            checkFlag += 1

        if checkFlag >= 10 and flag == False:
            SMSsender.sendSMS()
            sendmail(i[2])
            flag = True
            print ("[!] Moving Detection!!")
            count = 0

        if count == 0 and flag == True:
            flag = False
            checkFlag = 0

        # process next image
        motion.updateCameraImage(cam, i)

        key = cv2.waitKey(10)
        if key == 27:
            break
