import imaplib
import email

def fetch():
  returnValue = False
  imap = imaplib.IMAP4_SSL('{smtp-server}')
  imap.login('iot', '{iot-pwd}')
  imap.select('inbox')

  imapStatus, data = imap.search(None,'unseen')

  if(imapStatus == 'OK'):
    mails = data[0].split()
    if mails:
      latest_mail_index = mails[-1]
      msg = imap.fetch(latest_mail_index, '(RFC822)')
      msgStr = str(msg[1][0][1])
      if(msgStr.find('From: {your-email-name} <{your-email-address}>') > -1):
        if(msgStr.find('bottle') > -1):
          result = open("/srv/nfs/IoT/result", "w")
          result.write("bottle")
          result.close()
          returnValue = True
        elif(msgStr.find('beveragePack') > -1):
          result = open("/srv/nfs/IoT/result", "w")
          result.write("beveragePack")
          result.close()
          returnValue = True
        elif(msgStr.find('generalGarbage') > -1):
          result = open("/srv/nfs/IoT/result", "w")
          result.write("generalGarbage")
          result.close()
          returnValue = True
        elif(msgStr.find('other') > -1):
          returnValue = True
  return returnValue
