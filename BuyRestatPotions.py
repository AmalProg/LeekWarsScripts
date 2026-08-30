import requests
import Connection

def buyRestatPotions(count) :
    restatPotionInfos = {'item_id': 49, 'quantity': count}
    resp = requests.post(Connection.lwAPIUrl + 'market/buy-habs-quantity', restatPotionInfos, cookies=Connection.cookies)
    if resp.status_code != 200 :
        print('Request call went wrong !')
        return
    if resp.status_code == 200 :
        print('Bought ' + str(count) + ' restat potions !')
        return

if Connection.connectToLW() :
    count = int(input("How many potions would you like to buy ? "))
    buyRestatPotions(count)