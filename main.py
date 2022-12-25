import cv2
from urllib.request import urlopen
import os
import urllib.request
import requests
import json
def sizeDosya():
    sayac=0
    dosyalar = os.listdir()
    for a in range(len(dosyalar)):
        if (dosyalar[a].find('.mp4') >= 0):
            sayac=sayac+1
    return sayac
            
def kayit():
    osDosyasi = os.listdir()
    url = "http://localhost:8080/minibus/findByNumberPlate/1"
    data_json = json.loads(urlopen(url).read())
    kontrol = data_json[0]
    if (sizeDosya()<=0 or kontrol['checked']==True):
        kontrolVideo=0
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
                    try:
                        fileLocation=os.getcwd()
                        fileLocation=fileLocation.replace("\\", "/")
                        os.chmod(fileLocation, 0o777)
                        os.remove(osDosyasi[a])
                    except PermissionError:
                        kontrolVideo=1
        if(kontrolVideo==0):
            data = {'checked':'false','plaka': '1'}
            requests.post("http://localhost:8080/minibus/guncel", json=data)
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
