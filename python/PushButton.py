import RPi.GPIO as GPIO
import MyCamera
import TriggerRemoteServer
import ShowRecognizeResult

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def trigger_camera(channel):
  print('taking picture')
  MyCamera.take_picture()
  trigger_recognition()

def trigger_recognition():
  print('start recognition')
  TriggerRemoteServer.trigger()
  print('end recognition')
  ShowRecognizeResult.show()

GPIO.output(18, 1)
GPIO.add_event_detect(23, GPIO.RISING, callback=trigger_camera, bouncetime=16000)

message = input("Press enter to quit\n\n")
GPIO.cleanup()
