import boto3
import csv
import time
import paramiko
import requests


url = "http://www.clicker-box.com/"
client = boto3.client('ec2')
ec2 = boto3.resource('ec2')

#Creates key-pair

keypair_name = 'ec2-keypair2'


new_keypair = ec2.create_key_pair(KeyName=keypair_name)

with open('.\ec2-keypair2', 'w') as file:
    file.write(new_keypair.key_material)

print(new_keypair.key_fingerprint)

# Read number of lines in the CSV File
with open('test.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            print(row)
            userdata = {"sid": row[0], "firstname": row[1], "lastname": row[2], "email": row[3]}
            resp = requests.post( url + 'selectionsite/users.php', params=userdata)
            line_count += 1


number_of_lines = line_count - 1

#Set up an ec2 instance for each student in the class
ec2 = boto3.resource('ec2')

instances = ec2.create_instances(
    ImageId='ami-0b37e9efc396e4c38',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    KeyName='ec2-keypair2'
)

instances[0].wait_until_running()

l = []
instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
for instance in instances:
    l.append(instance.id)
    print(l)

image = ec2.Instance(l[0])
if(image.state == 'pending'):
        print("Waiting for image to be available.")
        while(image.state != 'running'):
            image = ec2.Image(l[0])
        print("Image Available to use")

print("WE ON")



# Create a list of all the active public DNS ip addresses

l = []

for i in ec2.instances.all():
    l.append(i.public_dns_name)
l = list(filter(None, l))
print(l)

time.sleep(10)
#SSH into all of the instances and install moodle on them



key = paramiko.RSAKey.from_private_key_file(r".\ec2-keypair2")
client1 = paramiko.SSHClient()
client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect/ssh to an instance

# Here 'ubuntu' is user name and 'instance_ip' is public IP of EC2
client1.connect(hostname=str(l[0]), username="ubuntu", pkey=key)

# Execute a command(cmd) after connecting/ssh to an instance
stdin, stdout, stderr = client1.exec_command("git clone https://github.com/fish258/configSite")
print("Moodle Install {} beingning Now".format(1))
time.sleep(10)
stdin, stdout, stderr = client1.exec_command("python3 configSite/installLAMP.py")
print(stdin, "\n\n", stdout.read(), "\n\n", stderr.read())
print(stdout.read())
print("Moodle Install {} finished installing".format(1))






print("SSH Done")


print("Ready to Create AMI")

lst1 = []
instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
for instance in instances:
    lst1.append(instance.id)
    print(lst1)

images = client.create_image(InstanceId=lst1[0], Name='Jacob')


lst = []
boto3conn = boto3.resource("ec2", region_name="us-west-2")
images1 = boto3conn.images.filter(Owners=['self'])
for i in images1:
    lst.append(i.image_id)

image = ec2.Image(lst[0])
if(image.state == 'pending'):
        print("Waiting for image to be available.")
        while(image.state != 'available'):
            image = ec2.Image(lst[0])
        print("Image Available to use")


print("Ready to set up Instances")

lst = []
boto3conn = boto3.resource("ec2", region_name="us-west-2")
images1 = boto3conn.images.filter(Owners=['self'])
for i in images1:
    lst.append(i.image_id)



FinalInstances = ec2.create_instances(
    ImageId=lst[0],
    MinCount=1,
    MaxCount=number_of_lines,
    InstanceType='t2.micro',
    KeyName='ec2-keypair2'
)
