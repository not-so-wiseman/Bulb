import requests

url = requests.get('https://www.blub.tech/auth')
print(url.text)

