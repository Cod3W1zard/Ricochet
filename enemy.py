import pygame
import random

class Enemy:
    
    keylist = []
    p = pygame.Vector2(0, 0)
    v = pygame.Vector2(0, 0)
    dir = pygame.Vector2(0, 0)
    hitbox = pygame.Rect(0, 0, 0, 0)
    colbox = pygame.Rect(0, 0, 0, 0)
    coloffset = pygame.Vector2(0,12)
    graphic = None

    spd = 2
    decel = .825
    accel = .75
    h = 8
    pd = 200
    clearshot = False
    shotcooldown = 30
    curshotcd = 0
    curpathfinding = False
    pathfindP = pygame.Vector2(0,0)
    die = False

    def __init__(self, surface, center, width, height, plr):
        self.surface = surface
        self.p = pygame.Vector2(center)
        self.v = pygame.Vector2(0, 0)
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(0, 0, width*2, height*2)
        self.colbox = pygame.Rect(0, 0, 16, 8)
        self.hitbox.center = self.p
        self.graphic = pygame.image.load("Assets/Images/bad00.png").convert_alpha()
        self.graphic = pygame.transform.scale(self.graphic, (width*2, height*2))
        self.flash = 0
        self.elist = None
        self.plr = plr
        self.keylist = []

    def update(self):
        self.set(self.p + self.v)     
        if self.curshotcd > 0:
            self.curshotcd -= 1

    def cols(self, rects):
        for rect in rects:
            disp = pygame.Vector2(self.p.xy)
            self.colbox.center = disp + self.coloffset
            if rect.colliderect(self.colbox.move(2*self.v.x, 0)):
                if self.v.x > 0:
                    disp = pygame.Vector2(rect.left - (.5 * self.colbox.width), disp.y)
                elif self.v.x < 0:
                    disp = pygame.Vector2(rect.right + (.5 * self.colbox.width), disp.y)    
                self.v = pygame.Vector2(0, self.v.y)   
            if rect.colliderect(self.colbox.move(2 * self.v.xy)):   
                if self.v.y < 0:
                    disp = pygame.Vector2(disp.x, rect.bottom + (.5 * self.colbox.height) - self.coloffset.y)
                elif self.v.y > 0:
                    disp = pygame.Vector2(disp.x, rect.top - (.5 * self.colbox.height) - self.coloffset.y)
                self.v = pygame.Vector2(self.v.x, 0)           
            self.set(disp)

    def track(self, plr):
        disp = (plr.p - self.p)
        self.dir = disp.normalize()
        self.clearshot = True

        if self.clearshot and disp.magnitude() < self.pd:
            self.v = self.v.move_towards(pygame.Vector2(0,0), self.decel)
        else:
             self.v = self.v.move_towards(self.dir * self.spd, self.accel)

    def set(self, location: tuple | pygame.Vector2):
        l = pygame.Vector2(location)
        self.hitbox.center = self.p = l

    def draw(self):
        if self.die and self.flash == 0:
            if random.uniform(1,1) == 1:
                key = pygame.Rect(0, 0, 5, 5)
                key.center = self.p
                Enemy.keylist.append(key)
            self.elist.remove(self)
        if self.flash % 4 < 2:
                image_rect = self.graphic.get_rect(center=self.p)
                pygame.draw.rect(self.surface,(0, 125, 0), self.colbox)
                self.surface.blit(self.graphic, image_rect)
        if self.flash > 0:
            self.flash -= 1

    def flash(self):
        pass
    
    def takeDamage(self, damage, elist):
        self.elist = elist
        self.h -= damage
        if(self.h <= 0):
            self.die = True
        self.flash = 60
