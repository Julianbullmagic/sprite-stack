import os
import pygame as pg
from settings import *
import hashlib

class Cache:
    def __init__(self):
        self.stacked_sprite_cache = {}
        self.entity_sprite_cache = {}
        self.viewing_angle = 360 // NUM_ANGLES
        self.cache_dir = 'sprite_cache'
        os.makedirs(self.cache_dir, exist_ok=True)
        self.get_stacked_sprite_cache()
        self.get_entity_sprite_cache()

    def get_entity_sprite_cache(self):
        for sprite_name in ENTITY_SPRITE_ATTRS:
            self.entity_sprite_cache[sprite_name] = {
                'images': None,
            }
            attrs = ENTITY_SPRITE_ATTRS[sprite_name]
            images = self.get_layer_array(attrs)
            self.entity_sprite_cache[sprite_name]['images'] = images

    def get_stacked_sprite_cache(self):
        for obj_name in STACKED_SPRITE_ATTRS:
            self.stacked_sprite_cache[obj_name] = {
                'rotated_sprites': {},
            }
            attrs = STACKED_SPRITE_ATTRS[obj_name]
            
            # Check if cached sprites exist and are up-to-date
            if self.cached_sprites_exist(obj_name, attrs):
                self.load_cached_sprites(obj_name)
            else:
                layer_array = self.get_layer_array(attrs)
                self.run_prerender(obj_name, layer_array, attrs)
                self.save_cached_sprites(obj_name)

                

    def cached_sprites_exist(self, obj_name, attrs):
        cache_file = os.path.join(self.cache_dir, f"{obj_name}_cache_info.txt")
        if not os.path.exists(cache_file):
            return False
        
        with open(cache_file, 'r') as f:
            cached_hash = f.read().strip()
        
        current_hash = self.get_sprite_hash(attrs['path'])
        return cached_hash == current_hash

    def get_sprite_hash(self, sprite_path):
        with open(sprite_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()

    def load_cached_sprites(self, obj_name):
        for angle in range(NUM_ANGLES):
            image_path = os.path.join(self.cache_dir, f"{obj_name}_{angle}.png")
            self.stacked_sprite_cache[obj_name]['rotated_sprites'][angle] = pg.image.load(image_path).convert_alpha()

    def save_cached_sprites(self, obj_name):
        for angle, sprite in self.stacked_sprite_cache[obj_name]['rotated_sprites'].items():
            image_path = os.path.join(self.cache_dir, f"{obj_name}_{angle}.png")
            pg.image.save(sprite, image_path)
        
        # Save cache info
        attrs = STACKED_SPRITE_ATTRS[obj_name]
        cache_file = os.path.join(self.cache_dir, f"{obj_name}_cache_info.txt")
        with open(cache_file, 'w') as f:
            f.write(self.get_sprite_hash(attrs['path']))


    def run_prerender(self, obj_name, layer_array, attrs):
        outline = attrs.get('outline', True)

        for angle in range(NUM_ANGLES):
            surf = pg.Surface(layer_array[0].get_size(), pg.SRCALPHA)  # Use SRCALPHA
            surf = pg.transform.rotate(surf, angle * self.viewing_angle)
            sprite_surf = pg.Surface([surf.get_width(), surf.get_height()
                                      + attrs['num_layers'] * attrs['scale']], pg.SRCALPHA)  # Use SRCALPHA
            

            for ind, layer in enumerate(layer_array):
                layer = pg.transform.rotate(layer, angle * self.viewing_angle)
                sprite_surf.blit(layer, (0, ind * attrs['scale']))



            image = pg.transform.flip(sprite_surf, True, True)
            self.stacked_sprite_cache[obj_name]['rotated_sprites'][angle] = image




    def get_layer_array(self, attrs):
        # load sprite sheet
        sprite_sheet = pg.image.load(attrs['path']).convert_alpha()
        # scaling
        sprite_sheet = pg.transform.scale(sprite_sheet,
                                          vec2(sprite_sheet.get_size()) * attrs['scale'])
        sheet_width = sprite_sheet.get_width()
        sheet_height = sprite_sheet.get_height()
        sprite_height = sheet_height // attrs['num_layers']
        # new height to prevent error
        sheet_height = sprite_height * attrs['num_layers']
        # get sprites
        layer_array = []
        for y in range(0, sheet_height, sprite_height):
            sprite = sprite_sheet.subsurface((0, y, sheet_width, sprite_height))
            layer_array.append(sprite)
        return layer_array[::-1]