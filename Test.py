import requests
import Connection
import Utils


if Connection.connectToLW() :
    resp = requests.get(Connection.lwAPIUrl + 'farmer/get-from-token', cookies=Connection.cookies)
    if resp.status_code != 200 :
        print('Request call went wrong !')
        exit()
    Utils.writeInFile(folderName='GameData', fileName='farmer.json', data=resp.json())