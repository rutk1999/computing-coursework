import pygame
pygame.init()
pygame.font.init()

class TextRenderer:
    def __init__(self, window):
        self.screen = window
        self.defaultSize = 32
        self.colour = (0, 0, 0)
        self.textFont = pygame.font.Font('freesansbold.ttf', self.defaultSize) 

    def drawText(self, text, posx, posy):
        self.textSurface = self.textFont.render(text, True, self.colour)
        self.screen.blit(self.textSurface, (posx, posy))
    
    def setFontSize(self, size):
        self.textFont = pygame.font.Font('freesansbold.ttf', size)