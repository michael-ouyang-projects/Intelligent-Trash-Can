# Intelligent-Trash-Can

![alt text](../master/Intelligent-Trash-Can.jpg "Product Image")

## Introduction

	This is an 'Intelligent Trash Can' that can classify garbage to three groups(bottle, beveragePack and generalGarbage).

	0. press the switch button, it will trigger the camera.
	1. use camera to take the picture of garbage.
	2. send the picture to cloud server.
	3. cloud server will use tensorflow api to classify image and get some tags.
	4. cloud server will use those tags to do classification and get the result.
	5. if the result is other, it will send email(with the image) to us first. 
	6. we can classify it by ourself and return the result to cloud server by replying the email.
	7. cloud server will return the result to raspberry pi.
	8. raspberry pi will blink the corresponding led light to tell the user which trash can to throw the garbage.
	9. if the result is still 'other' after our classification, the buzzer will noise.

	
## Video

[Introduction](https://youtu.be/SRkfxMqJyuk)

[Operation](https://youtu.be/C6XysghJNQs)

	
## Requirement

	Raspberry pi * 1
	Breadboard * 1
	Camera * 1
	led lights * 3
	buzzer * 1
	some jumper cable
	Cloud Server * 1
	
	
## Development Process

> **Remote Server (x86_64 GNU/Linux 4.4.0-116-generic) (Ubuntu 16.04.4 LTS xenial)**

#### Install ssh

	sudo apt-get install openssh-server (you can change the service port in /etc/ssh/sshd_config.)
	sudo ufw allow 22 (or the port you change in previous step.)
	sudo systemctl restart ssh

#### Install nfs-server

	sudo apt-get install nfs-kernel-server nfs-common
	sudo mkdir -p /srv/nfs/IoT/code /srv/nfs/IoT/pictures /srv/nfs/IoT/picturesInfo
	sudo groupadd -g 2049 nfs
	usermod -aG nfs {your-normal-user} (add user to nfs group)
	logout && login (refresh the group setting)
	sudo chown -R root:nfs /srv/nfs/IoT
	sudo chmod -R 775 /srv/nfs/IoT
	sudo vim /etc/exports

		// servers you want to share data with. (you can separate them with blank space.)<br />
		// if your pi is after NAT, you should add insecure in the brackets in order to allow clients connect via ports that greater than 1024. (rw,sync,no_root_squash,no_subtree_check,insecure)<br /><br />
		/srv/nfs/IoT   x.x.x.x(rw,sync,no_root_squash,no_subtree_check)
	sudo ufw allow 111 2049
	sudo systemctl restart nfs-kernel-server
	sudo systemctl enable nfs-kernel-server (f you want to bring up this service when server startup)

### Install miniconda3 (Recommend run as normal user)

* cd ~
* wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
* bash Miniconda3-latest-Linux-x86_64.sh

	// you may export path by yourself by edit ~/.bashrc.<br />
	// you can edit /etc/environment if you want to set global PATH.<br />
	* let miniconda3 auto export PATH for you.

* source .bashrc (reload .bashrc) <br/>

*// [Check that if you are using the right python]*
* which python

	```
	// should show something like this.
	/home/{your-normal-user}/miniconda3/bin/python
	```

* conda update conda
* pip install --upgrade pip <br/>

### install tensorflow (Run as normal user if you install miniconda3 as normal user)
* pip install numpy tensorflow <br/>

*// [Check that if you are correctly install those package]*
* pip list | egrep '(numpy|tensorflow)'

	```
	// should show something like this.
	numpy        1.14.3
	tensorflow   1.8.0
	```

* sudo apt-get install git
* mkdir ~/tensorflow
* cd ~/tensorflow
* git clone https://github.com/tensorflow/models.git <br/>

*// [Check that if you can create tensorflow's models correctly]*
* python ~/tensorflow/models/tutorials/image/imagenet/classify_image.py
	
	```
	// you should get some tags and scores.
	```
		
----------------------------------------------------------------------

> **Raspberry pi (armv7l GNU/Linux 4.14.34-v7+) (2017-11-29-raspbian-stretch-lite)**

* sudo apt-get update
* sudo apt-get dist-upgrade
* sudo apt-get autoremove
* sudo vim /etc/hosts
	
	```
	if (you have static ip) {

		127.0.0.1       localhost
		your-static-ip  {your-fqdn-name} {your-host-name}

	} else {

		127.0.0.1       localhost
		127.0.1.1       {your-fqdn-name} {your-host-name}

	}
	```

*// [Edit Host Name]*
* sudo vim /etc/hostname <br/>

*// [Edit Network]*	
* sudo vim /etc/network/interfaces
	
		if(you want to connect to internet via wifi) {
			
			auto wlan0
			iface wlan0 inet (static || dhcp)
			wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
			
			
			* vim /etc/wpa_supplicant/wpa_supplicant.conf
			
				network={
					ssid="{AP-name}"
					psk="{AP-password}"
					priority=1 (raspberry pi will try to connect to the highest priority(largest number) AP first.)
					id_str="{AP-info}"
				}
				
			
			// sometime raspberry pi won't connect to internet via wifi after startup.<br />
			// so we can auto re-bring-up the wifi interface or restart networking service right after startup.<br />
			* vim /etc/rc.local
			
				// add one of this at file's bottom right before exit 0.
				1. ifdown wlan0 && ifup wlan0
				2. systemctl restart networking
				
			
			// you can scan the available AP using this command.
			* iwlist wlan0 scan
		
		} else {
		
			auto eth0
			iface eth0 inet (static || dhcp)
			address x.x.x.x
			netmask 255.255.255.0
			gateway x.x.x.x
			dns-nameservers x.x.x.x x.x.x.x
		
		}
		
		
* sudo reboot <br/>

*// [Check that if you are correctly setting your host name]*
* hostname -f => fqdn-name
* hostname -s => host-name <br/>

*// [check that if you are connecting to the WAN]*
* ping 8.8.8.8 <br/>

*// [Install ssh]*
* sudo apt-get install openssh-server
* sudo systemctl restart ssh <br/>	

*// [Run as normal user, do not run as root!]* <br/>
*// [Create RSA keys and copy public key to remote server]* <br/>
*// [We can login in to the remote server with this private key. (don't need to enter the password while using ssh or scp)]*
* ssh-keygen -t rsa

	```
	press enter three time for default setting (use empty passphrase)
	```
	
*// [Install public key to remote server (~/.ssh/authorized_keys)]*
* cd ~/.ssh
* ssh-copy-id -i id_rsa.pub remote-server-user@remote-server-ip -p remote-server-ssh-port <br/>

*// [You can now login in to remote server without password after typing this command]*
* ssh remote-server-user@remote-server-ip -p remote-server-ssh-port <br/>	
	
*// [Install nfs client]*
* sudo apt-get install nfs-common
* sudo mkdir =p /mnt/nfs/IoT <br/>

*// [Check that if you are in remote-server's export list]*
* showmount -e remote-server-ip	
* sudo mount -t nfs remote-server-ip:/srv/nfs/IoT /mnt/nfs/IoT
		
*// [Check that if you are correctly connect to network file system server]*
* df -h | grep /mnt/nfs/IoT

	```		
	// should show something like this.
	remote-server-ip:/srv/nfs/IoT   28G  6.4G   21G  25% /mnt/nfs/IoT
	```
		
*// [If you want to auto mount on startup]*
* sudo vim /etc/fstab

	```
	remote-server-ip:/srv/nfs/IoT /mnt/nfs/IoT nfs defaults 0 0
	```	
		
* sudo groupadd -g 2049 nfs <br/>

*// [Add user to nfs group]*
* sudo usermod -aG nfs {your-normal-user}
* logout && login (refresh the group setting)
		
*// [Check point]*
* ls -ld /mnt/nfs/IoT

	```
	drwxrwxr-x 3 root nfs 4096 Jun 12 02:31 /mnt/nfs/IoT
	```

*// [Install berryconda3 (recommend run as normal user)]*
* cd ~
* wget https://github.com/jjhelmus/berryconda/releases/download/v2.0.0/Berryconda3-2.0.0-Linux-armv7l.sh
* bash Berryconda3-2.0.0-Linux-armv7l.sh <br/>

*// [Check that if you are using the right python]*
* which python

	```
	// should show something like this.
	'/home/{your-normal-user}/berryconda3/bin/python'
	```

* conda update conda
* pip install --upgrade pip <br/>

*// [Install python packages for our project] (Run as normal user if you install berryconda3 as normal user)*
* pip install numpy picamera RPi.GPIO <br/>

*// [Check that if you are correctly install those package]*
* pip list | egrep '(numpy|picamera|RPi.GPIO)'

	```
	// should show something like this.
	numpy        1.14.3
	picamera     1.13
	RPi.GPIO     0.6.3
	```
	
*// [If you are not using 'pi' as your normal user, add your user to group adm, sudo, video and gpio]*
* sudo vim /etc/group <br/>

*// [Check that if your normal user is in those group]*
* groups {normal-user}

	``` bash
	// should show something like this.
	{normal-user} : {normal-user} adm sudo video gpio nfs
	```

*// [Enable Camera]*
* sudo raspi-config
* Interfacing Options => P1 Camera => Yes => Ok => Finish

* mkdir -p ~/python_workspace/project
* cd ~/python_workspace/project <br/>

*// [Take picture and put it in /mnt/nfs/IoT]*
* [vim MyCamera.py](./python/MyCamera.py) <br/>

*// [Detect the switch button, execute the trigger method if the button is pressed]*
* [vim PushButton.py](./python/PushButton.py)
		
    ``` python
    import RPi.GPIO as GPIO
    import MyCamera

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def trigger_camera(channel):
      print('taking picture')
      MyCamera.take_picture()

    GPIO.output(18, 1)
    GPIO.add_event_detect(23, GPIO.RISING, callback=trigger_camera, bouncetime=16000)

    message = input("Press enter to quit\n\n")
    GPIO.cleanup()
    ```
	
----------------------------------------------------------------------

> **To Remote Server**

*// [Create script to automatically run tensorflow. (run as normal user if you install tensorflow as normal user)]*
* mkdir ~/bin
* cd ~/bin
* vim triggerTensorflow

	``` bash
	#!/bin/bash

	time=`date "+%Y-%m-%d_%H:%M:%S"`

	/home/{your-normal-user}/miniconda3/bin/python /home/{your-normal-user}/tensorflow/models/tutorials/image/imagenet/classify_image.py --image_file /srv/nfs/IoT/pictures/tmp.jpg > /srv/nfs/IoT/picturesInfo/${time}.txt

	mv /srv/nfs/IoT/pictures/tmp.jpg /srv/nfs/IoT/pictures/${time}.jpg
	```

* chmod 770 triggerTensorflow <br/>

*// [Because we create our shell script in ~/bin, so we don't need to update the path. (check it with below command)]*
* echo $PATH | grep "/home/{your-normal-user}/bin"
* which triggerTensorflow

----------------------------------------------------------------------

> **To Raspberry pi**

* cd ~/python_workspace/project <br/>

*// [trigger remote-server execute the script (triggerTensorflow)]*
* [vim TriggerRemoteServer.py](./python/TriggerRemoteServer.py)
* [vim PushButton.py](./python/PushButton.py)
	
    ``` python
    import TriggerRemoteServer

    // edit method
    def trigger_camera(channel):
      print('taking picture')
      MyCamera.take_picture()
      trigger_recognition()

    def trigger_recognition():
      print('start recognition')
      TriggerRemoteServer.trigger()
      print('end recognition')
    ```

----------------------------------------------------------------------
			
> **To Remote Server**

* cd /srv/nfs/IoT/code
* [vim bottle](./bash/bottle)
* [vim beveragePack](./bash/beveragePack)	
* [vim generalGarbage](./bash/generalGarbage) <br/>

*// [Classify image by keywords and write the classified result in /srv/nfs/IoT/result]*
* [vim Identify.py](./python/Identify.py) <br/>

*// [Notify us if the classified result is 'other'. I use my own mail server to send mail, you can use gmail if you want to]*
* [vim SendMail.py](./python/SendMail.py) <br/>

*// [Let us decide the final classified result]*
* [vim FetchMail.py](./python/FetchMail.py)	
* sudo chown -R root:nfs /srv/nfs/IoT <br/>

*// [Add this line at the bottom of the file]*
* vim ~/bin/triggerTensorflow

	``` bash
	/home/michael/miniconda3/bin/python /srv/nfs/IoT/code/Identify.py /srv/nfs/IoT/picturesInfo/${time}.txt /srv/nfs/IoT/pictures/${time}.jpg
	```	
	
----------------------------------------------------------------------

> **To Raspberry pi**

* cd ~/python_workspace/project
* [vim ShowRecognizeResult.py](./python/ShowRecognizeResult.py)
* [vim PushButton.py](./python/PushButton.py)
	
    ``` python
    import ShowRecognizeResult

    GPIO.setup(26, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(5, GPIO.OUT)
    GPIO.setup(4, GPIO.OUT)

    // edit method
    def trigger_recognition():
      print('start recognition')
      TriggerRemoteServer.trigger()
      print('end recognition')
      ShowRecognizeResult.show()
    ```
