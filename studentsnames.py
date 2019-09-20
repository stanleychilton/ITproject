import requests
userdata = {"firstname": "John", "lastname": "Doe", "email": "joedoe@live.com"}
resp = requests.post('http://www.clicker-box.com/selectionsite/users.php', params=userdata)
print(resp)