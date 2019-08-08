import os

#download moodle

os.chdir("/opt")
os.system("sudo git clone https://github.com/moodle/moodle.git")
os.chdir("/opt/moodle")
os.system("sudo git branch -a")
os.system("sudo git branch --track MOODLE_36_STABLE origin/MOODLE_36_STABLE")
os.system("sudo git checkout MOODLE_36_STABLE")
os.system("sudo cp -R /opt/moodle /var/www/html/")
os.system("sudo mkdir /var/moodledata")
os.system("sudo chown -R www-data /var/moodledata")
os.system("sudo chmod -R 777 /var/moodledata")
os.system("sudo chmod -R 0755 /var/www/html/moodle")

#write things in mysqld.cnf
os.system("sudo chmod o+w /etc/mysql/mysql.conf.d/mysqld.cnf")
x=0
newsta=""
with open("/etc/mysql/mysql.conf.d/mysqld.cnf","r+") as f:
    for line in f.readlines():
        if(line.find('default_storage_engine = innodb') == 0):
            x=1
#             print("s")
    f.seek(0)
    print(len(newsta))
    for line in f.readlines():
        if(line.find('skip-external-locking') == 0)and x==0:
            line="skip-external-locking"+"\ndefault_storage_engine = innodb\ninnodb_file_per_table = 1\ninnodb_file_format = Barracuda\n"
        newsta=newsta+line

f.close()
with open("/etc/mysql/mysql.conf.d/mysqld.cnf", 'r+') as f:
    f.writelines(newsta)
f.close()
os.system("sudo chmod o-w /etc/mysql/mysql.conf.d/mysqld.cnf")
os.system("sudo service mysql restart")

#os.system("sudo apt -y install python3-pip")
#os.system("python3 -m pip install pymysql")
#find user and password

os.system("sudo chmod o+r /etc/mysql/debian.cnf")
username=""
pwd=""
with open("/etc/mysql/debian.cnf","r") as f:
    for line in f.readlines():
        if(line.find('user') == 0):
            username=line[11:-1]
        if(line.find('password') == 0):
            pwd=line[11:-1]
f.close()

import pymysql

# 连接mysql数据库
con = pymysql.connect(host="127.0.0.1",user=username,password=pwd,port=3306)
# 创建游标 ， 利用游标来执行sql语句
cur = con.cursor()
sql1="CREATE DATABASE moodle DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 
sql2="create user 'moodledude'@'%' IDENTIFIED BY 'passwordformoodledude';"

cur.execute(sql1)
cur.execute(sql2)

cur.execute("GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,CREATE TEMPORARY TABLES,DROP,INDEX,ALTER ON moodle.* TO moodledude@localhost IDENTIFIED BY 'passwordformoodledude';")
cur.execute('quit;')

cur.close()
con.close()

os.system("sudo chmod -R 777 /var/www/html/moodle")
os.system("sudo chmod -R 0755 /var/www/html/moodle")
