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
        #self.changeState = False
        #self.nextState = ""
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
        self.menuButton = utility.Button(pygame.image.load("MenuButton.png").convert(), 272, 500)
        self.createPlayerButton = utility.Button(pygame.image.load("AddPlayerButton.png").convert(), 650, 500)
        self.players = []
        self.offset = 10
        self.fontSize = 24
        for i in range(len(jsonloader.data["players"])):
            player = utility.TextButton(self.window, self.offset, (i * (self.fontSize * 1.5)) + self.offset, self.fontSize)
            self.players.append(player)

    def render(self):
        self.window.fill((53, 92, 125))
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
        self.playerStatisticsButton = utility.Button(pygame.image.load("BrowsePlayers.png").convert(), 100, 500)
        self.menuButton = utility.Button(pygame.image.load("MenuButton.png").convert(), 428, 500)

    def render(self):
        self.playerStats.setFontSize(48)
        self.playerStats.drawCenteredText(self.playerInfo["name"], 400, 100)
        self.playerStats.setFontSize(32)
        self.playerStats.drawCenteredText("Age: " + self.playerInfo["age"], 400, 200)    
        self.playerStats.drawCenteredText("Runs: " + self.playerInfo["runsScored"], 400, 250)    
        self.playerStats.drawCenteredText("Wickets: " + self.playerInfo["wicketsTaken"], 400, 300)   
        self.playerStatisticsButton.render(self.window)
        self.menuButton.render(self.window)

    def update(self):
        self.window.fill((53, 92, 125))
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
        self.playerBrowseButton = utility.Button(pygame.image.load("BrowsePlayers.png").convert(), 272, 230)
        self.createMatchButton = utility.Button(pygame.image.load("CreateMatchButton.png").convert(), 272, 400)
        self.titleText = utility.Button(pygame.image.load("TitleText.png").convert_alpha(), 208, 50)

    def render(self):
        self.window.fill((53, 92, 125))
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
        #self.inputBox = InLineTextBox((400, 200), 200, color=(255, 255, 255), bg_color=(0, 0, 0))
        self.addPlayerButton = utility.Button(pygame.image.load("AddPlayerButton.png").convert(), 368, 500)

    def render(self):
        self.window.fill((53, 92, 125))
        self.text.setFontSize(48)
        self.text.drawCenteredText("Add a Player", 400, 100)
        #self.inputBox.render(self.window)
        self.addPlayerButton.render(self.window)
    
    def update(self):
        pass
        #if self.addPlayerButton.isPressed():
            #get text in the inputbox
            #temp = self.inputBox.text
            #split the string from name and age
            #nameAndAge = temp.split(',')
            #add player using jsonloader function
            #jsonloader.addPlayer(jsonloader.data, nameAndAge[0].strip(), nameAndAge[1].strip())
            #self.stateManager.changeState(PlayerBrowseState(self.stateManager, self.window))
    
    def pollEvents(self, event):
        #self.inputBox.update(event)
        self.addPlayerButton.pollForEvents(event)

class MatchState(State):
    def __init__(self, stateManager, window):
        super(MatchState, self).__init__(stateManager)
        self.window = window
        self.buttonOne = utility.Button(pygame.image.load("run1.png").convert(), 15, 500)
        self.buttonTwo = utility.Button(pygame.image.load("run2.png").convert(), 115, 500)
        self.buttonThree = utility.Button(pygame.image.load("run3.png").convert(), 215, 500)
        self.buttonFour = utility.Button(pygame.image.load("run4.png").convert(), 315, 500)
        self.buttonSix = utility.Button(pygame.image.load("run6.png").convert(), 415, 500)
        self.buttonWicket = utility.Button(pygame.image.load("wicket.png").convert(), 515, 500)
        self.buttonDot = utility.Button(pygame.image.load("dot.png").convert(), 615, 500)
        self.addToTotalScore = utility.Button(pygame.image.load("AddPlayerButton.png").convert(), 715, 500)
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
        self.window.fill((53, 92, 125))
        pygame.draw.rect(self.window, (80, 80, 80), (0, 20, 800, 60))
        self.buttonOne.render(self.window)
        self.buttonTwo.render(self.window)
        self.buttonThree.render(self.window)
        self.buttonFour.render(self.window)
        self.buttonSix.render(self.window)
        self.buttonWicket.render(self.window)
        self.buttonDot.render(self.window)
        self.addToTotalScore.render(self.window)
        self.text.setFontSize(48)
        self.text.drawCenteredText("Score: " + str(self.score) + "/" + str(self.totalWickets), 400, 50)
        self.text.setFontSize(24)
        self.text.drawCenteredText("Runs this ball: " + str(self.scoreThisBall), 100, 50)
        self.text.drawCenteredText("Over: " + str(self.overs) + "." + str(self.ballsThisOver), 700, 50)
        for i in range(len(self.teamNames)):
            self.text.drawCenteredText(self.teamNames[i].split(' ', 1)[1], 100, (i*35) + 100)
        for i in range(len(self.allBatsmenScores)):
            self.text.drawCenteredText(str(self.allBatsmenScores[i]), 700, (i*35) + 100)
        
    def update(self):
        if self.buttonOne.isPressed():
            self.scoreThisBall = 1
            self.balls = 1
            self.wicketTaken = 0
        elif self.buttonTwo.isPressed():
            self.scoreThisBall = 2
            self.balls = 1
            self.wicketTaken = 0
        elif self.buttonThree.isPressed():
            self.scoreThisBall = 3
            self.balls = 1
            self.wicketTaken = 0
        elif self.buttonFour.isPressed():
            self.scoreThisBall = 4
            self.balls = 1
            self.wicketTaken = 0
        elif self.buttonSix.isPressed():
            self.scoreThisBall = 6
            self.balls = 1
            self.wicketTaken = 0
        elif self.buttonWicket.isPressed():
            self.wicketTaken = 1
            self.balls = 1
        elif self.buttonDot.isPressed():
            self.balls = 1
            self.wicketTaken = 0
        if self.addToTotalScore.isPressed():
            self.score += self.scoreThisBall
            self.totalWickets += self.wicketTaken
            self.totalBalls += self.balls
            self.currentBatsmenScores[self.facingBatsman] += self.scoreThisBall
            self.overs = self.totalBalls//6
            self.ballsThisOver = self.totalBalls % 6
            if(self.wicketTaken == 1):
                self.allBatsmenScores.append(0)
                self.currentBatsmenScores[self.facingBatsman] = 0
                self.facingBatsman = 1
            self.allBatsmenScores[self.totalWickets + self.facingBatsman] = self.currentBatsmenScores[self.facingBatsman]
            if(self.scoreThisBall % 2 == 1):
                temp = self.facingBatsman
                self.facingBatsman = self.nonFacingBatsman
                self.nonFacingBatsman = temp
            self.balls = 0
            self.scoreThisBall = 0
            self.wicketTaken = 0

    def pollEvents(self, event):
        self.buttonOne.pollForEvents(event)
        self.buttonTwo.pollForEvents(event)
        self.buttonThree.pollForEvents(event)
        self.buttonFour.pollForEvents(event)
        self.buttonSix.pollForEvents(event)
        self.buttonWicket.pollForEvents(event)
        self.buttonDot.pollForEvents(event)
        self.addToTotalScore.pollForEvents(event)
        
