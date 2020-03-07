import RPi.GPIO as GPIO
from time import sleep

def show():
    result = open("/mnt/nfs/IoT/result", "r")
    imageResult = result.read()
    result.close()

    if(imageResult.find('bottle') > -1):
      print('bottle')
      GPIO.output(26, 1)
      sleep(5)
    elif(imageResult.find('beveragePack') > -1):
      print('beveragePack')
      GPIO.output(16, 1)
      sleep(5)
    elif(imageResult.find('generalGarbage') > -1):
      print('generalGarbage')
      GPIO.output(5, 1)
      sleep(5)
    else:
      print('other')
      for i in range(5):
        GPIO.output(4, 1)
        sleep(0.1)
        GPIO.output(4, 0)
        sleep(0.9)

    GPIO.output(26, 0)
    GPIO.output(16, 0)
    GPIO.output(5, 0)
    GPIO.output(4, 0)
    GPIO.cleanup()
