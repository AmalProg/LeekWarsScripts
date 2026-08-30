import requests
import Connection
import Utils


if Connection.connectToLW() :
    resp = requests.get(Connection.lwAPIUrl + 'weapon/get-templates', cookies=Connection.cookies)
    if resp.status_code != 200 :
        print('Request call went wrong !')
        exit()
    Utils.writeInFile(folderName='GameData', fileName='weaponTemplate.json', data=resp.json())