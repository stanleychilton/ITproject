import os

os.system("sudo apt-get install vsftpd")

# os.system("sudo ")
os.system("sudo chmod o+r /etc/vsftpd.conf")
os.system("sudo chmod o+w /etc/vsftpd.conf")
os.system("sudo chmod o+r vsftpd.txt")
os.system("sudo chmod o+w vsftpd.txt")
newline=""
with open("vsftpd.txt","r+") as f:
    for line in f.readlines():
        newline=newline+line
f.close()
with open("/etc/vsftpd.conf", 'r+') as f1:
    f1.seek(0)
    f1.truncate()
    f1.writelines(newline)
f1.close()
os.system("sudo iptables -t filter -A INPUT -p tcp --dport 10090:10100 -j ACCEPT")
os.system("sudo useradd -d /var/www/html/moodle -M ftpuser")
os.system("sudo echo ftpuser:1234| sudo chpasswd")
os.system("sudo chmod a-w /var/www/html/moodle")
os.system("sudo ufw disable")
#os.system("sudo nano /etc/pam.d/vsftpd  #auth    required pam_shells.so")

os.system("sudo chmod o+r /etc/pam.d/vsftpd")
os.system("sudo chmod o+w /etc/pam.d/vsftpd")

newsta=""
s="pam_shells.so"
with open("/etc/pam.d/vsftpd","r+") as f2:
    for line in f2.readlines():
        if s in line :
            line="#auth   required        pam_shells.so"
            print(line)
        newsta=newsta+line
f2.close()
with open("/etc/pam.d/vsftpd", 'r+') as f3:
    f3.writelines(newsta)
f3.close()

os.system("sudo service vsftpd restart")
