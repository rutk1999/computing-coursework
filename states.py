import pygame
import jsonloader
import utility

pygame.init()

"""TODO - sort out batsmen individual score
--state manager--
"""
class StateManager():
    def __init__(self, window):
        self.state = None
        self.window = window

    def update(self):
        self.state.update()
    
    def render(self):
        self.state.render()

    def pollEvents(self, event):
        self.state.pollEvents(event)

    def changeState(self, state):
        self.state = state

#state base class
class State():
    def __init__(self, stateManager):
        #these are for indicating whether it should move to the next state
        self.stateManager = stateManager

    def render(self, window):
        raise NotImplementedError
    
    def update(self):
        raise NotImplementedError

    def pollEvents(self, event):
        raise NotImplementedError

#player browsing screen
class PlayerBrowseState(State):
    def __init__(self, stateManager, window):
        super(PlayerBrowseState, self).__init__(stateManager)
        self.window = window
        self.util = utility.TextRenderer(window)
        self.menuButton = utility.Button(pygame.image.load("resources/MenuButton.png").convert(), 540, 630)
        self.createPlayerButton = utility.Button(pygame.image.load("resources/AddPlayerButton.png").convert(), 1200, 630)
        self.players = []
        self.offset = 10
        self.fontSize = 24
        for i in range(len(jsonloader.data["players"])):
            player = utility.TextButton(self.window, self.offset, (i * (self.fontSize * 1.5)) + self.offset, self.fontSize)
            self.players.append(player)

    def render(self):
        self.window.fill((0, 153, 51))
        for i in range(len(self.players)):
            self.players[i].render(jsonloader.data["players"][i]["name"])
        self.menuButton.render(self.window)
        self.createPlayerButton.render(self.window)

    def update(self):
        if self.menuButton.isPressed():
            self.stateManager.changeState(MenuState(self.stateManager, self.window))
        if self.createPlayerButton.isPressed():
            self.stateManager.changeState(PlayerCreationState(self.stateManager, self.window))
        for i in range(len(self.players)):
            if self.players[i].isPressed():
                self.stateManager.changeState(PlayerStatisticsState(self.stateManager, self.window, jsonloader.data["players"][i]))
        
    def pollEvents(self, event):
        self.menuButton.pollForEvents(event)
        self.createPlayerButton.pollForEvents(event)
        for i in range(len(self.players)):
            self.players[i].pollForEvents(event)

#player stats screen
class PlayerStatisticsState(State):
    def __init__(self, stateManager, window, playerInfo):
        super(PlayerStatisticsState, self).__init__(stateManager)
        self.window = window
        self.playerInfo = playerInfo
        self.playerStats = utility.TextRenderer(self.window)
        self.playerStatisticsButton = utility.Button(pygame.image.load("resources/BrowsePlayers.png").convert(), 340, 630)
        self.menuButton = utility.Button(pygame.image.load("resources/MenuButton.png").convert(), 668, 630)

    def render(self):
        self.playerStats.setFontSize(48)
        self.playerStats.drawCenteredText(self.playerInfo["name"], 640, 100)
        self.playerStats.setFontSize(32)
        self.playerStats.drawCenteredText("Age: " + self.playerInfo["age"], 640, 200)    
        self.playerStats.drawCenteredText("Runs: " + self.playerInfo["runsScored"], 640, 250)    
        self.playerStats.drawCenteredText("Wickets: " + self.playerInfo["wicketsTaken"], 640, 300)
        self.playerStats.drawCenteredText("Team: " + self.playerInfo["team"], 640, 350)   
        self.playerStatisticsButton.render(self.window)
        self.menuButton.render(self.window)

    def update(self):
        self.window.fill((0, 153, 51))
        if self.playerStatisticsButton.isPressed():
            self.stateManager.changeState(PlayerBrowseState(self.stateManager, self.window))
        if self.menuButton.isPressed():
            self.stateManager.changeState(MenuState(self.stateManager, self.window))

    def pollEvents(self, event):
        self.playerStatisticsButton.pollForEvents(event)
        self.menuButton.pollForEvents(event)

#menu screen
class MenuState(State):
    def __init__(self, stateManager, window):
        super(MenuState, self).__init__(stateManager)
        self.window = window
        self.util = utility.TextRenderer(window)
        self.util.setFontSize(16)
        self.playerBrowseButton = utility.Button(pygame.image.load("resources/BrowsePlayers.png").convert(), 548, 230)
        self.createMatchButton = utility.Button(pygame.image.load("resources/CreateMatchButton.png").convert(), 548, 400)
        self.titleText = utility.Button(pygame.image.load("resources/TitleText.png").convert_alpha(), 478, 50)

    def render(self):
        self.window.fill((0, 153, 51))
        self.playerBrowseButton.render(self.window)  
        self.createMatchButton.render(self.window)
        self.titleText.render(self.window)

    def update(self):
        if self.playerBrowseButton.isPressed():
            self.stateManager.changeState(PlayerBrowseState(self.stateManager, self.window))
        if self.createMatchButton.isPressed():
            self.stateManager.changeState(MatchCreationState(self.stateManager, self.window))

    def pollEvents(self, event):
        self.playerBrowseButton.pollForEvents(event)     
        self.createMatchButton.pollForEvents(event)

#player creation state
class PlayerCreationState(State):
    def __init__(self, stateManager, window):
        super(PlayerCreationState, self).__init__(stateManager)
        self.window = window
        self.text = utility.TextRenderer(window)
        self.inputBox = utility.TextInput(window, 510, 200, 24)
        self.addPlayerButton = utility.Button(pygame.image.load("resources/AddPlayerButton.png").convert(), 608, 630)
        self.playerData = ''
        self.playerName = ''
        self.playerAge = ''
        
    def render(self):
        self.window.fill((0, 153, 51))
        self.text.setFontSize(48)
        self.text.drawCenteredText("Add a Player", 640, 100)
        self.text.setFontSize(24)
        self.text.drawCenteredText("To add a player, enter the player name followed by a ':', then enter the age and team.", 640, 560)
        self.text.drawCenteredText("An example is 'Alastair Cook:30 England'", 640, 600)
        self.addPlayerButton.render(self.window)
        self.inputBox.render()
    
    def update(self):
        if self.addPlayerButton.isPressed():
            self.playerData = self.inputBox.getText().split(":")
            self.playerName = self.playerData[0]
            self.playerInfo = self.playerData[1].split(" ")
            self.playerAge = self.playerInfo[0]
            self.playerTeam = self.playerInfo[1]
            jsonloader.addPlayer(jsonloader.data, self.playerName, self.playerAge, self.playerTeam)
            self.stateManager.changeState(PlayerBrowseState(self.stateManager, self.window))
            jsonloader.saveFile(jsonloader.data)
            
    def pollEvents(self, event):
        #self.inputBox.update(event)
        self.addPlayerButton.pollForEvents(event)
        self.inputBox.pollForEvents(event)

#creating the match state
##TODO fix this
class MatchCreationState(State):
    def __init__(self, stateManager, window):
        super(MatchCreationState, self).__init__(stateManager)
        self.window = window
        self.text = utility.TextRenderer(window)
        #get the teams from the json file
        self.teams = jsonloader.data["teams"]
        #list which will loop through all of the players and find valid teams to display
        self.validTeams = []
        self.teams = []
        #checks to see the valid teams from the collection
        for x in range(len(jsonloader.data["players"])):
            for y in range(len(jsonloader.data["teams"])):
                if jsonloader.data["players"][x]["team"] == jsonloader.data["teams"][y]["teamName"]:
                    if jsonloader.data["teams"][y]["teamName"] in self.validTeams:
                        pass
                    else:
                        self.validTeams.append(jsonloader.data["players"][x]["team"])
        self.teamOne = ""
        self.teamTwo = ""
        self.offset = 0
        self.teamOneButton = utility.TextButton(self.window, 620, 450, 24)
        self.teamTwoButton = utility.TextButton(self.window, 660, 450, 24)
        self.canChangeState = False

    def render(self):
        self.window.fill((0, 153, 51))
        self.text.setFontSize(48)
        self.text.drawCenteredText("Create a match", 640, 100)
        self.text.drawCenteredText(self.teamOne + " vs " + self.teamTwo, 640, 300)
        self.text.setFontSize(24)
        for team in self.validTeams:
            if self.validTeams.index(team) == self.offset:
                self.text.drawCenteredText("* " + team, 200, 600 + (self.validTeams.index(team) * 30))
            else:
                self.text.drawCenteredText(team, 200, 600 + (self.validTeams.index(team) * 30))
        #if both teams are selected then ask which team is batting/bowling
        if self.teamOne != "" and self.teamTwo != "":
            self.text.drawCenteredText("Which team is batting first?", 640, 400)
            self.teamOneButton.render("1")
            self.teamTwoButton.render("2")
            self.canChangeState = True          

    def update(self):
        if self.canChangeState == True:
            if self.teamOneButton.isPressed():
                self.stateManager.changeState(MatchState(self.stateManager, self.window, self.teamOne, self.teamTwo, self.teamOne))
            elif self.teamTwoButton.isPressed():
                 self.stateManager.changeState(MatchState(self.stateManager, self.window, self.teamOne, self.teamTwo, self.teamTwo))

    def pollEvents(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if(self.offset < len(self.validTeams) - 1):
                    self.offset += 1
                else:
                    self.offset = len(self.validTeams) - 1
                print(self.offset)
            elif event.key == pygame.K_UP:
                if(self.offset > 0):
                    self.offset -= 1
                else:
                    self.offset = 0
                print(self.offset)
            if event.key == pygame.K_RETURN:
                print("You selected: " + self.validTeams[self.offset])
                if(self.teamOne == ''):
                    self.teamOne = self.validTeams[self.offset]
                elif(self.teamTwo == ''):
                    self.teamTwo = self.validTeams[self.offset]
        self.teamOneButton.pollForEvents(event)
        self.teamTwoButton.pollForEvents(event)

#----TEST----
def printList(l):
    print(str(l))
#------------

#-------TODO: FIX DUPLICATE BOWLER WICKETS------------#
class MatchState(State):
    def __init__(self, stateManager, window, teamOne, teamTwo, battingFirst):
        super(MatchState, self).__init__(stateManager)
        #constructor & utility stuff
        self.stateManager = stateManager
        self.window = window
        self.text = utility.TextRenderer(window)
        buttonFiles = ["run1.png", "run2.png", "run3.png", "run4.png", "run5.png", "run6.png", "wicket1.png", "wicket2.png", "dot.png", "wide.png", "AddPlayerButton.png"]
        self.buttons = []
        offset = 50
        spacing = 110
        for i in range(len(buttonFiles)):
            self.buttons.append(utility.Button(pygame.image.load("resources/" + buttonFiles[i]).convert(), offset + (i * spacing), 640))

        #important variables
        self.scoreThisBall = 0
        self.score = 0
        self.innings = 1
        self.target = 0
        self.wicketTaken = 0
        self.totalWickets = 0
        self.balls = 0
        self.totalBalls = 0
        self.ballsThisOver = 0
        self.overs = 0
        self.maxOvers = 1
        self.facingBatsman = 0
        self.nonFacingBatsman = 1
        self.askWicketTaker = False
        self.offset = 0

        #data to save at the end of the match - gets passed on to next state to save the stats for the match
        self.wicketTakers = []
        self.runScorers = []
        
        #team stuff
        self.teamOne = teamOne
        self.teamTwo = teamTwo
        self.battingFirst = battingFirst
        
        #holds teams involved
        self.teams = []
        self.battingPlayerNames = []
        self.bowlingPlayerNames = []
        
        #add order of teams batting first in list and add players to list
        if self.teamOne == self.battingFirst:
            self.teams.append(self.teamOne)
            self.teams.append(self.teamTwo)
            self.addPlayers(self.teamOne, self.battingPlayerNames)
            self.addPlayers(self.teamTwo, self.bowlingPlayerNames)
        else:
            self.teams.append(self.teamTwo)
            self.teams.append(self.teamOne)
            self.addPlayers(self.teamTwo, self.battingPlayerNames)
            self.addPlayers(self.teamOne, self.bowlingPlayerNames)

        #holds current batters and their scores
        self.currentBatting = [[self.battingPlayerNames[0], 0], [self.battingPlayerNames[1], 0]]
        #next batter variable
        self.nextBatter = 2
            
        #------FOR TESTING-------#
        printList(self.currentBatting)
        printList(self.bowlingPlayerNames)
        self.found = False
        print(self.teams[0])
        
    def addPlayers(self, team, teamList):
        for i in range(len(jsonloader.data["players"])):
            if jsonloader.data["players"][i]["team"] == team:
                teamList.append(jsonloader.data["players"][i]["name"])

    def checkForWicket(self):
        if self.wicketTaken > 0 and self.totalWickets < 10:
            self.runScorers.append(self.currentBatting[self.wicketTaken - 1])
            self.currentBatting[self.wicketTaken - 1] = [self.battingPlayerNames[self.nextBatter], 0]
            self.nextBatter += 1
            self.totalWickets += 1
            self.askWicketTaker = True
            self.wicketTaken = 0
            print(self.runScorers)
        if self.wicketTaken > 0 and self.totalWickets == 9 and self.innings == 1:
            self.changeInnings()
                
    def updateRuns(self):
        self.score += self.scoreThisBall
        #change batsman score only if it not a wide/bye
        if self.balls == 1:
            self.currentBatting[self.facingBatsman][1] += self.scoreThisBall
        self.totalBalls += self.balls
        self.overs = self.totalBalls//6
        self.ballsThisOver = self.totalBalls % 6
        #if it is not a wide then only change facing batsman
        if(self.scoreThisBall % 2 == 1) and self.balls == 1:
            temp = self.facingBatsman
            self.facingBatsman = self.nonFacingBatsman
            self.nonFacingBatsman = temp
        self.balls = 0
        self.scoreThisBall = 0
        if self.overs == self.maxOvers and self.innings == 1:
            self.addBatsmenScores()
            self.changeInnings()
        if self.innings == 2:
            self.checkWin()

    def askForName(self):
        self.window.fill((0, 153, 51))
        self.text.setFontSize(48)
        self.text.drawCenteredText("Who got the wicket?", 640, 60)
        self.text.setFontSize(32)
        for i in range(len(self.bowlingPlayerNames)):
            if self.offset == i:
                self.text.drawCenteredText(self.bowlingPlayerNames[i-1] + " * ", 640, 140 + (i * 50))
            else:
                self.text.drawCenteredText(self.bowlingPlayerNames[i-1], 640, 140 + (i * 50))

    #changes the innings
    def changeInnings(self):
        print("ada")
        temp = self.battingPlayerNames
        self.battingPlayerNames = self.bowlingPlayerNames
        self.bowlingPlayerNames = temp
        self.target = self.score + 1
        self.currentBatting = [[self.battingPlayerNames[0], 0], [self.battingPlayerNames[1], 0]]
        self.overs = 0
        self.score = 0
        self.totalBalls = 0
        self.innings = 2

    def checkWin(self):
        if self.overs == self.maxOvers and self.innings == 2:
            if self.score == self.target - 1:
                print("The match is a draw")
            elif self.score < self.target - 1:
                print(self.teams[0] + " wins")
                self.stateManager.changeState(MatchWinState(self.stateManager, self.window, self.teams[0], self.wicketTakers, self.runScorers))
            elif self.score >= self.target:
                print(self.teams[1] + " wins")
                self.stateManager.changeState(MatchWinState(self.stateManager, self.window, self.teams[1], self.wicketTakers, self.runScorers))
            self.addBatsmenScores()
        elif self.score >= self.target and self.innings == 2:
            print(self.teams[1] + " wins")
            self.addBatsmenScores()
            self.stateManager.changeState(MatchWinState(self.stateManager, self.window, self.teams[1], self.wicketTakers, self.runScorers))

    def addBatsmenScores(self):
        self.runScorers.append(self.currentBatting[0])
        self.runScorers.append(self.currentBatting[1])
        printList(self.runScorers)
          
    def render(self):
        #while a wicket has not fallen
        if self.askWicketTaker == True:
            self.askForName()
        else:
            #basic window stuff
            self.window.fill((0, 153, 51))
            
            #drawing some needed text on the screen
            self.text.setFontSize(36)
            self.text.drawCenteredText(self.teamOne + " vs " + self.teamTwo, 640, 40)
            self.text.setFontSize(48)
            self.text.drawCenteredText("Score: " + str(self.score) + "/" + str(self.totalWickets), 640, 110)
            self.text.setFontSize(24)
            self.text.drawCenteredText("Runs this ball: " + str(self.scoreThisBall), 100, 35)
            self.text.drawCenteredText("Over: " + str(self.overs) + "." + str(self.ballsThisOver), 1200, 35)

            #current batter text
            self.text.setFontSize(48)
            self.text.drawCenteredText(str(self.currentBatting[0][0]) + "   " + str(self.currentBatting[0][1]), 640, 270)
            self.text.drawCenteredText(str(self.currentBatting[1][0]) + "   " + str(self.currentBatting[1][1]), 640, 370)

            #second innings stuff
            if self.innings == 2:
                self.text.drawCenteredText("Target: " + str(self.target), 100, 110)

            #place asterisk on the side of the facing batsman
            if self.facingBatsman == 0:
                self.text.drawCenteredText("*", 400, 270)
            else:
                self.text.drawCenteredText("*", 400, 370)

            #drawing buttons
            for i in range(len(self.buttons)):
                self.buttons[i].render(self.window)

    def update(self):
        print(self.found)
        if self.buttons[0].isPressed():
            self.scoreThisBall = 1
            self.balls = 1
            self.wicketTaken = 0
        elif self.buttons[1].isPressed():
            self.scoreThisBall = 2
            self.balls = 1
            self.wicketTaken = 0
        elif self.buttons[2].isPressed():
            self.scoreThisBall = 3
            self.balls = 1
            self.wicketTaken = 0
        elif self.buttons[3].isPressed():
            self.scoreThisBall = 4
            self.balls = 1
            self.wicketTaken = 0
        elif self.buttons[4].isPressed():
            self.scoreThisBall = 5
            self.balls = 1
            self.wicketTaken = 0
        elif self.buttons[5].isPressed():
            self.scoreThisBall = 6
            self.balls = 1
            self.wicketTaken = 0
        elif self.buttons[6].isPressed():
            self.wicketTaken = 1
            self.batsmanOut = 1
            self.balls = 1
        elif self.buttons[7].isPressed():
            self.wicketTaken = 2
            self.batsmanOut = 2
            self.balls = 1
        elif self.buttons[8].isPressed():
            self.balls = 1
            self.wicketTaken = 0
        elif self.buttons[9].isPressed():
            self.scoreThisBall = 1
            self.wicketTaken = 0
            self.balls = 0
        if self.buttons[10].isPressed():
            self.updateRuns()
            self.checkForWicket()
    
    def pollEvents(self, event):
        for i in range(len(self.buttons)):
            self.buttons[i].pollForEvents(event)

        #to handle when the user selects a user
        if event.type == pygame.KEYDOWN:
            if self.askWicketTaker == True:
                if event.key == pygame.K_DOWN:
                    if(self.offset < 10):
                        self.offset += 1
                    else:
                        self.offset = 10
                    print(self.offset)
                elif event.key == pygame.K_UP:
                    if(self.offset > 0):
                        self.offset -= 1
                    else:
                        self.offset = 0
                    print(self.offset)
                if event.key == pygame.K_RETURN:
                    print("You selected: " + self.bowlingPlayerNames[self.offset-1])
                    #checking for duplicate
                    #var to check if soemthing is found
                    if len(self.wicketTakers) > 0:   
                        for i in range(len(self.wicketTakers)):
                            if self.wicketTakers[i][0] == self.bowlingPlayerNames[self.offset-1]:
                                self.wicketTakers[i][1] += 1
                            #todo fix this
                            if self.found == False:
                                self.wicketTakers.append([self.bowlingPlayerNames[self.offset-1], 1])
                    else:
                        print("True")
                        self.wicketTakers.append([self.bowlingPlayerNames[self.offset-1], 1])
                    printList(self.wicketTakers)
                    self.askWicketTaker = False
            else:
                if event.key == pygame.K_1:
                    self.facingBatsman = 0
                    self.nonFacingBatsman = 1
                elif event.key == pygame.K_2:
                    self.facingBatsman = 1
                    self.nonFacingBatsman = 0

class MatchWinState(State):
    def __init__(self, stateManager, window, winningTeam, wicketTakers, runScorers):
        self.stateManager = stateManager
        self.window = window
        self.winningTeam = winningTeam
        self.text = utility.TextRenderer(window)
        self.wicketTakers = wicketTakers
        self.runScorers = runScorers
        printList(wicketTakers)
        printList(runScorers)

    def render(self):
        self.window.fill((0, 153, 51))
        self.text.setFontSize(48)
        self.text.drawCenteredText(self.winningTeam + " has won the match", 640, 100)
        self.text.setFontSize(36)
        self.text.drawCenteredText("Run Scorers: ", 320, 170)
        self.text.setFontSize(24)
        for i in range(len(self.runScorers)):
            self.text.drawCenteredText(str(self.runScorers[i][0]) + ": " + str(self.runScorers[i][1]), 320, 240 + (i * 30))

    def update(self):
        pass

    def pollEvents(self, event):
        pass
        
        
