from unittest import case

import pygame
import player
import enemy
walls = None
plr = None
PLAYER_WIDTH = 16
PLAYER_HEIGHT = 16
enemies = None

class TaggedRect(pygame.Rect):
    def __init__(self, x, y, width, height, sprite = None, tag="", flip_x = False, flip_y = False):
        super().__init__(x, y, width, height)
        self.tag = tag
        self.sprite = sprite
        if self.sprite != None:
            self.sprite = pygame.image.load(f"Assets/Images/{self.sprite}.png").convert_alpha()
            self.sprite = pygame.transform.flip(self.sprite, flip_x, flip_y)
            self.sprite = pygame.transform.scale(self.sprite, (50, 50))


def Generate(screen):
    plr = player.Player(screen, (150,200), PLAYER_WIDTH, PLAYER_HEIGHT)
    enemies = [
        enemy.Enemy(screen, (450,200), PLAYER_WIDTH, PLAYER_HEIGHT)
        ]
    walls = [
        TaggedRect(50, 50, 50, 50, sprite = "plant_c", flip_y = True),
        TaggedRect(50, 100, 50, 50, sprite = "plant_t", flip_y = True),
        TaggedRect(100, 50, 50, 50, sprite = "plant_b", flip_y = True),
        TaggedRect(50, 250, 50, 50, sprite = "plant_t"),
        TaggedRect(50, 300, 50, 50, sprite = "plant_c"),
        TaggedRect(100, 300, 50, 50, sprite = "plant_b"),
        TaggedRect(450, 50, 50, 50, sprite = "plant_b", flip_x = True, flip_y = True),
        TaggedRect(500, 100, 50, 50, sprite = "plant_t", flip_x = True, flip_y = True),
        TaggedRect(500, 50, 50, 50, sprite = "plant_c", flip_x = True, flip_y = True),
        TaggedRect(500, 250, 50, 50, sprite = "plant_t", flip_x = True),
        TaggedRect(500, 300, 50, 50, sprite = "plant_c", flip_x = True),
        TaggedRect(450, 300, 50, 50, sprite = "plant_b", flip_x = True),
        TaggedRect(250, 150, 100, 100),
        TaggedRect(275, 0, 50, 50, tag = "shed")
        ]
    return (plr, enemies, walls)