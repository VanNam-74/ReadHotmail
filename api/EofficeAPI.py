import requests
from api.HotmailAPI import HotmailAPI
from api import User

class EofficeAPI:

    API_HOST = "https://thenewmoonteam.com"
    API_LOGIN = f"{API_HOST}/public_api/user/login"
    auth = ()
    header = {}
    user = User()
    


    async def get_profile_for_id(self,id):
        self.API_GET = f"{self.API_HOST}/public_api/kdp/accounts/info/{id}"
        self.auth = (self.user._username,self.user._password)
        self.header = {
            'content-type':'application/json'
        }
        
        req = requests.get(url=self.API_GET,auth=self.auth,headers=self.header)
        
        if req.status_code == 200:
            data = req.json()
            # account_profile_list_dict = await convert_list_of_dict_account(data)
            # browser_profile_list_dict = await convert_list_of_dict_browser(data)
            # fingerprint_profile_list_dict = await convert_list_of_dict_fingerprint(data)
        else:
            data = {}
            # account_profile_list_dict = []

        return data

    def check_auth(self,username,password):

        auth = (username,password)
        headers = {
            'content-type':'application/json'
        }

        req = requests.get(url=self.API_LOGIN,auth=auth,headers=headers)

        return req
    
    
# account_profile = []  

# async def convert_list_of_dict_account(account_data):
#     hotmail_api = HotmailAPI()
#     id = account_data.get("id")
#     hotmail_data = await hotmail_api.get_hotmail_info_for_id(id)

#     access_token =  hotmail_data.get("access_token", "") if hotmail_data else ""
#     refresh_token = hotmail_data.get("refresh_token", "") if hotmail_data else ""
#     error = hotmail_data.get("error", "") if hotmail_data else ""
#     status = hotmail_data.get("status", "") if hotmail_data else ""
#     # for row in data:
#     account_profile.append(
#         {
#         "ID": account_data.get("id"),
#         "Profile_name":account_data.get("username"),
#         "Password": account_data.get("password"),
#         "Access_token": access_token,
#         "Refresh_token": refresh_token,
#         "error": error,
#         "Status": status,
#         "Browser_id": account_data.get("browser", {}).get("id"),
#         "Fingerprint_id": account_data.get("id"),
#         },
#     )
#     return account_profile


# browser_profile = []
# async def convert_list_of_dict_browser(browser_data):

#     # for row in data:
#     browser_profile.append(
#         {
#         "ID": browser_data.get("id"),
#         "Browser_type":browser_data.get("browser", {}).get("browser_type"),
#         "Proxy_type": browser_data.get("browser", {}).get("proxy_type"),
#         "Proxy_ip": browser_data.get("browser", {}).get("proxy_ip"),
#         "Proxy_port":browser_data.get("browser", {}).get("proxy_port"),
#         "Proxy_user":browser_data.get("browser", {}).get("proxy_user"),
#         "Proxy_pass":browser_data.get("browser", {}).get("proxy_pass"),
#         "Profile_name":browser_data.get("browser", {}).get("profile_name"),
#         "Fingerprint_id":"",
#         },
#     )
#     return browser_profile

# fingerprint_profile = []
# async def convert_list_of_dict_fingerprint(fingerprint_data):


#     finger_info__node = fingerprint_data.get("browser").get("finger_info")
#     # for row in data:
#     fingerprint_profile.append(
#         {
#         "ID": fingerprint_data.get("id"),
#         "Group1":finger_info__node.get("group1"),
#         "Group2": finger_info__node.get("group2"),
#         "Device1":finger_info__node.get("device1"),
#         "Device2":finger_info__node.get("device2"),
#         "Device3":finger_info__node.get("device3"),
#         "GPU":finger_info__node.get("DanaFP.webgl.GPU"),
#         "R6408":finger_info__node.get("DanaFP.webgl.R6408"),
#         "R35661":finger_info__node.get("DanaFP.webgl.R35661"),
#         "R36349":finger_info__node.get("DanaFP.webgl.R36349"),
#         "Random":finger_info__node.get("DanaFP.webgl.Random"),
#         "Browser_id":fingerprint_data.get("browser", {}).get("id"),
#         "Id_profile":fingerprint_data.get("id")
#         },
#     )
#     return fingerprint_profile