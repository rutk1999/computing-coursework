import json

def readJson(fileName):
    fileData = open(fileName, "r")
    fileString = fileData.read()
    fileJSON = json.loads(fileString)
    return fileJSON

def addObjectToList(fileJSON, element, field, value):
    fileJSON[element].append({field : value})
    
def addPlayer(fileJSON, playerName, playerAge):
    fileJSON["players"].append({"name" : playerName, "age" : playerAge, "matchesPlayed" : "0", "runsScored" : "0", "wicketsTaken" : "0"})    

def deletePlayer(fileJSON, playerName):
    for i in range(len(fileJSON["players"])):
        if fileJSON["players"][i]["name"] == playerName:
            del fileJSON["players"][i]

def saveFile(fileJSON):
    with open('data.txt', 'w') as outfile:
        json.dump(fileJSON, outfile)

data = readJson("resources/data.txt")
saveFile(data)


