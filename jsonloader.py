import json

def readJson(fileName):
    fileData = open(fileName, "r")
    fileString = fileData.read()
    fileJSON = json.loads(fileString)
    return fileJSON

def addObjectToList(fileJSON, element, field, value):
    fileJSON[element].append({field : value})
    
def addPlayer(fileJSON, playerName, playerAge):
    fileJSON["players"].append({"name" : playerName, "age" : playerAge})    

def saveFile(fileJSON):
    with open('data.txt', 'w') as outfile:
        json.dump(fileJSON, outfile)

data = readJson("data.txt")
saveFile(data)

