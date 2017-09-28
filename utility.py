import pygame
pygame.init()
pygame.font.init()

class TextRenderer:
    def __init__(self, window):
        self.screen = window
        self.defaultSize = 32
        self.colour = (255, 255, 255)
        self.textFont = pygame.font.Font('Roboto-Thin.ttf', self.defaultSize) 
        self.textSurface = self.textFont.render("", True, self.colour)

    def drawText(self, text, posx, posy):
        self.textSurface = self.textFont.render(text, True, self.colour)
        self.screen.blit(self.textSurface, (posx, posy))
    
    def drawCenteredText(self, text, posx, posy):
        size = self.textFont.size(text)
        finalX = posx - (size[0] / 2)
        finalY = posy - (size[1] / 2)
        self.textSurface = self.textFont.render(text, True, self.colour)
        self.screen.blit(self.textSurface, (finalX, finalY))
    
    def setFontSize(self, size):
        self.textFont = pygame.font.Font('Roboto-Thin.ttf', size)

class Button:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.pressed = False

    def render(self, window):
        window.blit(self.image, (self.x, self.y))

    def pollForEvents(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            if x >= self.x and x <= self.x + self.image.get_rect()[2] and y >= self.y and y <= self.y + self.image.get_rect()[3]:
                self.pressed = True
        else:
            self.pressed = False
    def isPressed(self):
        return self.pressed

class TextButton:
    def __init__(self, window, x, y, fontSize):
        self.textRenderer = TextRenderer(window)
        self.textRenderer.setFontSize(fontSize)
        self.x = x
        self.y = y
        self.pressed = False
        
    def render(self, text):
        self.textRenderer.drawText(text, self.x, self.y)
    
    def pollForEvents(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            if x >= self.x and x <= self.x + self.textRenderer.textSurface.get_rect()[2] and y >= self.y and y <= self.y + self.textRenderer.textSurface.get_rect()[3]:
                self.pressed = True
            else:
                self.pressed = False
    def isPressed(self):
        return self.pressed
