import requests
import boto3
ec2 = boto3.resource('ec2')

l = []

for i in ec2.instances.all():
     l.append([i.public_ip_address, i.instance_id])
     l = list(filter(None, l))
     


for j in l:
     userdata = {"url": j[0], "id":j[1]}
     resp = requests.post('http://www.clicker-box.com/selectionsite/instances.php', params=userdata)
     print(resp)
