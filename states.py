import pygame
import jsonloader
import utility

pygame.init()

##TODO - sort out batsmen individual score
##
#state manager
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
            self.stateManager.changeState(MatchState(self.stateManager, self.window))

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
        self.text.drawCenteredText("To add a player, enter the player name followed by a ':', then enter the age.", 640, 560)
        self.text.drawCenteredText("An example is 'Alastair Cook: 30'", 640, 600)
        self.addPlayerButton.render(self.window)
        self.inputBox.render()
    
    def update(self):
        if self.addPlayerButton.isPressed():
            self.playerData = self.inputBox.getText().split(":")
            self.playerName = self.playerData[0]
            self.playerAge = self.playerData[1].strip()
            jsonloader.addPlayer(jsonloader.data, self.playerName, self.playerAge)
            self.stateManager.changeState(PlayerBrowseState(self.stateManager, self.window))
            
    def pollEvents(self, event):
        #self.inputBox.update(event)
        self.addPlayerButton.pollForEvents(event)
        self.inputBox.pollForEvents(event)

class MatchState(State):
    def __init__(self, stateManager, window):
        super(MatchState, self).__init__(stateManager)
        self.window = window
        buttonFiles = ["run1.png", "run2.png", "run3.png", "run4.png", "run5.png", "run6.png", "wicket.png", "dot.png", "AddPlayerButton.png"]
        self.buttons = []
        offset = 100
        spacing = 120
        for i in range(len(buttonFiles)):
            self.buttons.append(utility.Button(pygame.image.load("resources/" + buttonFiles[i]).convert(), offset + (i * spacing), 630)) 
        self.text = utility.TextRenderer(window)
        self.scoreThisBall = 0
        self.score = 0
        self.wicketTaken = 0
        self.totalWickets = 0
        self.balls = 0
        self.totalBalls = 0
        self.ballsThisOver = 0
        self.overs = 0
        self.teamNames = []
        self.allBatsmenScores = [0, 0]
        self.currentBatsmenScores = [0, 0]
        self.facingBatsman = 0
        self.nonFacingBatsman = 1
        for i in range(len(jsonloader.data["players"])):
            self.teamNames.append(jsonloader.data["players"][i]["name"])

    def render(self):
        self.window.fill((0, 153, 51))
        #banner for score
        pygame.draw.rect(self.window, (80, 80, 80), (0, 20, 1280, 60))
        #banner for scorecard
        pygame.draw.rect(self.window, (22, 160, 68), (5, 90, 600, 500))
        for i in range(len(self.buttons)):
            self.buttons[i].render(self.window)
        self.text.setFontSize(48)
        self.text.drawCenteredText("Score: " + str(self.score) + "/" + str(self.totalWickets), 640, 50)
        self.text.setFontSize(24)
        self.text.drawCenteredText("Runs this ball: " + str(self.scoreThisBall), 100, 50)
        self.text.drawCenteredText("Over: " + str(self.overs) + "." + str(self.ballsThisOver), 1080, 50)
        for i in range(len(self.teamNames)):
            self.text.drawCenteredText(self.teamNames[i].split(' ', 1)[1], 100, (i*40) + 120)
        for i in range(len(self.allBatsmenScores)):
            if(self.allBatsmenScores[i] == self.allBatsmenScores[self.totalWickets + self.facingBatsman]):
                self.text.drawCenteredText(str(self.allBatsmenScores[i]) + "*", 520, (i*40) + 120)
            else:
                self.text.drawCenteredText(str(self.allBatsmenScores[i]), 520, (i*40) + 120)
        self.text.drawCenteredText("Current batsmen: " + str(self.currentBatsmenScores), 820, 120)
        self.text.drawCenteredText("All batsmen scores: " + str(self.allBatsmenScores), 820, 240)
        self.text.drawCenteredText("Facing batsman: " + str(self.facingBatsman), 820, 360)
        self.text.drawCenteredText("Non facing batsman: " + str(self.nonFacingBatsman), 820, 480)
    def update(self):
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
        elif self.buttons[5].isPressed():
            self.scoreThisBall = 6
            self.balls = 1
            self.wicketTaken = 0
        elif self.buttons[6].isPressed():
            self.wicketTaken = 1
            self.balls = 1
        elif self.buttons[7].isPressed():
            self.balls = 1
            self.wicketTaken = 0
        if self.buttons[8].isPressed():
            self.score += self.scoreThisBall
            self.totalWickets += self.wicketTaken
            self.totalBalls += self.balls
            self.currentBatsmenScores[self.facingBatsman] += self.scoreThisBall
            self.overs = self.totalBalls//6
            self.ballsThisOver = self.totalBalls % 6
            if(self.wicketTaken == 1):
                self.allBatsmenScores.append(0)
                self.currentBatsmenScores[self.facingBatsman] = 0
            self.allBatsmenScores[self.totalWickets + self.facingBatsman] = self.currentBatsmenScores[self.facingBatsman]
            if(self.scoreThisBall % 2 == 1):
                temp = self.facingBatsman
                self.facingBatsman = self.nonFacingBatsman
                self.nonFacingBatsman = temp
            self.balls = 0
            self.scoreThisBall = 0
            self.wicketTaken = 0

    def pollEvents(self, event):
        for i in range(len(self.buttons)):
            self.buttons[i].pollForEvents(event)
        
