import csv
import boto3
import paramiko
import time
import os

ec2 = boto3.resource('ec2')

students_list = []

#Read number of lines in the CSV File
with open(r'C:\Users\Admin\PycharmProjects\EC2Creator\test.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(row)
            line_count += 1
    print(f'Processed {line_count} lines.')

number_of_lines = line_count - 1

#Set up an ec2 instance for each student in the class
ec2 = boto3.resource('ec2')

instances = ec2.create_instances(
    ImageId='ami-0b37e9efc396e4c38',
    MinCount=1,
    MaxCount=number_of_lines,
    InstanceType='t2.micro',
    KeyName='ec2-keypair2'
)
y = number_of_lines - 1

#Wait for the ec2 instances to be running

time.sleep(100)

#Create a list of all the active public DNS ip addresses

l = []

for i in ec2.instances.all():
    l.append(i.public_dns_name)
l = list(filter(None, l))

#SSH into all of the instances and install moodle on them

x = 0
while x <= number_of_lines:

    key = paramiko.RSAKey.from_private_key_file(r"C:\Users\Admin\PycharmProjects\Tester\ec2-keypair2.pem")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect/ssh to an instance
    try:
        # Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
        client.connect(hostname=str(l[x]), username="ubuntu", pkey=key)

        # Execute a command(cmd) after connecting/ssh to an instance
        stdin, stdout, stderr = client.exec_command("git clone https://github.com/fish258/configSite")
        print("now")
        time.sleep(10)
        stdin, stdout, stderr = client.exec_command("python3 configSite/installLAMP.py")
        print(stdin, "\n\n", stdout.read(), "\n\n", stderr.read())
        print("now")
        print(stdout.read())

    except():
        print("test")
    x = x + 1

#Reads the CSV file

files = os.listdir()
for x in range(0, len(files)):
    print(x+1, files[x])
while True:
    i = int(input("please choose a csv file to read: "))
    chosenfile = files[i-1]


    try:
        with open(chosenfile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    print(f'\t{row[0]} {row[1]} {row[2]} {row[3]}')
                    students_list.append([row[0], row[1], row[2], row[3]])
                    line_count += 1
            print(f'Processed {line_count} lines.')
            break
    except Exception as e:
        print(e)

print(students_list)

#Creates a list of the ip addresses of all ec2 instances

l=[]
for i in ec2.instances.all():
    l.append(i.public_ip_address)
for i in students_list:
    i.append(l[0])
    l.pop(0)

print(students_list)

#Assigns the ip addresses to a user and creates a new CSV file

with open("output.csv",'w', newline='') as resultFile:
    wr = csv.writer(resultFile, dialect='excel')
    wr.writerows(students_list)
