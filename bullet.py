import pygame 

class Bullet:
       p = pygame.Vector2(0, 0)
       v = pygame.Vector2(0, 0)
       r = 1
       maxbounces = 5
       curbounces = 0
       speed = 5

       def __init__(self, surface, center, radius, speed, direction):
              self.surface = surface
              self.p = pygame.Vector2(center)
              self.r = radius
              self.v = pygame.Vector2(direction * speed)
              self.hitbox = pygame.Rect(0, 0, radius*2, radius*2)
              self.hitbox.center = self.p
              curbounces = 0

       def cols(self, rects):
              c = False
              for rect in rects:
                     if rect.colliderect(self.hitbox.move(self.v.x, 0)):
                            if self.v.x > 0:
                                   self.p = pygame.Vector2(rect.left - (.5 * self.hitbox.width), self.p.y)
                            elif self.v.x < 0:
                                   self.p = pygame.Vector2(rect.right + (.5 * self.hitbox.width), self.p.y)    
                            self.v = pygame.Vector2(-self.v.x, self.v.y)
                     if rect.colliderect(self.hitbox.move(self.v.xy)):   
                            if self.v.y < 0:
                                   self.p = pygame.Vector2(self.p.x, rect.bottom + (.5 * self.hitbox.height))
                            elif self.v.y > 0:
                                   self.p = pygame.Vector2(self.p.x, rect.top - (.5 * self.hitbox.height))    
                            self.v = pygame.Vector2(self.v.x, -self.v.y)
                     
              if c:
                     self.curbounces += 1
                            
       def update(self):
              self.p += self.v
              self.hitbox.center = self.p

       def move(self, rects):

              self.p.x += self.v.x
              self.hitbox.center = self.p
              
              for rect in rects:
                     if self.hitbox.colliderect(rect):
                            self.v.x = -self.v.x
                            self.p.x += 2 * self.v.x
                            self.hitbox.center = self.p
                            break
              
              self.p.y += self.v.y
              self.hitbox.center = self.p

              for rect in rects:
                     if self.hitbox.colliderect(rect):
                            self.v.y = -self.v.y
                            self.p.y += 2 * self.v.y
                            self.hitbox.center = self.p
                            break
              self.hitbox.center = self.p
       
       def draw(self):
              pygame.draw.circle(self.surface, (255, 0, 0), self.p, self.r)