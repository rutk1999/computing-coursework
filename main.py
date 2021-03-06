import pygame
import states
pygame.init()
pygame.font.init()

class Main:
    def __init__(self):
        self.window = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.stateManager = states.StateManager(self.window)
        self.menuState = states.MenuState(self.stateManager, self.window)
        self.testState = states.MatchState(self.stateManager, self.window, "England", "New Zealand", "New Zealand", 1)
        self.test2State = states.MatchCreationState(self.stateManager, self.window)
        self.stateManager.changeState(self.test2State)
        self.running = True

    def update(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            self.stateManager.pollEvents(event)
        self.stateManager.update()

    def render(self):  
        self.stateManager.render()

    def loop(self):
        while self.running:
            events = pygame.event.get()
            self.update(events)
            self.render()
            pygame.display.update()
            self.clock.tick(60)
            
main = Main()
main.loop()
pygame.quit()

