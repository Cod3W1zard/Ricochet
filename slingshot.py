import pygame
import math
import player

import bullet

class Slingshot:
    
    def __init__(self, surface, center, width, height, player):
        self.surface = surface
        self.p = pygame.Vector2(center)
        self.width = width
        self.height = height
        self.graphic = pygame.image.load("Assets/Images/frame001.png").convert_alpha()
        self.graphic = pygame.transform.scale(self.graphic, (width*2, height*2))
        self.rotation = 0
        self.current_sprite = self.graphic
        self.shoot_stage = 0
        self.flip = False
        self.player = player

    def shoot(self):
        b = bullet.Bullet(self.surface, self.p + (0, 6), 5, 10, pygame.Vector2((pygame.mouse.get_pos()) - self.p).normalize())
        bullet.pbullets.append(b)
        print(pygame.mouse.get_pos())
        self.shoot_stage = 1

    def rotate(self):
        #self.graphic = pygame.transform.rotate(self.graphic, self.rotation)
        self.radians = math.radians(self.rotation)
        self.p = pygame.Vector2(self.p.x, self.p.y) + (13 * math.cos(self.radians), -13 * math.sin(self.radians))
        if self.rotation > 360 or self.rotation < -360:
            self.rotation = 0
        if self.rotation > 90 or self.rotation < -90:
            self.rotation -= 180
            self.flip = True
        else:
            self.flip = False
        
        if self.flip:    
            self.current_sprite = pygame.transform.flip(self.graphic, True, False)
            self.player.current_sprite = pygame.transform.flip(self.player.graphic, True, False)
        else:
            self.current_sprite = self.graphic
            self.player.current_sprite = self.player.graphic

        self.current_sprite = pygame.transform.rotate(self.current_sprite, self.rotation)
    def draw(self):
        
        if self.shoot_stage in  (1, 2, 5, 6):
                    self.graphic = pygame.image.load("Assets/Images/frame002.png").convert_alpha()
                    self.shoot_stage +=1
        elif self.shoot_stage in (3, 4):
                    self.graphic = pygame.image.load("Assets/Images/frame003.png").convert_alpha()
                    self.shoot_stage += 1
        elif self.shoot_stage == 7:
             self.graphic = pygame.image.load("Assets/Images/frame001.png").convert_alpha()
             self.shoot_stage = 0
        self.rotation = (pygame.Vector2((pygame.mouse.get_pos()) - self.p).normalize().angle_to(pygame.Vector2(1, 0)))
        self.rotate()
        image_rect = self.current_sprite.get_rect(center=self.p + (0, 6))
        self.surface.blit(self.current_sprite, image_rect)

        if self.shoot_stage == 1:
            self.shoot_stage = 2
    