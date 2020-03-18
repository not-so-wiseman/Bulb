

class User:
    def __init__(self, username, password):
        '''
            Creates a test user that can be used to make requests to D2L
        '''
        self.username = username
        self.password = password
        self.tokens = {}
        self.redirect_url = None

    def set_token(self, url):
        '''
            Recieves a url in the form: 
            https://blub.tech?x_a=afnej&x_b=bksefbkwe&x_c=hjfhfwfw.
            Where x_a is the app ID, x_b is the app key,
            and x_c is the app signature.
        '''
        self.redirect_url = url
        url = url[url.find("x_a"):]
        parameters = url.split('&')
        self.tokens["id"] = parameters[0].split('=')[1]
        self.tokens["key"] = parameters[1].split('=')[1]
        self.tokens["signature"] = parameters[2].split('=')[1]