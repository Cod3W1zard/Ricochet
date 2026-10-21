from pygame import Vector2
import pygame
import random

class Enemy:
    
    keylist = []
    keyg = pygame.image.load("Assets/Images/key.png")
    p = pygame.Vector2(0, 0)
    v = pygame.Vector2(0, 0)
    dir = pygame.Vector2(0, 0)
    hitbox = pygame.Rect(0, 0, 0, 0)
    colbox = pygame.Rect(0, 0, 0, 0)
    coloffset = pygame.Vector2(0,12)

    spd = 2
    decel = .125
    accel = .125

    h = 8
    state = "pursue"

    pd = 200
    clearshot = False
    shotcooldown = 90
    curshotcd = 0
    curpathfinding = False
    pathfindP = pygame.Vector2(0,0)

    fl = False
    spritesheet = None
    grect = pygame.Rect(0,0,32,32)
    animations = {
        "idle" : ([(0,0)], 1, False),
        "run" : ([(0, 32), (32, 32), (64, 32), (96, 32)], 5, True),
        "hurt" : ([(0,64), (32, 64)], 5, False),
    }
    curAnim = "idle"

    def __init__(self, surface, center, width, height, plr):
        self.surface = surface
        self.p = pygame.Vector2(center)
        self.v = pygame.Vector2(0, 0)
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(0, 0, width*2, height*2)
        self.colbox = pygame.Rect(0, 0, 16, 8)
        self.hitbox.center = self.p
        self.spritesheet = pygame.image.load("Assets/Images/Enemy/bad.png").convert_alpha()
        self.flash = 0
        self.elist = None
        self.plr = plr
        self.keylist = []

    def update(self):
        self.set(self.p + self.v)     
        if self.curshotcd > 0:
            self.curshotcd -= 1
        self.animationLogic()

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

    walldist = 1000
    def track(self, plr, walls):
        disp = (plr.p - self.p)
        self.dir = disp.normalize()    
        if self.curpathfinding:
            wdisp = (self.pathfindP - self.p)
            if wdisp.dot(self.dir) < 0:
               self.curpathfinding = False
            self.dir = wdisp.normalize()
            self.v = self.v.move_towards(self.dir * self.spd, self.accel)
        else:
            self.clearshot = True
            walldist = 10000
            for w in walls:
                if w.clipline(self.p, plr.p):
                    self.clearshot = False
                    horz = abs(disp.x) > abs(disp.y)
                    px = 0
                    py = 0

                    if disp.x <= 0: 
                        if self.p.x > w.right:
                            px = w.right + self.colbox.width * 2
                            if self.p.x < w.top or self.p.x > w.bottom:
                                px = w.left - self.colbox.width * 2
                        else:
                            px = w.left - self.colbox.width * 2
                            if self.p.x < w.top or self.p.x > w.bottom:
                                px = w.right + self.colbox.width * 2
                    else:
                        if self.p.x < w.left:
                            px = w.left - self.colbox.width * 2
                            if self.p.x < w.top or self.p.x > w.bottom:
                                px = w.right + self.colbox.width * 2
                        else:
                            px = w.right + self.colbox.width * 2
                            if self.p.x < w.top or self.p.x > w.bottom:
                                px = w.left - self.colbox.width * 2

                    if disp.y <= 0: 
                        if self.p.y > w.bottom:
                            py = w.bottom + self.colbox.height * 4
                        else:
                            py = w.top - self.colbox.height * 4
                    else:
                        if self.p.x < w.top:
                            py = w.top - self.colbox.height * 4
                        else:
                            py = w.bottom + self.colbox.height * 4
                       
                    temp = pygame.Vector2(px, py)
                    tdisp = temp - self.p
                    if tdisp.magnitude() < walldist and not w.clipline(self.p, temp):
                        walldist = tdisp.magnitude()                          
                        self.pathfindP = pygame.Vector2(px, py)
                        self.curpathfinding = True

            if self.clearshot:
                if disp.magnitude() < self.pd:
                    self.v = self.v.move_towards(pygame.Vector2(0,0), self.decel)
                else:
                    self.v = self.v.move_towards(self.dir * self.spd, self.accel)

    def set(self, location: tuple | pygame.Vector2):
        l = pygame.Vector2(location)
        self.hitbox.center = self.p = l
    
    def takeDamage(self, damage, elist):
        self.elist = elist
        self.h -= damage 
        if not self.dying:
            self.flash = 60
        if(self.h <= 0):
            self.dying = True
        
    def takeDamage(self, bullet, elist):
        self.elist = elist
        self.h -= bullet.hit()
        self.v += bullet.v * .5
        self.state = "hitstun"
        if not self.state == "dead":
            self.flash = 60
            if(self.h <= 0):
                self.state = "dead"
    
    def hurt(self):
        self.v = self.v.move_towards(pygame.Vector2(0 ,0), self.decel)
        if self.v.magnitude() < 1 and self.state != "dead":
            self.state = "pursue"

    animTick = 0
    currentframe = 0
    def animationLogic(self):
        if self.state == "pursue":
            if self.curAnim != "idle":
                if self.v.magnitude() < .1:
                    self.changeAnim("idle")
            if self.curAnim != "run":
                if self.v.magnitude() > .1:
                    self.changeAnim("run")
        if self.curAnim != "hurt":
            if self.state == "hitstun":
                self.changeAnim("hurt")
        if self.dir.x > 0:
            self.fl = False
        else:
            self.fl = True
            
        self.playAnimation()

    def changeAnim(self, anim):
        self.animTick = 0
        self.currentframe = 0
        self.curAnim = anim

    def playAnimation(self):
        self.animTick += 1
        if self.animTick >= self.animations[self.curAnim][1]:
            if self.currentframe == len(self.animations[self.curAnim][0]) - 1:
                if self.animations[self.curAnim][2]: 
                    self.currentframe = 0
            else:
                self.currentframe += 1
            self.animTick = 0
        self.grect.x = self.animations[self.curAnim][0][self.currentframe][0]
        self.grect.y = self.animations[self.curAnim][0][self.currentframe][1]

    def draw(self):
        if self.flash > 0:
            self.flash -= 1
        if self.state == "dead" and self.flash == 0:
            if random.uniform(1,1) == 1:
                key = pygame.Rect(0, 0, 16, 16)
                key.center = self.p
                Enemy.keylist.append(key)
            self.elist.remove(self)
        if self.flash % 4 < 2:
            #pygame.draw.rect(self.surface,(0, 125, 0), self.colbox)
            disp = pygame.Vector2(-self.grect.width/2, -self.grect.height/2)
            I = self.spritesheet.subsurface(self.grect)
            self.surface.blit(pygame.transform.flip(I, self.fl, False), self.p + disp)
        