import pygame
#Menu buttons
class Button:
    def __init__(self,x,y,image, scale):
        imagewidth = image.get_width()
        imageheight = image.get_height()
        self.image = pygame.transform.scale(image, (int(imagewidth*scale), int(imageheight*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
    def draw(self,surface):
        action=False

        #Mouseposition
        pos=pygame.mouse.get_pos()

        #Mouseover and clicked check
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1 and self.clicked == False:
                self.clicked=True
                action=True
            if pygame.mouse.get_pressed()[0]==0:
                self.clicked=False
        #Draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action