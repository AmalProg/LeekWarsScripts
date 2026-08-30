import requests
import Connection
import BasicAPI

def buyCombatPack() :
    resp = requests.post(Connection.lwAPIUrl + 'market/buy-habs', {"item_id": 265}, cookies=Connection.cookies)
    if resp.status_code == 400 :
        print('Can\'t buy combat pack !')
    elif resp.status_code == 200 :
        print('Combat pack bought successfully !')
    else :
        print('Request call went wrong for buying combat pack !')

def retrieveCombatPack() :
    resp = requests.post(Connection.lwAPIUrl + 'item/retrieve', {"template": 265, "quantity": 1}, cookies=Connection.cookies)
    if resp.status_code == 200 :
        print('Combat pack retrieved successfully !')
    else :
        print('Request call went wrong for retrieving combat pack !')

def buyAndRetrieveCombatPack() :
    buyCombatPack()
    retrieveCombatPack()

Connection.doFunctionWithAllAccounts(buyAndRetrieveCombatPack)
input('Press any key to exit...')
exit(1)