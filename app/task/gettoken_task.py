
import requests
from fastapi.responses import JSONResponse, HTMLResponse
from models.account import Account
from api.HotmailAPI import HotmailAPI

account_model = Account()
hotmailAPI = HotmailAPI()
action_array = []

async def gettoken_profile_task(request):
    

    data = await request.json()
    profileCount = data.get('profileCount')
    print("Profile Count:", profileCount)
    data_account = account_model.readAccount()
    print("Data Account:", data_account)

    result = checkTokenInAccount(data_account)

    print("Result:", result)
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     futures = [executor.submit(checkTokenInAccount, data_hotmail_local) for i in range(profileCount)]
    #     for future in concurrent.futures.as_completed(futures):
    #         action_array.append(future.result())

    # print("Action array:", action_array)
    return JSONResponse(
        content={
            "status_code": 200,
            "data": result,
        }
    )
    # return jsonify(
    #     {
    #         'action_array': result,    
    #     }
    # )



def checkTokenInAccount(data_hotmail_local):

    if data_hotmail_local:
        position = 0
        for row in data_hotmail_local:
            access_token = row['Access_token']
            refresh_token = row['Refresh_token']
            status = row['Status']
            id_profile = row['ID']
            if access_token and refresh_token and status.lower() == 'completed':
                action_array.append({
                    'position': position,
                    'ID': "",
                    'action': '',
                })
            else:
                action_array.append({
                    'position': position,
                    'ID': id_profile,
                    'action': 'start',
                })
            position += 1

        return action_array
    else:
        action_array.append({
            'position': 0,
            'ID': "",
            'action': "",
        })

        return action_array    