import pygame as pg
import math
import random
from settings import *


class StackedSprite(pg.sprite.Sprite):
    def __init__(self, app, name, pos, rot=0, is_grass=False):
        self.app = app
        self.name = name
        self.pos = vec2(pos) * TILE_SIZE
        self.player = app.player
        self.group = app.main_group
        super().__init__(self.group)

        self.attrs = STACKED_SPRITE_ATTRS[name]
        self.y_offset = vec2(0, self.attrs['y_offset'])
        self.cache = app.cache.stacked_sprite_cache
        self.viewing_angle = app.cache.viewing_angle
        self.rotated_sprites = self.cache[name]['rotated_sprites'].copy()
        self.angle = 0
        self.screen_pos = vec2(0, 0)
        self.rot = (rot % 360) // self.viewing_angle
        self.is_grass = is_grass

        # Initialize image and rect
        self.image = self.rotated_sprites[0]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        # Add collision shape after rect is created
        self.collision_shape = self.create_collision_shape()

    def create_collision_shape(self):
        if self.name in ['house1', 'house2', 'house3', 'house4', 'house5', 'house6', 'stores', 'store2']:
            # Rectangular collision for buildings
            width = self.attrs.get('collision_width', self.rect.width * 0.8)
            height = self.attrs.get('collision_height', self.rect.height * 0.5)
            return pg.Rect(self.pos.x - width / 2, self.pos.y - height / 2, width, height)
        elif self.name in ['blue_tree', 'redtree', 'tree2', 'tree3', 'tree4', 'tree5', 'fountain', 'car', 'van', 'tank']:
            # Circular collision for trees, fountain, and vehicles
            radius = self.attrs.get('collision_radius', min(self.rect.width, self.rect.height) * 0.3)
            return (self.pos, radius)
        else:
            return None

    def update(self):
        self.transform()
        self.get_angle()
        self.get_image()
        self.change_layer()

    def draw_collision_shape(self, screen):
        if self.collision_shape:
            transformed_pos = (self.pos - self.player.offset).rotate_rad(self.player.angle) + CENTER
            if isinstance(self.collision_shape, pg.Rect):
                rect = self.collision_shape.copy()
                rect.center = transformed_pos
                pg.draw.rect(screen, (255, 0, 0), rect, 2)
            elif isinstance(self.collision_shape, tuple):
                pg.draw.circle(screen, (255, 0, 0), transformed_pos, self.collision_shape[1], 2)


    def generate_tint(self):
        if self.name.startswith('grass'):
            # Exaggerated green tint for grass
            r = random.randint(100, 200)
            g = random.randint(180, 255)
            b = random.randint(100, 200)
        else:  # For trees
            # Exaggerated brownish-green tint for trees
            r = random.randint(120, 220)
            g = random.randint(140, 240)
            b = random.randint(80, 180)
        
        # Increase overall brightness to make tint more noticeable
        brightness_factor = random.uniform(1.1, 1.3)
        r = min(255, int(r * brightness_factor))
        g = min(255, int(g * brightness_factor))
        b = min(255, int(b * brightness_factor))
        
        return (r, g, b)

    def apply_tint_to_sprites(self):
        for angle in self.rotated_sprites:
            original_sprite = self.rotated_sprites[angle]
            tinted_sprite = pg.Surface(original_sprite.get_size(), pg.SRCALPHA)
            tinted_sprite.blit(original_sprite, (0, 0))
            tinted_sprite.fill(self.tint, special_flags=pg.BLEND_RGB_MULT)
            self.rotated_sprites[angle] = tinted_sprite


    def update_collision_shape(self):
        if isinstance(self.collision_shape, pg.Rect):
            self.collision_shape.center = self.pos
        elif isinstance(self.collision_shape, tuple):
            self.collision_shape = (self.pos, self.collision_shape[1])

    def transform(self):
        pos = (self.pos - self.player.offset).rotate_rad(self.player.angle)
        self.screen_pos = vec2(int(pos.x + CENTER.x), int(pos.y + CENTER.y))

    def get_angle(self):
        angle = -math.degrees(self.player.angle) // self.viewing_angle + self.rot
        self.angle = int(angle % NUM_ANGLES)

    def get_image(self):
        self.image = self.rotated_sprites[self.angle]
        self.rect = self.image.get_rect(center=(int(self.screen_pos.x + self.y_offset.x), 
                                                int(self.screen_pos.y + self.y_offset.y)))

    def change_layer(self):
        if self.is_grass:
            self.group.change_layer(self, -float('inf'))
        else:
            self.group.change_layer(self, round(self.pos.y))

    def get_world_rect(self):
        # Return a rect representing the sprite's position in the world
        return pg.Rect(self.pos.x - self.original_size[0] / 2,
                       self.pos.y - self.original_size[1] / 2,
                       self.original_size[0],
                       self.original_size[1])


class TrnspStackedSprite(StackedSprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app.transparent_objects.append(self)
        self.dist_to_player = 0.0
        self.alpha_trigger = False

    def get_alpha_image(self):
        if self.alpha_trigger:
            if self.rect.centery > self.player.rect.top:
                if self.rect.contains(self.player.rect):
                    self.image = self.image.copy()
                    self.image.set_alpha(70)

    def get_dist_to_player(self):
        self.dist_to_player = self.screen_pos.distance_to(self.player.rect.center)

    def update(self):
        super().update()
        self.get_dist_to_player()

    def get_image(self):
        super().get_image()
        self.get_alpha_image()