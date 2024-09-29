import pygame as pg
import math
from settings import *

class Terrain:
    def __init__(self, app):
        self.app = app
        # Load the image with original colors
        self.image = pg.image.load('D1.png').convert_alpha()
        
        # Scale the image to match the map size
        self.image = pg.transform.scale(self.image, (int(MAP_WIDTH * TILE_SIZE), int(MAP_HEIGHT * TILE_SIZE)))

    def render(self, screen):
        pos = -self.app.player.offset
        pos = pos.rotate_rad(self.app.player.angle)
        screen_pos = pos + CENTER
        rotated = pg.transform.rotate(self.image, -math.degrees(self.app.player.angle))
        rect = rotated.get_rect(center=screen_pos)
        screen.blit(rotated, rect.topleft)