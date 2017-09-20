import pygame
import jsonloader
import utility

pygame.init()

#state base class
class State():
    def __init__(self):
        #these are for indicating whether it should move to the next state
        self.changeState = False
        self.nextState = ""
    
    def render(self, window):
        raise NotImplementedError
    
    def update(self):
        raise NotImplementedError

    def pollEvents(event):
        raise NotImplementedError

#player browsing screen
class PlayerBrowseState(State):
    def __init__(self, window):
        super(PlayerBrowseState, self).__init__()
        self.window = window
        self.util = utility.TextRenderer(window)
        self.util.setFontSize(16)

    def render(self):
        for i in range(len(jsonloader.data["players"])):
            self.util.drawText(jsonloader.data["players"][i]["name"], 0, i * 20)
    def update(self):
        print("test")
    
    def pollEvents(self, event):
        pass

class TestState(State):
    def __init__(self, window):
        super(TestState, self).__init__()
        self.window = window
        self.util = utility.TextRenderer(window)
        self.util.setFontSize(16)
    
    def render(self):
        self.window.fill((255, 0, 255))
        self.util.drawText("Lorem ipsum dolor mit", 50, 50)
    
    def update(self):
        self.mousePos = pygame.mouse.get_pos()
        #TODO - check for mouse input(if it is clicked on text)

    def pollEvents(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_0:
            self.nextState = "PlayerBrowse"
            self.changeState = True
            
            