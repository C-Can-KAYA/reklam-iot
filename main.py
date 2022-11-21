import cv2
from urllib.request import urlopen
import os
import urllib.request
from moviepy.editor import VideoFileClip
import json

def kayit():
    url = "https://reklamcilik.herokuapp.com/minibus/findByNumberPlate/5"
    osDosyasi = os.listdir()
    data_json = json.loads(urlopen(url).read())
    dosyaAdi = []
    for x in data_json:
        dosyaAdi.append(x["reklamId"] + '.mp4')
        if not (x["reklamId"] + '.mp4' in osDosyasi):
            urllib.request.urlretrieve(x["reklamLink"], x["reklamId"] + '.mp4')

    for a in range(len(osDosyasi)):
        if not (osDosyasi[a] == "main.py" or osDosyasi[a] == ".idea" or osDosyasi[a] == "venv"):
            try:
                if not (dosyaAdi[a] in osDosyasi):
                    os.remove(osDosyasi[a])
            except IndexError:
                os.remove(osDosyasi[a])
    return osDosyasi
def get_length(filename):
    clip = VideoFileClip(filename)
    return clip.duration
a = 1
while a == 1:
    duration = 0.0
    osDosyasi = kayit()
    if osDosyasi is not None:
        for c in range(len(osDosyasi)):
            if not (osDosyasi[c] == "main.py"):
                videoName = osDosyasi[c]
                video = cv2.VideoCapture(videoName)
                if video.isOpened():
                    print('Video başarılı bir şekilde açıldı')
                else:
                    print('Bir sorunla karşılaşıldı')
                windowName = 'Video Reproducer'
                cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
                while True:
                    ret,frame = video.read() 
                    if not ret: 
                         print("frame okunamıyor")   
                         cv2.destroyWindow(windowName)
                         break
                    reescaled_frame  = frame
                    cv2.setWindowProperty(windowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                    cv2.imshow(windowName, reescaled_frame )
                    waitKey = (cv2.waitKey(13) & 0xFF)
                    if  waitKey == ord('q'):
                         print("video kapatıldı.")
                         cv2.destroyWindow(windowName)
                         video.release()
                         break
