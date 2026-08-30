import requests
import Connection
import Utils
import time

# Connect to all accounts and register to all tournaments
def registerToAllTournaments() :
    for accountName in Connection.users.keys() :
        if Connection.connectToLW(accountName) :
            resp = requests.get(Connection.lwAPIUrl + 'farmer/get-from-token', cookies=Connection.cookies)
            if resp.status_code != 200 :
                print('Request call went wrong couldn\'t connect with ' + accountName + ' !')
                break;

            farmer = resp.json()["farmer"]
            # Register all leeks to tournament
            for leekId, leek in farmer["leeks"].items() :
                leekInfos = {"leek_id": leekId}
                resp = requests.post(Connection.lwAPIUrl + 'leek/register-tournament/', leekInfos, cookies=Connection.cookies)
                if resp.status_code != 200 :
                    print('Request call went wrong for leek ' + str(leek["name"]) + ' !')
                else :
                    print('Leek ' + str(leek["name"]) + ' registered to tournament !')

            time.sleep(0.5)

            # Register farmer to tournament
            farmerInfos = {"farmer_id": farmer["id"]}
            resp = requests.post(Connection.lwAPIUrl + 'farmer/register-tournament/', farmerInfos, cookies=Connection.cookies)
            if resp.status_code != 200 :
                print('Request call went wrong for farmer ' + str(farmer["name"]) + ' !')
            else :
                print('Farmer ' + str(farmer["name"]) + ' registered to tournament !')

            time.sleep(0.5)

            # Register all team compositions to tournament
            resp = requests.get(Connection.lwAPIUrl + 'team-composition/get-farmer-compositions', cookies=Connection.cookies)
            if resp.status_code != 200 :
                print('Request call went wrong for team compositions !')
            else :
                for compositionId in resp.json() :
                    compositionInfos = {"composition_id": compositionId}
                    resp = requests.post(Connection.lwAPIUrl + 'team/register-tournament/', compositionInfos, cookies=Connection.cookies)
                    if resp.status_code != 200 :
                        print('Request call went wrong for composition ' + str(compositionId) + ' !')
                    else :
                        print('Composition ' + str(compositionId) + ' registered to tournament !')

        time.sleep(1)

Connection.doFunctionWithAllAccounts(registerToAllTournaments)