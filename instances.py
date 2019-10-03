import requests
userdata = {"url": "www.instance4.com", "id": instance_id}
resp = requests.post('http://www.clicker-box.com/selectionsite/instances.php', params=userdata)
print(resp)