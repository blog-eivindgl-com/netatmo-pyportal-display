import adafruit_requests as requests

class AccessTokenService():
    def __init__(self, secrets):
        super().__init__()
        self._requests = requests
        self._grant_type = secrets['netatmo-granttype']
        self._client_id = secrets['netatmo-clientid']
        self._client_secret = secrets['netatmo-clientsecret']
        self._username = secrets['netatmo-username']
        self._password = secrets['netatmo-password']
        self._expires_in = 0;
        self._access_token = "";
        self._refresh_token = "";
    
    def get_access_token(self):
        if self._access_token != "":
            return self._access_token
        data = {
            "grant_type": self._grant_type, 
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "username": self._username,
            "password": self._password,
            "scope": "read_station read_thermostat"
        }
        response = self._requests.get("https://www.vg.no")
        #response = self._requests.post("https://api.netatmo.com", data=data)
        if response.status_code == 200:
            self._expires_in = response.expires_in
            self._refresh_token = response.refresh_token
            self._access_token = response.access_token
            return self._access_token