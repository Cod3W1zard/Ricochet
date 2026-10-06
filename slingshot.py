import pygame
import math

class Slingshot:
    def __init__(self, surface, center, width, height):
        self.surface = surface
        self.p = pygame.Vector2(center)
        self.width = width
        self.height = height
        self.graphic = pygame.image.load("Assets/Images/chet00.png").convert_alpha()
        self.graphic = pygame.transform.scale(self.graphic, (width*2, height*2))
        self.rotation = 0


    def rotate(self):
        #self.graphic = pygame.transform.rotate(self.graphic, self.rotation)
        self.radians = math.radians(self.rotation)
        self.p = pygame.Vector2(self.p.x, self.p.y) + (8 * math.cos(self.radians), -8 * math.sin(self.radians))
    def draw(self):
        self.rotation = (pygame.Vector2((pygame.mouse.get_pos()) - self.p).normalize().angle_to(pygame.Vector2(1, 0)))
        self.rotate()
        image_rect = self.graphic.get_rect(center=self.p)
        self.surface.blit(self.graphic, image_rect)