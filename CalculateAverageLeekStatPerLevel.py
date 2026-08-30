import requests
import os
import json
import time
import Connection
import Utils

RANKING_TYPES = {1: 'level-50', 2: 'level-100', 3: 'level-150', 4: 'level-200', 5: 'level-250', 6: 'level-299', 7: 'leek'}

FAST_DELAY = 0.15
SLOW_DELAY = 0.6

def saveLeeksData(type, maxLeeksCount = 2000, delay = SLOW_DELAY) :
    meanLeekStats = {   "life": 0,
                        "strength": 0,
                        "wisdom": 0,
                        "agility": 0,
                        "resistance": 0,
                        "science": 0,
                        "magic": 0,
                        "tp": 0,
                        "mp": 0}
    leeksCount = 0
    leeksCountPerStat = {   "life": 0,
                            "strength": 0,
                            "wisdom": 0,
                            "agility": 0,
                            "resistance": 0,
                            "science": 0,
                            "magic": 0,
                            "tp": 0,
                            "mp": 0}
    pageNumber = 1
    for pageNumber in range(1, maxLeeksCount // 50 + 2) :
        resp = requests.get(Connection.lwAPIUrl + 'ranking/get-active/' + type + '/talent/' + str(pageNumber) + '/null', cookies=Connection.cookies)
        if resp.status_code != 200 :
            print('Request call went wrong for page ' + str(pageNumber) + ' !')
            break;

        rankingData = resp.json()["ranking"]
        for leek in rankingData :
            # Sleep for 0.6 seconds to avoid being banned by the API
            time.sleep(delay)
            leekId = str(leek["id"])
            resp = requests.get(Connection.lwAPIUrl + 'leek/get/' + leekId, cookies=Connection.cookies)
            if resp.status_code != 200 :
                print('Request call went wrong for leek ' + leekId + ' !')
                break;

            leekData = resp.json()
            
            meanLeekStats["life"] += leekData["total_life"]
            leeksCountPerStat["life"] += 1
            for stat in ("strength", "wisdom", "agility", "resistance", "science", "magic"):
                if leekData[stat] > 10:
                    meanLeekStats[stat] += leekData["total_" + stat]
                    leeksCountPerStat[stat] += 1
            meanLeekStats["tp"] += leekData["total_tp"] 
            leeksCountPerStat["tp"] += 1
            meanLeekStats["mp"] += leekData["total_mp"]
            leeksCountPerStat["mp"] += 1

            leeksCount += 1
            if leeksCount % 10 == 0 :
                # remove last printed line
                print('\033[F\033[K', end='')
                print('Processed ' + str(leeksCount) + ' leeks ! Current page: ' + str(pageNumber) + ' / ' + str(maxLeeksCount // 50 + 1))
            if leeksCount >= maxLeeksCount :
                break

    # Calculate the mean stats
    for stat in meanLeekStats :
        meanLeekStats[stat] /= leeksCountPerStat[stat]
        meanLeekStats[stat] = round(meanLeekStats[stat])

    Utils.writeInFile(folderName='LeeksData', fileName=type + '.json', data=meanLeekStats)

# Get the total number of leeks in the game
def getLeeksCount() :
    resp = requests.get(Connection.lwAPIUrl + 'leek/get-count', cookies=Connection.cookies)
    if resp.status_code != 200 :
        print('Request call went wrong !')
        return
    print('There are ' + str(resp.json()['leeks']) + ' leeks !')

# Connect to Leek Wars and get the leeks data
def start():
    getLeeksCount()
    for key, value in RANKING_TYPES.items() :
        print(str(key) + ' : ' + value)
    choice = int(input("Which ranking type would you like to get the leeks data from ? "))
    leeksCount = int(input("How many leeks would you like to get the data from ? (max 2000) "))
    fastMode = input("Would you like to enable fast mode ? (y/n) ")
    delay = FAST_DELAY if fastMode.lower() == 'y' else SLOW_DELAY
    startTime = time.time()
    saveLeeksData(RANKING_TYPES[choice], leeksCount, delay)
    print('Time taken: ' + str(time.time() - startTime) + ' seconds')

# Save the stats of a specific leek in a JSON file
def saveLeekStats():
    # print leek stats for a specific leek
    leekId = input("Enter the leek ID: ")
    resp = requests.get(Connection.lwAPIUrl + 'leek/get/' + leekId, cookies=Connection.cookies)
    if resp.status_code != 200 :
        print('Request call went wrong for leek ' + leekId + ' !')
        return

    Utils.writeInFile(folderName='LeeksData', fileName=leekId + '.json', data=resp.json())

if Connection.connectToLW() :
    start()
