import os

def trigger():
  command = "ssh {remote-server-user}@{remote-server-ip} -p {remote-server-ssh-port} 'bash /home/{remote-server-user}/bin/triggerTensorflow'"
  os.system(command)
