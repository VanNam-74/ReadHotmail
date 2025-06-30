
import requests
import json
class HotmailAPI:

    API_HOST = "http://192.168.1.104:8000"



    # def __init__(self, api_key: str):
    #     self.api_key = api_key
    def get_hotmail_info(self):
        self.API_GET = f"{self.API_HOST}/api/v1/profiles/"
        self.header = { 
            'content-type': 'application/json'
        }

        req = requests.get(url=self.API_GET, headers=self.header)
        if req.status_code == 200:
            data = req.json()
            print(f"result: {data}")
            return data
        else:
            print(f"Error fetching hotmail info: {req.status_code}, {req.text}")
            return []
        
        
    async def get_hotmail_info_for_id(self, profile_id):
        self.API_GET = f"{self.API_HOST}/api/v1/profiles/{profile_id}"
        self.header = { 
            'content-type': 'application/json'
        }

        req = requests.get(url=self.API_GET, headers=self.header)
        if req.status_code == 200:
            data = req.json()
            print(f"result: {data}")
            return data
        else:
            print(f"Error fetching hotmail info: {req.status_code}, {req.text}")
            return {}
    def create_hotmail_profile(self,data_create: dict):
        self.API_POST = f"{self.API_HOST}/api/v1/profiles/"
        self.header = {
            'content-type':'application/json'
        }
        self.body = {
            "profile_name": data_create.get("profile_name"),
            "password": data_create.get("password"),
            "browser_id": data_create.get("browser_id"),
            "access_token": data_create.get("access_token"),
            "refresh_token": data_create.get("refresh_token"),
            "error": data_create.get("error"),
            "status": data_create.get("status"),
            "profile_id": data_create.get("profile_id"),
        }
        req = requests.post(url=self.API_POST,headers=self.header,json=self.body)
        if req.status_code == 200:
            print("create profile hotmail success")
            return True
        else:
            print("create profile hotmail failed")
            print(f"Status code: {req.status_code}, Response: {req.text}")
            return False

    def update_token_hotmail(self,id_profile, access_token: str, refresh_token: str):
        self.API_UPDATE = f"{self.API_HOST}/api/v1/profiles/{id_profile}"
        self.header = {
            'content-type':'application/json'
        }
        self.body = {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        req = requests.put(url=self.API_UPDATE,headers=self.header,json=self.body)
        if req.status_code == 200:
            print("Update token success")
            return True
        else:
            print("Update token failed")
            print(f"Status code: {req.status_code}, Response: {req.text}")
            return False
