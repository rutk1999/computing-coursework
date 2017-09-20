import pygame
import states
pygame.init()
pygame.font.init()

class Main:
    def init(self):
        self.window = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.states = {"Test": states.TestState(self.window), "PlayerBrowse": states.PlayerBrowseState(self.window)}
        self.setState("Test")

    def setState(self, defaultState):
        self.stateName = defaultState
        self.state = self.states[self.stateName]
        self.isStateFinished = False

    def update(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.isStateFinished = True
            self.state.pollEvents(event)
        if self.state.changeState:
            self.setState(self.state.nextState)
        self.state.update()

    def render(self):  
        self.window.fill((100, 225, 6))  
        self.state.render()

    def loop(self):
        while not self.isStateFinished:
            events = pygame.event.get()
            self.update(events)
            self.render()
            pygame.display.update()
            self.clock.tick(60)

main = Main()
main.init()
main.loop()

pygame.quit()

