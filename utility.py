import pygame
import math
pygame.init()
pygame.font.init()

class TextRenderer:
    def __init__(self, window, fontName='resources/Roboto-Thin.ttf'):
        self.screen = window
        self.defaultSize = 32
        self.colour = (255, 255, 255)
        self.fontName = fontName
        self.textFont = pygame.font.Font(self.fontName, self.defaultSize) 
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
        self.textFont = pygame.font.Font(self.fontName, size)

class Button:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.pressed = False
        self.image.set_alpha(180)

    def render(self, window):
        window.blit(self.image, (self.x, self.y))

    def pollForEvents(self, event):
        x, y = pygame.mouse.get_pos()
        if x >= self.x and x <= self.x + self.image.get_rect()[2] and y >= self.y and y <= self.y + self.image.get_rect()[3]:
            if event.type == pygame.MOUSEBUTTONUP:
                self.pressed = True
                self.image.set_alpha(220)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.image.set_alpha(255)
            else:
                self.image.set_alpha(220)
        else:
            self.pressed = False
            self.image.set_alpha(180)
        
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

class TextInput:
    #TODO - handle capital letters
    def __init__(self, window, x, y, fontSize):
        self.window = window
        self.textRenderer = TextRenderer(self.window, 'resources/Roboto-ThinMono.ttf')
        self.textRenderer.setFontSize(fontSize)
        self.x = x
        self.y = y
        self.textBuffer = []
        self.oscillation = 0
        self.blinkColour = (0, 0, 0)
        self.blinkSpeed = 5
        self.offset = 0

    def render(self):
        self.oscillation = math.sin((pygame.time.get_ticks() / 1000) * self.blinkSpeed)
        if(self.oscillation < 0):
            self.blinkColour = (0, 0, 0)
        else:
            self.blinkColour = (0, 153, 51)

        for i in range(len(self.textBuffer)):
            self.textRenderer.drawText(str(self.textBuffer[i]), self.x + (i * 15), self.y)
        pygame.draw.rect(self.window, self.blinkColour, (self.x + (len(self.textBuffer) * 15), self.y + 2, 2, 30))

    def pollForEvents(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if(len(self.textBuffer)) == 0:
                    return
                else:
                    self.textBuffer.pop()
            elif event.key == pygame.K_LSHIFT:
                self.offset = 32
            else:
                self.textBuffer.append(chr(event.key - self.offset))
                self.offset = 0
                print(self.textBuffer)

    def getText(self):
        return ''.join(self.textBuffer)
        
            
