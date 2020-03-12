import requests

url = requests.get('https://www.blub.tech/login')
print(url.text)

