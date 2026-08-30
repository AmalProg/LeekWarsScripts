import traceback
import requests
import os
import time
import datetime
import json
import random
import Connection

_localTime = datetime.datetime.now()

def startSoloFights(count) :
    return

"""
Starts {count} farmer fights
"""
def startFarmerFights(count) :
    for i in range(0, int(count)) :
        resp = requests.get(Connection.lwAPIUrl + 'garden/get-farmer-opponents', cookies=Connection.cookies)
        if resp.status_code == 200 :
            opponents = resp.json()['opponents']
            if len(opponents) == 0 :
                print('No opponents could be found')
                return
            randIndex = random.randint(0, len(opponents) - 1)
            opponent = opponents[randIndex]
            print('Starting fight n\'{0} with {1}'.format(i, opponent['name']))
            resp = requests.post(Connection.lwAPIUrl + 'garden/start-farmer-fight/', {'target_id': opponent['id']}, cookies=Connection.cookies)
            if resp.status_code == 200 :
                file = open(_localTime.strftime('%H-%M-%S') + '.txt', 'a')
                fightId = resp.json()['fight']
                file.write('|' + str(fightId))

                cantStartNewFight = True
                timeWaited = 0
                while cantStartNewFight :
                    resp = requests.get(Connection.lwAPIUrl + 'fight/get/' + str(fightId), cookies=Connection.cookies)
                    if resp.status_code == 200 :
                        queue = resp.json()['queue']
                        # Si la position dans le queue est > 10
                        queuePos = int(queue['position'])
                        if queuePos > 10 :
                            # On attend avant de relancer un combat
                            print('Waiting for {0}s to start a new fight, queue position {1}'.format(timeWaited, queuePos), end='\r')
                            time.sleep(10)
                            timeWaited += 10
                        else :
                            if timeWaited != 0 :
                                print('')
                            cantStartNewFight = False

            else :
                raise Exception('Fight n\'{0} couldn\'t be started'.format(i))
        else :
            raise Exception('Couldn\'t find opponents to start fight n\'{0} with'.format(i))

def startTeamFights(count) :
    return

def startFights() :
    if Connection.connectToLW() :
        os.chdir(os.path.join(os.getcwd(), 'StartedFights'))
        # Create a new directory of the current time
        newDirPath = os.path.join(os.getcwd(), 'fights_' + _localTime.strftime('%d-%m-%Y'))
        os.makedirs(newDirPath, exist_ok=True)
        os.chdir(newDirPath)

        fightType = input('Which fight type would you like to start (s / f / t) ? ')
        count = input('How many fights do you want to start ? ')
        try :
            match fightType :
                case 's' :
                    startSoloFights(count)
                case 'f' :
                    startFarmerFights(count)
                case 't' :
                    startTeamFights(count)
        except Exception as error :
            print(traceback.print_exc())
            print(error)
            
if __name__ == '__main__' :
    startFights()