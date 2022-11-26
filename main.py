import cv2
from urllib.request import urlopen
import os
import urllib.request
import json
import datetime
def sizeDosya():
    sayac=0
    dosyalar = os.listdir()
    for a in range(len(dosyalar)):
        if (dosyalar[a].find('.mp4') >= 0):
            sayac=sayac+1
    return sayac
            
def kayit():
    osDosyasi = os.listdir()
    now = datetime.datetime.now().time()
    if (sizeDosya()<=0 or (now.hour == 12 and now.minute==25)):
        url = "https://reklamcilik.herokuapp.com/minibus/findByNumberPlate/5"
        data_json = json.loads(urlopen(url).read())
        dosyaAdi = []
        for x in data_json:
            dosyaAdi.append(x["reklamId"] + '.mp4')
            if not (x["reklamId"] + '.mp4' in osDosyasi):
                urllib.request.urlretrieve(x["reklamLink"], x["reklamId"] + '.mp4')
        for a in range(len(osDosyasi)):
            if (osDosyasi[a].find('.mp4') >= 0):
                try:
                    if not (dosyaAdi[a] in osDosyasi):
                        os.remove(osDosyasi[a])
                except IndexError:
                    os.remove(osDosyasi[a])
    return osDosyasi

while True:   
    osDosyasi = kayit()
    if osDosyasi is not None:
        for c in range(len(osDosyasi)):
            if (osDosyasi[c].find('.mp4') >= 0):
                videoName = osDosyasi[c]
                video = cv2.VideoCapture(videoName)
                if video.isOpened():
                    print('Video başarılı bir şekilde açıldı')
                else:
                    print('Bir sorunla karşılaşıldı')
                windowName = 'Video Reproducer'
                
                while True:
                    cv2.namedWindow(windowName, cv2.WND_PROP_FULLSCREEN)
                    ret,frame = video.read() 
                    if not ret: 
                         print("frame okunamıyor")   
                         cv2.destroyWindow(windowName)
                         break
                    rescaled_frame  = frame
                    cv2.setWindowProperty(windowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_AUTOSIZE)
                    cv2.resizeWindow(windowName, 3840,2160)
                    cv2.imshow(windowName, rescaled_frame )
                    waitKey = (cv2.waitKey(1) & 0xFF)
                    if  waitKey == ord('q'):
                         print("video kapatıldı.")
                         cv2.destroyWindow(windowName)
                         video.release()
                         break
