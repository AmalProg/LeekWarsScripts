import requests
import json
import Connection
import Utils
from CalculateAverageLeekStatPerLevel import RANKING_TYPES
import BasicAPI

def transferDataToRegisters(registerName, jsonData):
    for leek in BasicAPI.getLeeks() :
        registerInfos = {"leek_id": leek["id"], "key": registerName, "value": jsonData}
        resp = requests.post(Connection.lwAPIUrl + 'leek/set-register', json=registerInfos, cookies=Connection.cookies)
        if resp.status_code != 200:
            print('Setting the register ' + registerInfos["key"] + ' went wrong !')
        else:
            print('Mean stats for register ' + registerInfos["key"] + ' transferred successfully !')

def transferMeanStatsPerLevelToRegisters():
    # Get the mean stats per level from the files
    meanStatsPerLevel = {}
    for key, value in RANKING_TYPES.items():
        meanStatsPerLevel[value] = Utils.readFromFile(folderName='LeeksData', fileName=value + '.json')

    jsonData = json.dumps(meanStatsPerLevel)
    transferDataToRegisters("MEAN_STATS_LEEKS", jsonData)

if Connection.connectToLW() :
    transferMeanStatsPerLevelToRegisters()