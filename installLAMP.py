#!/usr/bin/python
import os
//vim has been installed automatically.
os.system(“sudo apt-get update”)
os.system(“sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password ceshimima'”)
os.system(“sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password ceshimima'”)
os.system(“sudo apt install apache2 mysql-client mysql-server php libapache2-mod-php”)
os.system(“sudo apt -y install vim php-cli  php-intl php-xmlrpc php-soap php-mysql php-zip php-gd php-mbstring php-curl php-xml php-pear php-bcmath”)
os.system(“sudo service apache2 restart”)
os.system(“sudo apt install git”)
