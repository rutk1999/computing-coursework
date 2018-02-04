import json

def readJson(fileName):
    fileData = open(fileName, "r")
    fileString = fileData.read()
    fileJSON = json.loads(fileString)
    return fileJSON

def addObjectToList(fileJSON, element, field, value):
    fileJSON[element].append({field : value})
    
def addPlayer(fileJSON, playerName, playerAge, playerTeam):
    fileJSON["players"].append({"name" : playerName, "age" : playerAge, "matchesPlayed" : "0", "runsScored" : "0", "wicketsTaken" : "0", "team" : playerTeam})    

def deletePlayer(fileJSON, playerName):
    for i in range(len(fileJSON["players"])):
        if fileJSON["players"][i]["name"] == playerName:
            del fileJSON["players"][i]

def increaseMatchCounter(fileJSON, playerName):
    for i in range(len(fileJSON["players"])):
        if fileJSON["players"][i]["name"] == playerName:
            fileJSON["players"][i]["matchesPlayed"] = str(1 + int(fileJSON["players"][i]["matchesPlayed"]))
            pass
        
#todo do this
def addPlayerStats(fileJSON, playerName, runs, wickets):
    for i in range(len(fileJSON["players"])):
        if fileJSON["players"][i]["name"] == playerName:
            fileJSON["players"][i]["runsScored"] = str(runs + int(fileJSON["players"][i]["runsScored"]))
            fileJSON["players"][i]["wicketsTaken"] = str(wickets + int(fileJSON["players"][i]["wicketsTaken"]))

def saveFile(fileJSON):
    with open('data.json', 'w') as outfile:
        json.dump(fileJSON, outfile)

data = readJson("data.json")
