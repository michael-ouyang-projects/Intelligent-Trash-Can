import sys
from time import sleep

import SendMail
import FetchMail

imageInfoPath = sys.argv[1]
imagePath = sys.argv[2]

imageInfo = open(imageInfoPath, "r")
imageInfos = imageInfo.read().splitlines()
imageInfo.close()


beveragePack = open("/srv/nfs/IoT/code/beveragePack", "r")
beveragePackKeys = beveragePack.read().splitlines()
beveragePack.close()

for i in range(len(beveragePackKeys)):
  for j in range(len(imageInfos)):
    if(imageInfos[j].find(beveragePackKeys[i]) > -1):
      result = open("/srv/nfs/IoT/result", "w")
      result.write("beveragePack")
      result.close()
      sys.exit()


bottle = open("/srv/nfs/IoT/code/bottle", "r")
bottleKeys = bottle.read().splitlines()
bottle.close()

for i in range(len(bottleKeys)):
  for j in range(2):
    if(imageInfos[j].find(bottleKeys[i]) > -1):
      result = open("/srv/nfs/IoT/result", "w")
      result.write("bottle")
      result.close()
      sys.exit()


generalGarbage = open("/srv/nfs/IoT/code/generalGarbage", "r")
generalGarbageKeys = generalGarbage.read().splitlines()
generalGarbage.close()

for i in range(len(generalGarbageKeys)):
  for j in range(len(imageInfos)):
    if(imageInfos[j].find(generalGarbageKeys[i]) > -1):
      result = open("/srv/nfs/IoT/result", "w")
      result.write("generalGarbage")
      result.close()
      sys.exit()


result = open("/srv/nfs/IoT/result", "w")
result.write("other")
result.close()
SendMail.send(imagePath)
for i in range(30):
  sleep(2)
  if(FetchMail.fetch()):
    break
