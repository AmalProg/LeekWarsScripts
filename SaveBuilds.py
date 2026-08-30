import requests
import os
import json
import time
import datetime
import Connection

def saveLeekBuild(leekId) :
    resp = requests.get(Connection.lwAPIUrl + 'leek/get/' + leekId, cookies=Connection.cookies)
    if resp.status_code == 200 :
        leek = resp.json()
        file = open(leek['name'] + '.json', 'w')
        file.write(json.dumps(leek))
    else :
        print('Request to get leek {0} went wrong'.format(leekId))


def saveAllBuilds() :
    if Connection.connectToLW() :
        resp = requests.get(Connection.lwAPIUrl + 'farmer/get-from-token', cookies=Connection.cookies)
        if resp.status_code == 200 :
            farmer = resp.json()['farmer']
            leeks = farmer['leeks']
            os.chdir(os.path.join(os.getcwd(), 'SavedBuilds'))
            # Create a new directory of the current time
            localTime = datetime.datetime.now()
            newDirPath = os.path.join(os.getcwd(), 'build_' + localTime.strftime('%d-%m-%Y_%H-%M-%S'))
            os.makedirs(newDirPath)
            os.chdir(newDirPath)
            for leekId in leeks :
                saveLeekBuild(leekId)
        else :
            print('Request to get farmer went wrong')

saveAllBuilds()