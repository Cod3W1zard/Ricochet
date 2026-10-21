import random
import sys
import pygame
import bullet
import enemy
import lvl
import slingshot
import asyncio

async def main():
       pygame.init()

       WIDTH = 600
       HEIGHT = 400
       DEBUG_LINE_LENGTH = 100
       
       screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE | pygame.SCALED)
       icon = pygame.image.load("Assets/Images/Player/chet00.png").convert_alpha()
       pygame.display.set_icon(icon)
       pygame.display.set_caption("Ricochet")
       clock = pygame.time.Clock()
       font_top = pygame.font.Font(None, 32)
       font_bottom = pygame.font.Font(None, 12)
       debug = False
       background = pygame.image.load("Assets/Images/background.png").convert_alpha()
       tile_width = background.get_width()
       tile_height = background.get_height()
       running = True

       l = lvl.Generate(screen)
       plr = l[0]
       enms = l[1]
       walls = l[2]

       s = slingshot.Slingshot(screen, plr.p, 8, 8, plr)
       def predict_bounce():
              direction = pygame.Vector2((pygame.mouse.get_pos()) - plr.p).normalize()
              position = s.p + (0,6)
              test_hitbox = pygame.Rect(0, 0, 12, 12)
              test_hitbox.center = position
              previous_collide = position.copy()
              collisions = []
              velocity = pygame.Vector2(direction.x * 10, direction.y * 10)
              for _ in range(DEBUG_LINE_LENGTH):
                     position.x += velocity.x
                     test_hitbox.center = position    
                     for rect in walls:
                            if test_hitbox.colliderect(rect):
                                   velocity.x = -velocity.x
                                   position.x += velocity.x
                                   test_hitbox.center = position
                                   collisions.append((previous_collide, position.copy()))
                                   previous_collide = position.copy()
                                   break
                                   
                     position.y += velocity.y
                     test_hitbox.center = position
              
                     for rect in walls:
                            if test_hitbox.colliderect(rect):
                                   velocity.y = -velocity.y
                                   position.y += velocity.y
                                   test_hitbox.center = position
                                   collisions.append((previous_collide, position.copy()))
                                   previous_collide = position.copy()
                                   break
                     test_hitbox.center = position
                     if len(collisions) > 4:
                            break
              if len(collisions) > 4:
                     pygame.draw.line(screen, (255, 0, 0), collisions[0][0], collisions[0][1], 2)
                     for col in collisions[1:4]:
                            pygame.draw.line(screen, (0, 255, 0), col[0], col[1], 2)
                     pygame.draw.line(screen, (0, 255, 0), collisions[-1][0], collisions[-1][1], 2)
              elif len(collisions) > 0:
                     pygame.draw.line(screen, (255, 0, 0), collisions[0][0], collisions[0][1], 2)
                     for col in collisions[1:]:
                            pygame.draw.line(screen, (0, 255, 0), col[0], col[1], 2)
                     pygame.draw.line(screen, (0, 255, 0), previous_collide, position, 2)
              else:
                     pygame.draw.line(screen, (255, 0, 0), previous_collide, position, 2)
                                                  
       while running:
              if plr.game_state == "play":
                     for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                   running = False
                            if event.type == pygame.MOUSEBUTTONDOWN and plr.state == "run":
                                   s.shoot()
                            if event.type == pygame.KEYDOWN:
                                   if event.key == pygame.K_F1:
                                          debug = not debug
                                   if event.key == pygame.K_k and debug:
                                          plr.keys += 1
                                   if event.key == pygame.K_LCTRL:
                                          enms.append(enemy.Enemy(screen, (random.uniform(0, 600), random.uniform(0, 400)), lvl.PLAYER_WIDTH, lvl.PLAYER_HEIGHT, plr))
                     
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
                    

                     if plr.state == "run":
                            plr.movement(i)      
                            if keys[pygame.K_SPACE]: 
                                   plr.dash(i)
                     if plr.state == "hitstun" or plr.state == "dead" or plr.state == "dash":
                            plr.drag()                                                                                                                              
                     plr.cols(walls)
                     plr.update()
                     for x in range(0, WIDTH, tile_width):
                            for y in range(0, HEIGHT, tile_height):
                                   screen.blit(background, (x, y))
       
                     for rect in walls:
                            if rect.sprite != None:
                                          screen.blit(rect.sprite, rect)
                     plr.draw() 
                     for e in enms:
                            if e.state == "pursue":
                                   e.track(plr, walls)
                                   if e.clearshot and e.curshotcd == 0:
                                          eb = bullet.Bullet(screen, e.p, 5, 10, e.dir, type = "enemy")
                                          bullet.ebullets.append(eb)
                                          e.curshotcd = e.shotcooldown
                            if e.state == "hitstun" or e.state == "dead":
                                   e.hurt()
                            e.cols(walls)
                            e.update()                            
                            e.draw()
                     for key in enemy.Enemy.keylist[:]:
                            if plr.hitbox.colliderect(key):
                                   plr.keys += 1
                                   enemy.Enemy.keylist.remove(key)
                            else:
                                   screen.blit(enemy.Enemy.keyg, key)
                     for eb in bullet.ebullets [:]:
                            eb.move(walls)
                            if eb.curbounces >= eb.maxbounces:
                                   bullet.ebullets.remove(eb)
                            if eb.hitbox.colliderect(plr.hitbox) and plr.state != "dash":
                                   plr.takeDamage(eb)
                                   bullet.ebullets.remove(eb)
                            eb.draw() 
                     for pb in bullet.pbullets[:]:
                            pb.move(walls)
                            if pb.curbounces >= pb.maxbounces:
                                   bullet.pbullets.remove(pb)
                            ind = pb.hitbox.collidelist([e.hitbox for e in enms])
                            if ind != -1 and pb.curbounces != 0:
                                   enms[ind].takeDamage(pb, enms)
                                   bullet.pbullets.remove(pb)
                            pb.draw()
                     if debug:
                            predict_bounce()
                     s.p = plr.p
                     s.draw()

                     text = font_top.render(f"Keys: {plr.keys}", True, (255, 255, 255))
                     screen.blit(text, (20, 20))
                     text = font_bottom.render(f"Debug: F1", True, (255, 255, 255))
                     screen.blit(text, (12, 388))
              
              if plr.game_state == "win":
                     for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                   running = False
                            if event.type == pygame.KEYDOWN:
                                   if event.key == pygame.K_SPACE:
                                          l = lvl.Generate(screen)
                                          plr = l[0]
                                          enms = l[1]
                                          plr.keylist = []
                                          walls = l[2]
                                          plr.game_state = "play"
                     screen.fill((0,0,0))
                     text = font_top.render(f"You Win!", True, (255, 255, 255))
                     screen.blit(text, (300-text.get_width()/2, 200))
              
              pygame.display.flip()
              clock.tick(60)
              await asyncio.sleep(0)
       pygame.quit()
       sys.exit()

asyncio.run(main())
