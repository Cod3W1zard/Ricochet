import pygame
import player

walls = None
plr = None
PLAYER_WIDTH = 16
PLAYER_HEIGHT = 16
enemies = None

class TaggedRect(pygame.Rect):
    def __init__(self, x, y, width, height, tag=""):
        super().__init__(x, y, width, height)
        self.tag = tag

def Generate(screen):
    plr = player.Player(screen, (150,200), PLAYER_WIDTH, PLAYER_HEIGHT)
    
    walls = [
        TaggedRect(50, 50, 50, 50),
        TaggedRect(50, 100, 50, 50),
        TaggedRect(100, 50, 50, 50),
        TaggedRect(50, 250, 50, 50),
        TaggedRect(50, 300, 50, 50),
        TaggedRect(100, 300, 50, 50),
        TaggedRect(450, 50, 50, 50),
        TaggedRect(500, 100, 50, 50),
        TaggedRect(500, 50, 50, 50),
        TaggedRect(500, 250, 50, 50),
        TaggedRect(500, 300, 50, 50),
        TaggedRect(450, 300, 50, 50),
        TaggedRect(250, 150, 100, 100),
        TaggedRect(275, 0, 50, 50, "shed")
        ]
    return (plr, enemies, walls)
