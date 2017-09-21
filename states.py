import pygame
import jsonloader
import utility

pygame.init()

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
        self.util.setFontSize(16)
        self.menuButton = utility.Button(pygame.image.load("MenuButton.png").convert(), 272, 500)
        self.players = []
        for i in range(len(jsonloader.data["players"])):
            player = utility.TextButton(self.window, 0, i * 50)
            self.players.append(player)

    def render(self):
        self.window.fill((53, 92, 125))
        for i in range(len(self.players)):
            self.players[i].render(jsonloader.data["players"][i]["name"])
        self.menuButton.render(self.window)

    def update(self):
        if self.menuButton.isPressed():
            self.stateManager.changeState(MenuState(self.stateManager, self.window))

    def pollEvents(self, event):
        self.menuButton.pollForEvents(event)

#player stats screen
class PlayerStatisticsState(State):
    def __init__(self, stateManager, window, playerInfo):
        super(PlayerStatisticsState, self).__init__(stateManager)
        self.window = window
        self.playerInfo = playerInfo
        self.playerStats = utility.TextRenderer(self.window)

    def render(self):
        self.playerStats.drawText(self.playerInfo, 0, 0)        

    def update(self):
        self.window.fill((53, 92, 125))

    def pollEvents(self, event):
        pass

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
        #TODO - check for mouse input(if it is clicked on text)
        if self.playerBrowseButton.isPressed():
            self.stateManager.changeState(PlayerBrowseState(self.stateManager, self.window))

    def pollEvents(self, event):
        self.playerBrowseButton.pollForEvents(event)     
        self.createMatchButton.pollForEvents(event) 
            
            