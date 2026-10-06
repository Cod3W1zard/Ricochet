import pygame
import player

walls = None
plr = None
PLAYER_WIDTH = 16
PLAYER_HEIGHT = 16
enemies = None

def Generate(screen):
    plr = player.Player(screen, (300,200), PLAYER_WIDTH, PLAYER_HEIGHT)
    walls = [
        pygame.Rect(50, 50, 50, 50),
        pygame.Rect(50, 100, 50, 50),
        pygame.Rect(100, 50, 50, 50),
        pygame.Rect(50, 250, 50, 50),
        pygame.Rect(50, 300, 50, 50),
        pygame.Rect(100, 300, 50, 50),
        pygame.Rect(450, 50, 50, 50),
        pygame.Rect(500, 100, 50, 50),
        pygame.Rect(500, 50, 50, 50),
        pygame.Rect(500, 250, 50, 50),
        pygame.Rect(500, 300, 50, 50),
        pygame.Rect(450, 300, 50, 50),
        pygame.Rect(250, 150, 100, 100),
        ]
    return (plr, enemies, walls)
