#!/usr/bin/python
import os
#vim has been installed automatically.
os.system("sudo apt-get update")
os.system("sh install.sh")
os.system("sudo apt -y install apache2 php libapache2-mod-php")
os.system("sudo apt -y install vim php-cli  php-intl php-xmlrpc php-soap php-mysql php-zip php-gd php-mbstring php-curl php-xml php-pear php-bcmath")
os.system("sudo service apache2 restart")
os.system("sudo apt -y install git")

os.system("sudo apt -y update")
os.system("sudo apt -y install python3-pip")
os.system("pip3 install pymysql")

os.system("python3 script.py")
