import requests

url = requests.get('http://127.0.0.1:5000/login')
print(url.text)

