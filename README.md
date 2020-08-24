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

	
## Prepare

	Raspberry pi * 1
	Breadboard * 1
	Camera * 1
	led lights * 3
	buzzer * 1
	some jumper cable
	Cloud Server * 1
	
	
## Development Process

> **To Remote Server (x86_64 GNU/Linux 4.4.0-116-generic) (Ubuntu 16.04.4 LTS xenial)**

#### Install ssh

	sudo apt-get install openssh-server (you can change the service port in /etc/ssh/sshd_config.)
	sudo ufw allow 22 (or the port you change in previous step.)
	sudo systemctl restart ssh
		

#### Install nfs server

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


// recommend run as normal user.
* install miniconda3

	* cd ~

	* wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh

	* bash Miniconda3-latest-Linux-x86_64.sh

	// you may export path by yourself by edit ~/.bashrc.<br />
	// you can edit /etc/environment if you want to set global PATH.<br />
	* let miniconda3 auto export PATH for you.

	* source .bashrc (reload .bashrc)

	// check that if you are using the right python. 
	* which python

		// should show something like this.
		'/home/{your-normal-user}/miniconda3/bin/python'.


	* conda update conda

	* pip install --upgrade pip


// run as normal user if you install miniconda3 as normal user.
* install tensorflow

	* pip install numpy

	* pip install tensorflow

	// check that if you are correctly install those package.
	* pip list | egrep '(numpy|tensorflow)'

		// should show something like this.
			numpy        1.14.3
			tensorflow   1.8.0


	* sudo apt-get install git

	// clone it to ~/tensorflow directory.
	* cd ~

	* mkdir tensorflow

	* cd tensorflow

	* git clone https://github.com/tensorflow/models.git

	// check that if you are correctly create tensorflow's models.
	* python ~/tensorflow/models/tutorials/image/imagenet/classify_image.py

		// you should get some tags and scores.

		
----------------------------------------------------------------------

> **To Raspberry pi (armv7l GNU/Linux 4.14.34-v7+) (2017-11-29-raspbian-stretch-lite)**

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
	
* sudo vim /etc/hostname
		
	{your-host-name}
		
		
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
		
		
	* sudo reboot
	
	// check that if you are correctly setting your host name.
	* hostname -f => fqdn-name
	* hostname -s => host-name
	
	// check that if you are connecting to the WAN.
	* ping 8.8.8.8

	* install ssh
	
		* sudo apt-get install openssh-server
		
		* sudo systemctl restart ssh
		
	
	// we can login in to the remote server with this private key. (don't need to enter the password while using ssh or scp)<br />
	// run as normal user, do not run as root!<br />
	* create RSA keys and copy public key to remote server
	
		* ssh-keygen -t rsa
		
		* press enter three time for default setting (use empty passphrase)
		
		* cd ~/.ssh
		
		* ssh-copy-id -i id_rsa.pub remote-server-user@remote-server-ip -p remote-server-ssh-port (install public key to remote server [~/.ssh/authorized_keys])
		
		// you can now login in to remote server without password after typing this command.
		* ssh remote-server-user@remote-server-ip -p remote-server-ssh-port
		
	
	* install nfs client
	
		* sudo apt-get install nfs-common
		
		* sudo mkdir /mnt/nfs
		
		* sudo mkdir /mnt/nfs/IoT

		// you can first check that if you are in remote-server's export list by this command.
		* showmount -e remote-server-ip
		
		* sudo mount -t nfs remote-server-ip:/srv/nfs/IoT /mnt/nfs/IoT
		
		// check that if you are correctly connect to network file system server.
		* df -h | grep /mnt/nfs/IoT
			
			// should show something like this.
			remote-server-ip:/srv/nfs/IoT   28G  6.4G   21G  25% /mnt/nfs/IoT
		
		
		// if you want to auto mount on startup
		* sudo vim /etc/fstab
		
			remote-server-ip:/srv/nfs/IoT /mnt/nfs/IoT nfs defaults 0 0
		
		
		* sudo groupadd -g 2049 nfs
	
		// add user to nfs group
		* sudo usermod -aG nfs {your-normal-user}
		
		* logout && login (refresh the group setting)
		
		// check point
		* ls -ld /mnt/nfs/IoT
		
			drwxrwxr-x 3 root nfs 4096 Jun 12 02:31 /mnt/nfs/IoT
	
	
	// recommend run as normal user.
	* install berryconda3
	
		* cd ~
		
		* wget https://github.com/jjhelmus/berryconda/releases/download/v2.0.0/Berryconda3-2.0.0-Linux-armv7l.sh
	
		* bash Berryconda3-2.0.0-Linux-armv7l.sh

		// check that if you are using the right python. 
		* which python
			
			// should show something like this.
			'/home/{your-normal-user}/berryconda3/bin/python'
		
		* conda update conda

		* pip install --upgrade pip
	
	
	// run as normal user if you install berryconda3 as normal user.
	* install python packages for our project.
	
		* pip install numpy
		
		* pip install picamera
		
		* pip install RPi.GPIO
		
		// check that if you are correctly install those package.
		* pip list | egrep '(numpy|picamera|RPi.GPIO)'
			
			// should show something like this.
			numpy        1.14.3
			picamera     1.13
			RPi.GPIO     0.6.3
	
	
	// if you are not using 'pi' as your normal user.
	* sudo vim /etc/group
	
		add your user in group adm, sudo, video and gpio.
	
	
	// check that if your normal user is in those group.
	* groups {normal-user}
	
		// should show something like this.
		{normal-user} : {normal-user} adm sudo video gpio nfs
	
	
	* enable camera
	
		* sudo raspi-config
		
		* Interfacing Options => P1 Camera => Yes => Ok => Finish
	
	
	* mkdir ~/python_workspace
	
	* mkdir ~/python_workspace/project
	
	* cd ~/python_workspace/project
	
	// take picture and put it in /mnt/nfs/IoT.
	* [vim MyCamera.py](./python/MyCamera.py)
		
	
	// detect the switch button, execute the trigger method if the button is pressed.
	* vim PushButton.py
		
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

* create script to automatically run tensorflow. (run as normal user if you install tensorflow as normal user)
* mkdir ~/bin
* cd ~/bin
* vim triggerTensorflow
``` bash
  #!/bin/bash

  time=`date "+%Y-%m-%d_%H:%M:%S"`

  /home/{your-normal-user}/miniconda3/bin/python /home/{your-normal-user}/tensorflow/models/tutorials/image/imagenet/classify_image.py --image_file /srv/nfs/IoT/pictures/tmp.jpg > /srv/nfs/IoT/picturesInfo/${time}.txt

  mv /srv/nfs/IoT/pictures/tmp.jpg /srv/nfs/IoT/pictures/${time}.jpg
```
* chmod 770 triggerTensorflow <br/><br/>
*[Because we create our shell script in ~/bin, so we don't need to update the path. (check it with below command)]*
* echo $PATH | grep "/home/{your-normal-user}/bin"
* which triggerTensorflow
----------------------------------------------------------------------

> **To Raspberry pi**

* cd ~/python_workspace/project
* [vim TriggerRemoteServer.py](./python/TriggerRemoteServer.py) (trigger remote-server execute the script [triggerTensorflow])
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
* [vim generalGarbage](./bash/generalGarbage) <br/><br/>
// [Classify image by keywords and write the classified result in /srv/nfs/IoT/result]
* [vim Identify.py](./python/Identify.py) <br/><br/>
// [Notify us if the classified result is 'other'. I use my own mail server to send mail, you can use gmail if you want to]
* [vim SendMail.py](./python/SendMail.py) <br/><br/>
//[Let us decide the final classified result]
* [vim FetchMail.py](./python/FetchMail.py)	
* sudo chown -R root:nfs /srv/nfs/IoT <br/><br/>
//[Add this line at the bottom of the file]
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
		
