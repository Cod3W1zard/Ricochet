import pygame
import sys
import random

pygame.init()

WIDTH = 600
HEIGHT = 400

SPEED = 5
FRICTION = 0.4
PLAYER_WIDTH = 16
PLAYER_HEIGHT = 16

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE | pygame.SCALED)
pygame.display.set_caption("Ricochet")
clock = pygame.time.Clock()
    
running = True

player_image = pygame.image.load("gnome_still.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH*2, PLAYER_HEIGHT*2))

rects = []

class Player:

       def __init__(self, surface, center, width, height):
              self.surface = surface
              self.center = pygame.Vector2(center)
              self.width = width
              self.height = height
              self.hitbox = pygame.Rect(0, 0, width*2, height*2)
              self.hitbox.center = self.center
       def move(self, dist: tuple | pygame.Vector2):
              dist = pygame.Vector2(dist)
              self.center += dist
              self.hitbox.center += dist
       def set(self, location: tuple | pygame.Vector2):
              location = pygame.Vector2(location)
              self.center = location
              self.hitbox.center = location
       def draw(self):
              image_rect = player_image.get_rect(center=self.center)
              self.surface.blit(player_image, image_rect)

player = Player(screen, (300,200), PLAYER_WIDTH, PLAYER_HEIGHT)
player_velocity = pygame.Vector2(0, 0)

while len(rects) < 10:
       rect = pygame.Rect(random.uniform(0, WIDTH - 50), random.uniform(0, HEIGHT - 50), 50, 50)
       if not rect.colliderect(player.hitbox):
              rects.append(rect)

while running:
       # EVENT
       for event in pygame.event.get():
        if event.type == pygame.QUIT:
                    running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
              print(pygame.mouse.get_pos())
       keys = pygame.key.get_pressed()

       previous_x = player.center.x
       previous_y = player.center.y


       if keys[pygame.K_LEFT]:
              player_velocity += (-SPEED, 0)
       if keys[pygame.K_RIGHT]:
              player_velocity += (SPEED, 0)
       if keys[pygame.K_UP]:
              player_velocity += (0, -SPEED)
       if keys[pygame.K_DOWN]:
              player_velocity += (0, SPEED)

       player.move((int(player_velocity.x), 0))
       for rect in rects:
              if player.hitbox.colliderect(rect):
                     player.set((previous_x, player.center.y))
                     player_velocity.x = 0

       player.move((0, int(player_velocity.y)))
       for rect in rects:
              if player.hitbox.colliderect(rect):
                     player.set((player.center.x, previous_y))
                     player_velocity.y = 0

       player_velocity *= FRICTION

       screen.fill((20, 24, 40))

       for rect in rects:
              pygame.draw.rect(screen, (255,255,255), rect)

       player.draw()

       pygame.display.flip()
       clock.tick(60)
    
    
pygame.quit()
sys.exit()
    