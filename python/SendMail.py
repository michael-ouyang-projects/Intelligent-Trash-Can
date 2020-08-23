import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

def send(imagePath):
  sender = 'iot@domain.com'
  receiver = '{your-email-address}'

  msg = MIMEMultipart()
  msg['Subject'] = 'Intelligent Trash Can'
  msg['From'] = sender
  msg['To'] = receiver

  text = MIMEText('Cannot classify the trash!')
  msg.attach(text)

  imageData = open(imagePath, 'rb').read()
  image = MIMEImage(imageData, name='Image')
  msg.attach(image)

  smtp = smtplib.SMTP('{smtp-server}', {smtp-port})
  smtp.ehlo()
  smtp.starttls()
  smtp.login('iot', '{iot-pwd}')
  smtp.sendmail(sender, receiver, msg.as_string())
  smtp.quit()
