import requests
import os
import time
import Connection

lwAPIUrl = Connection.lwAPIUrl;

"""
Get the code of the specified ai
"""
def getAiCode(ai) :
    time.sleep(0.4)
    resp = requests.get(lwAPIUrl + "ai/get/" + str(ai['id']), cookies=Connection.cookies)
    if resp.status_code == 200 :
        return resp.json()['ai']['code']
    else :
        raise Exception("Couldn't retrieve ai (id: {0}) informations".format(ai['id']))
    

"""
Create the arborescence of folders and ais
"""
def createFolderArbo(rootDir, foldersPerParentFolder, aisPerParentFolder, folderId, arboIndex = 0) :
    try :
        os.chdir(rootDir)
        for ai in aisPerParentFolder.get(folderId, []) :
            file = open(ai["name"] + ".leek", "wt")
            file.write(getAiCode(ai))
            print((" " * (arboIndex * 4)) + "🗎 Created {0}.leek (id: {1}) file".format(ai['name'], ai['id']))
    except Exception as error:
        print("An error has occured : ", error)

    for folder in foldersPerParentFolder.get(folderId, []) :
        os.chdir(rootDir)

        try :
            newDir = os.path.join(os.getcwd(), folder['name'])
            os.makedirs(newDir, exist_ok=True)
            if os.path.exists(newDir) :
                print((" " * (arboIndex * 4)) + "📁 Created {0} (id: {1}) directory".format(folder['name'], folder['id']))
                createFolderArbo(newDir, foldersPerParentFolder, aisPerParentFolder, folder['id'], arboIndex + 1)
        except OSError as error :
            print(error.strerror)


"""
Export all the file from Leek Wars
"""
def exportAI() :
    if Connection.connectToLW() :
        aisResp = requests.get(lwAPIUrl + 'ai/get-farmer-ais', cookies=Connection.cookies)
        if aisResp.status_code == 200 :
            foldersPerParentFolder = {}
            for folder in aisResp.json()['folders'] :
                parentFolder = folder['folder']
                # If this parent folder isn't yet in the dictionary
                if foldersPerParentFolder.get(parentFolder) == None :
                    foldersPerParentFolder[parentFolder] = []
                foldersPerParentFolder.get(parentFolder).append(folder)

            aisPerParentFolder = {}
            for ai in aisResp.json()['ais'] :
                parentFolder = ai['folder']
                # If this parent folder isn't yet in the dictionary
                if aisPerParentFolder.get(parentFolder) == None :
                    aisPerParentFolder[parentFolder] = []
                aisPerParentFolder.get(parentFolder).append(ai)

            createFolderArbo(os.path.join(os.getcwd(), "LeekWarsIA"), foldersPerParentFolder, aisPerParentFolder, 0, 0)
        else :
            print('La récupération des id des IA a échouée')

    else :
        print('La connection à Leek Wars a échouée')

exportAI()