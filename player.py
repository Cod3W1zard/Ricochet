from inspect import currentframe
import pygame
import sys

class Player:
    p = pygame.Vector2(0, 0)
    v = pygame.Vector2(0, 0)
    hitbox = pygame.Rect(0, 0, 0, 0)
    colbox = pygame.Rect(0, 0, 0, 0)
    coloffset = pygame.Vector2(0,12)

    dashcd = 1
    curdashcd = 0
    dashspd = 6
    spd = 3
    decel = .25
    accel = .75
    
    h = 16
    state = "run"

    fl = False
    spritesheet = None
    grect = pygame.Rect(0,0,32,32)
    animations = {
        "idle" : ([(0,0)], 1, False),
        "run" : ([(0, 32), (32, 32), (64, 32), (96, 32)], 5, True),
        "hurt" : ([(0,64), (32, 64)], 5, False),
        "dash" : ([(0,96), (32, 96)], 5, False),
    }
    curAnim = "idle"

    def __init__(self, surface, center, width, height, game_state):
        self.surface = surface
        self.p = pygame.Vector2(center)
        self.v = pygame.Vector2(0, 0)
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(0, 0, width*2, height*2)
        self.colbox = pygame.Rect(0, 0, 16, 8)
        self.hitbox.center = self.p
        self.spritesheet = pygame.image.load("Assets/Images/Player/chet.png").convert_alpha()
        self.keys = 0
        self.game_state = game_state

    def update(self):
        self.set(self.p + self.v)
        self.animationLogic()

    def cols(self, rects):
        for rect in rects:
            disp = pygame.Vector2(self.p.xy)
            self.colbox.center = disp + self.coloffset 
            if rect.tag == "shed" and rect.colliderect(self.colbox.move(2*self.v.x, 2*self.v.y)):
                if self.keys >= 4:
                    self.game_state = "win"
                    self.keys = 0
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
        
    def movement(self, dir):
        if dir.magnitude() < .1:
            self.v = self.v.move_towards(pygame.Vector2(0,0), self.decel)
        else:
            self.v = self.v.move_towards(dir.normalize() * self.spd, self.accel)

    def set(self, location: tuple | pygame.Vector2):
        l = pygame.Vector2(location)
        self.hitbox.center = self.p = l
    
    def takeDamage(self, damage):
        self.h -= damage
        if self.h <= 0:
            pygame.quit()
            sys.exit()

    def takeDamage(self, bullet):
        self.h -= bullet.hit()
        self.state = "hitstun"
        d = bullet.hit()
        self.v += bullet.v * .5
        
        if d > 0:
            self.h -= d
    
        if not self.state == "dead":
            #self.flash = 60
            if(self.h <= 0):
                self.state = "dead"
    
    def dash(self, dir):
        self.state = "dash"
        if dir.xy != (0, 0):
            self.v = dir.normalize() * self.dashspd
    


    def drag(self):
        self.v = self.v.move_towards(pygame.Vector2(0 ,0), self.decel)
        if self.v.magnitude() < 1 and self.state != "dead":
            self.state = "run"

    animTick = 0
    currentframe = 0
    def animationLogic(self):
        if self.curAnim != "idle":
            if self.v.magnitude() < .1:
                self.changeAnim("idle")
        if self.curAnim != "run":
            if self.v.magnitude() > .1:
                self.changeAnim("run")
        elif abs(self.v.x) > .1:
            if self.v.x > 0:
                self.fl = False
            else:
                self.fl = True

        if self.state == "hitstun" or self.state == "dead":
            if self.curAnim != "hurt":
                self.changeAnim("hurt")

            if abs(self.v.x) > 1:
                if self.v.x > 0:
                    self.fl = True
                else:
                    self.fl = False
        
        if self.state == "dash":
            if self.curAnim != "dash":
                self.changeAnim("dash")

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
        #pygame.draw.rect(self.surface,(0, 125, 0), self.colbox)
        disp = pygame.Vector2(-self.grect.width/2, -self.grect.height/2)
        I = self.spritesheet.subsurface(self.grect)
        self.surface.blit(pygame.transform.flip(I, self.fl, False), self.p + disp)