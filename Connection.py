import requests
import getpass
import os
from dotenv import dotenv_values

lwAPIUrl = 'https://leekwars.com/api/'

users = {
    "Amal": {
        "login": "Amal",
        "password": "PASSWORD_AMAL"
    },
    "Eautaku": {
        "login": "Eautaku",
        "password": "PASSWORD_EAUTAKU"
    },
    "Unlucky": {
        "login": "Unlucky",
        "password": "PASSWORD_UNLUCKY"
    },
    "HolyGrail": {
        "login": "HolyGrail",
        "password": "PASSWORD_HOLYGRAIL"
    },
    "Demi": {
        "login": "Demi",
        "password": "PASSWORD_DEMI"
    }
}

"""
Start a connection to Leek Wars API
"""
def connectToLW(accountName="Amal") :
    config = dotenv_values(".env")

    login = users[accountName]["login"]
    password = config[users[accountName]["password"]]
    return tryToConnectToLW(login, password)


"""
Connect to Leek Wars and keep the cookies needed for other API calls
"""
def tryToConnectToLW(login, password) :
    loginData = {'login': login, 'password': password}
    loginResp = requests.post(lwAPIUrl + 'farmer/login-token/', loginData)
    if loginResp.status_code == 200 :
        global cookies
        cookies = loginResp.cookies
        return True
    else :
        print('La connection à Leek Wars a échouée')
        return False

if __name__ == '__main__' :
    connectToLW()