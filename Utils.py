import os
import json

def writeInFile(folderName, fileName, data):
    os.makedirs(folderName, exist_ok=True)
    with open(os.path.join(folderName, fileName), 'w') as f:
        json.dump(data, f)