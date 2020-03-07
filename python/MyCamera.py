from picamera import PiCamera
from time import sleep

camera = PiCamera()

def take_picture():
    camera.start_preview()
    sleep(3)
    imagePath = '/mnt/nfs/IoT/pictures/tmp.jpg'
    camera.capture(imagePath)
    camera.stop_preview()
