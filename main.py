import sys
import pygame
import bullet
import lvl
import slingshot
import asyncio

async def main():
       pygame.init()

       WIDTH = 600
       HEIGHT = 400

       screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE | pygame.SCALED)
       pygame.display.set_icon(screen)
       pygame.display.set_caption("Ricochet")
       clock = pygame.time.Clock()
       font = pygame.font.Font(None, 32)
       
       running = True

       l = lvl.Generate(screen)
       plr = l[0]
       enms = l[1]
       walls = l[2]

       s = slingshot.Slingshot(screen, plr.p, 8, 8, plr)
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
                            s.shoot()
                     if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                   plr.keys += 1
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

              screen.fill((0, 150, 0))

              for rect in walls:
                     if rect.tag == "shed":
                            pygame.draw.rect(screen, (150, 75, 0), rect)
                     else:
                            pygame.draw.rect(screen, (255,255,255), rect)
              plr.draw() 
              for e in enms:
                     e.track(plr, walls)
                     e.cols(walls)
                     e.update()
                     if e.clearshot and e.curshotcd == 0:
                            eb = bullet.Bullet(screen, e.p, 5, 10, e.dir)
                            eb.baseDamage = 5
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
                            enms[ind].takeDamage(pb.hit(), enms)
                     pb.draw()
              predict_bounce()
              s.p = plr.p
              s.draw()

              text = font.render(f"Keys: {plr.keys}", True, (255, 255, 255))
              screen.blit(text, (20, 20))
              pygame.display.flip()
              clock.tick(60)
              await asyncio.sleep(0)

       pygame.quit()
       sys.exit()

asyncio.run(main())