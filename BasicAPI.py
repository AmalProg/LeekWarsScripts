import json

import requests
import Connection


farmer = None
def getFarmer() :
    global farmer
    if farmer is None :
        resp = requests.get(Connection.lwAPIUrl + 'farmer/get-from-token', cookies=Connection.cookies)
        if resp.status_code != 200 :
            print('Request call went wrong for farmer !')
            return None
        farmer = resp.json()
    return farmer

global leeks
leeks = None
def getLeeks() :
    global leeks
    if leeks is None :
        farmerData = getFarmer()
        if farmerData is None:
            return None
        leeksData = farmerData["farmer"]["leeks"]
        leeks = []
        for leekId in leeksData:
            leek = leeksData[leekId]
            leeks.append(leek)

    return leeks