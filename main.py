import sys
import pygame
import random
import player
import bullet
import lvl
import slingshot

pygame.init()

WIDTH = 600
HEIGHT = 400

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE | pygame.SCALED)
pygame.display.set_icon(screen)
pygame.display.set_caption("Ricochet")
clock = pygame.time.Clock()
    
running = True

l = lvl.Generate(screen)
plr = l[0]
enms = l[1]
walls = l[2]

s = slingshot.Slingshot(screen, plr.p, 8, 8)
def predict_bounce():
       direction = pygame.Vector2((pygame.mouse.get_pos()) - plr.p).normalize()
       position = pygame.Vector2(plr.p.xy)
       test_hitbox = pygame.Rect(0, 0, 10, 10)
       test_hitbox.center = position
       for _ in range(200):
              position.x += direction.x * 10
              test_hitbox.center = position
              for rect in walls:
                     if test_hitbox.colliderect(rect):
                            pygame.draw.line(screen, (0, 255, 0), position, position - direction * 10, 2)
                            direction.x = -direction.x
                            pygame.draw.line(screen, (0, 255, 0), position, position + direction * 10, 2)
                            position.x += direction.x * 20
                            break

              position.y += direction.y * 10
              test_hitbox.center = position
              for rect in walls:
                     if test_hitbox.colliderect(rect):
                            pygame.draw.line(screen, (0, 255, 0), position, position - direction * 10, 2)
                            direction.y = -direction.y
                            pygame.draw.line(screen, (0, 255, 0), position, position + direction * 10, 2)
                            position.y += direction.y * 20
                            break

while running:
       for event in pygame.event.get():
              if event.type == pygame.QUIT:
                    running = False
              if event.type == pygame.MOUSEBUTTONDOWN:
                     b = bullet.Bullet(screen, plr.p, 5, 10, pygame.Vector2((pygame.mouse.get_pos()) - plr.p).normalize())
                     bullet.pbullets.append(b)
                     print(pygame.mouse.get_pos())
       keys = pygame.key.get_pressed()

       i = pygame.Vector2(0, 0)      
       if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
              i += (1, 0)
       if keys[pygame.K_LEFT] or keys[pygame.K_a]:
              i += (-1, 0)
       if keys[pygame.K_UP] or keys[pygame.K_w]:
              i += (0, -1)
       if keys[pygame.K_DOWN] or keys[pygame.K_s]:
              i += (0, 1)
       plr.movement(i)                                                                                                                                           
       plr.cols(walls)
       plr.update()

       screen.fill((20, 24, 40))

       for rect in walls:
              pygame.draw.rect(screen, (255,255,255), rect)
       plr.draw() 
       for e in enms:
              e.track(plr)
              e.cols(walls)
              e.update()
              if e.clearshot and e.curshotcd == 0:
                     eb = bullet.Bullet(screen, e.p, 5, 10, e.dir)
                     bullet.ebullets.append(eb)
                     e.curshotcd = e.shotcooldown
              e.draw()
       for eb in bullet.ebullets [:]:
              eb.cols(walls)
              eb.update()
              if eb.curbounces >= eb.maxbounces:
                     bullet.ebullets.remove(eb)
              if eb.hitbox.colliderect(plr.hitbox):
                     plr.takeDamage(eb.hit())
              eb.draw() 
       for pb in bullet.pbullets [:]:
              pb.cols(walls)
              pb.update()
              if pb.curbounces >= pb.maxbounces:
                     bullet.pbullets.remove(pb)
              ind = pb.hitbox.collidelist([e.hitbox for e in enms])
              if(ind != -1):
                     enms[ind].takeDamage(eb.hit(), enms)
              pb.draw()
       predict_bounce()
       s.p = plr.p
       s.draw()

       pygame.display.flip()
       clock.tick(60)
       
pygame.quit()
sys.exit()
