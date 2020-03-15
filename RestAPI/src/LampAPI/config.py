import os

# To do: 
# replace values with environment variables
class Config:
    def __init__(self):
        self._host = 'muntest.brightspace.com'
        self._target = 'https://blub.tech' 
        self._app_id = 'rumLdUKs14G5okboyjFkmQ' 
        self._app_key = 'UL_WoG-mxZNO_vgS0ooGQg' 

    def get_target(self):
        return os.environ['API_URL']

    def get_id(self):
        return os.environ['APP_ID']

    def get_host(self):
        return os.environ['D2L_SERVER']

    def get_key(self):
        return os.environ['APP_KEY']