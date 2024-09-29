import pygame as pg

vec2 = pg.math.Vector2

RES = WIDTH, HEIGHT = vec2(1000, 600)
CENTER = H_WIDTH, H_HEIGHT = RES // 2
TILE_SIZE = 225

# Add these lines
MAP_SIZE = MAP_WIDTH, MAP_HEIGHT = vec2(9, 9)  # Adjust these values as needed

PLAYER_SPEED = 0.4
PLAYER_ROT_SPEED = 0.0015

BG_COLOR = 'olivedrab'
NUM_ANGLES = 180 

def calculate_y_offset(num_layers, scale):
    # The base of the sprite should be at the bottom of the lowest layer
    # We subtract 1 from num_layers because we want the offset from the center
    return -((num_layers - 1) * scale) // 2

# entity sprite settings
ENTITY_SPRITE_ATTRS = {
    'player': {
        'path': 'assets/entities/player/player.png',
        'num_layers': 7,
        'scale': 0.35,
        'y_offset': 0,
    },
    'kitty': {
        'path': 'assets/entities/cats/kitty.png',
        'num_layers': 8,
        'scale': 0.8,
        'y_offset': -20,
    },
}

# stacked sprites settings
STACKED_SPRITE_ATTRS = {
    'grass': {
        'path': 'assets/stacked_sprites/grass.png',
        'num_layers': 11,
        'scale': 11,
        'y_offset': calculate_y_offset(11, 11),
        'outline': False,
        'initial_rotation': 'random',
    },
        'trellis': {
        'path': 'assets/stacked_sprites/trellis.png',
        'num_layers': 19,
        'scale': 8,
        'y_offset': calculate_y_offset(19, 8),
        'initial_rotation': 0,
    },
    'blue_tree': {
        'path': 'assets/stacked_sprites/blue_tree.png',
        'num_layers': 43,
        'scale': 8,
        'y_offset': calculate_y_offset(43, 8),
        'initial_rotation': 'random',
    },
    'car': {
        'path': 'assets/stacked_sprites/car.png',
        'num_layers': 9,
        'scale': 10,
        'y_offset': calculate_y_offset(9, 10),
        'initial_rotation': 0,
    },
    'van': {
        'path': 'assets/stacked_sprites/van.png',
        'num_layers': 20,
        'scale': 6,
        'y_offset': calculate_y_offset(20, 6),
        'initial_rotation': 0,
    },
    'tank': {
        'path': 'assets/stacked_sprites/tank.png',
        'num_layers': 17,
        'scale': 5,
        'y_offset': calculate_y_offset(17, 5),
        'initial_rotation': 0,
    },
        'house1': {
        'path': 'assets/stacked_sprites/house1.png',
        'num_layers': 30,
        'scale': 5,
        'y_offset': calculate_y_offset(30, 5),
        'initial_rotation': 0,
    },
            'house2': {
        'path': 'assets/stacked_sprites/house2.png',
        'num_layers': 25,
        'scale': 5,
        'y_offset': calculate_y_offset(25, 5),
        'initial_rotation': 0,
    },
                'house3': {
        'path': 'assets/stacked_sprites/house3.png',
        'num_layers': 55,
        'scale': 5,
        'y_offset': calculate_y_offset(55, 5),
        'initial_rotation': 0,
    },
                    'house4': {
        'path': 'assets/stacked_sprites/house4.png',
        'num_layers': 64,
        'scale': 5,
        'y_offset': calculate_y_offset(64, 5),
        'initial_rotation': 0,
    },
                        'house5': {
        'path': 'assets/stacked_sprites/house5.png',
        'num_layers': 24,
        'scale': 5,
        'y_offset': calculate_y_offset(24, 5),
        'initial_rotation': 0,
    },
                            'house6': {
        'path': 'assets/stacked_sprites/house6.png',
        'num_layers': 64,
        'scale': 5,
        'y_offset': calculate_y_offset(64, 5),
        'initial_rotation': 0,
    },
                    'stores': {
        'path': 'assets/stacked_sprites/stores.png',
        'num_layers': 24,
        'scale': 5,
        'y_offset': calculate_y_offset(24, 5),
        'initial_rotation': 0,
    },
                        'store2': {
        'path': 'assets/stacked_sprites/store2.png',
        'num_layers': 24,
        'scale': 5,
        'y_offset': calculate_y_offset(24, 5),
        'initial_rotation': 0,
    },
                            'redtree': {
        'path': 'assets/stacked_sprites/redtree.png',
        'num_layers': 19,
        'scale': 8,
        'y_offset': calculate_y_offset(19, 8),
        'initial_rotation': 'random',
    },
                                'tree2': {
        'path': 'assets/stacked_sprites/tree2.png',
        'num_layers': 40,
        'scale': 8,
        'y_offset': calculate_y_offset(40,8),
        'initial_rotation': 'random',
    },
                                    'tree3': {
        'path': 'assets/stacked_sprites/tree3.png',
        'num_layers': 40,
        'scale': 8,
        'y_offset': calculate_y_offset(40, 8),
        'initial_rotation': 'random',
    },
                                        'tree4': {
        'path': 'assets/stacked_sprites/tree4.png',
        'num_layers': 40,
        'scale': 8,
        'y_offset': calculate_y_offset(40,8),
        'initial_rotation': 'random',
    },
                                            'tree5': {
        'path': 'assets/stacked_sprites/tree5.png',
        'num_layers': 32,
        'scale': 8,
        'y_offset': calculate_y_offset(32, 8),
        'initial_rotation': 'random',
    },
                                                'grass2': {
        'path': 'assets/stacked_sprites/grass2.png',
        'num_layers': 10,
        'scale': 6,
        'y_offset': calculate_y_offset(10, 6),
        'initial_rotation': 'random',
    },
                                                    'fountain': {
        'path': 'assets/stacked_sprites/fountain.png',
        'num_layers': 64,
        'scale': 6,
        'y_offset': calculate_y_offset(64, 6),
        'initial_rotation': 'random',
    },
}



















