import os

# To do: 
# replace values with environment variables
class Config:
    def get_target(self):
        return os.environ['API_URL']

    def get_id(self):
        return os.environ['APP_ID']

    def get_host(self):
        return os.environ['D2L_SERVER']

    def get_key(self):
        return os.environ['APP_KEY']