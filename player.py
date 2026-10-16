import pygame

class Player:
    p = pygame.Vector2(0, 0)
    v = pygame.Vector2(0, 0)
    hitbox = pygame.Rect(0, 0, 0, 0)
    colbox = pygame.Rect(0, 0, 0, 0)
    coloffset = pygame.Vector2(0,12)
    graphic = None

    spd = 3
    decel = .825
    accel = .75
    h = 15

    def __init__(self, surface, center, width, height):
        self.surface = surface
        self.p = pygame.Vector2(center)
        self.v = pygame.Vector2(0, 0)
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(0, 0, width*2, height*2)
        self.colbox = pygame.Rect(0, 0, 16, 8)
        self.hitbox.center = self.p
        self.graphic = pygame.image.load("Assets/Images/Player/chet00.png").convert_alpha()
        self.graphic = pygame.transform.scale(self.graphic, (width*2, height*2))
        self.current_sprite = self.graphic
        self.keys = 0

    def update(self):
        self.set(self.p + self.v)

    def cols(self, rects):
        for rect in rects:
            disp = pygame.Vector2(self.p.xy)
            self.colbox.center = disp + self.coloffset
            if rect.colliderect(self.colbox.move(2*self.v.x, 0)):
                if rect.tag == "shed" and self.keys >= 4:
                                print("Win!")
                                self.keys = 0
                if self.v.x > 0:
                    disp = pygame.Vector2(rect.left - (.5 * self.colbox.width), disp.y)
                elif self.v.x < 0:
                    disp = pygame.Vector2(rect.right + (.5 * self.colbox.width), disp.y)    
                self.v = pygame.Vector2(0, self.v.y)   
            if rect.colliderect(self.colbox.move(2 * self.v.xy)):
                if rect.tag == "shed" and self.keys >= 4:
                                print("Win!")
                                self.keys = 0   
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

    def draw(self):
        image_rect = self.graphic.get_rect(center=self.p)
        #pygame.draw.rect(self.surface,(0, 125, 0), self.colbox)
        self.surface.blit(self.graphic, image_rect)