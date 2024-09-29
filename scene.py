from stacked_sprite import *
from random import uniform
from entity import Entity

P = 'player'
K = 'kitty'  # entity
A, B, C, D, E, h1, h2, h3, h4, h5, h6, st, st2, rt, t2, t3, t4, t5, g, t, f = 'van', 'tank', 'blue_tree', 'car', 'grass','house1','house2','house3','house4','house5','house6','stores','store2','redtree','tree2','tree3','tree4','tree5','grass2','trellis','fountain'

MAP = [
    [h1, f, g, g, K, t5, t5, 0, h2],
    [g, g, g, g, g, g, g, t4, K],
    [t4, g, 0, t, g, t4, E, g, h4],
    [g, g, g, E, g, g, f, g, 0],
    [g, E, h5, g, P, E, g, g, h3],
    [g, st2, g, A, E, D, t4, g, 0],
    [K, g, g, g, t5, t4, g, g, g],
    [rt, g, g, g, E, t4, g, g, t5],
    [h6, st, h5, g, g, g, g, K, 0],
]

MAP_SIZE = MAP_WIDTH, MAP_HEIGHT = vec2(len(MAP), len(MAP[0]))
MAP_CENTER = MAP_SIZE / 2

class Scene:
    def __init__(self, app):
        self.app = app
        self.load_scene()

    def load_scene(self):
        # First, create all grass objects
        for j, row in enumerate(MAP):
            for i, name in enumerate(row):
                if name in ['grass', 'grass2']:
                    self.create_sprite(name, i, j, is_grass=True)

        # Then create all other objects
        for j, row in enumerate(MAP):
            for i, name in enumerate(row):
                pos = vec2(i, j) + vec2(0.5)
                if name == 'player':
                    self.app.player.offset = pos * TILE_SIZE
                elif name == 'kitty':
                    Entity(self.app, name=name, pos=pos)
                elif name and name not in ['grass', 'grass2']:
                    self.create_sprite(name, i, j, is_grass=False)

    def create_sprite(self, name, i, j, is_grass):
        pos = vec2(i, j) + vec2(0.5)
        attrs = STACKED_SPRITE_ATTRS[name]
        if attrs['initial_rotation'] == 'random':
            rot = uniform(0, 360)
        else:
            rot = attrs['initial_rotation']
        
        StackedSprite(self.app, name=name, pos=pos, rot=rot, is_grass=is_grass)

    def get_closest_object_to_player(self):
        closest = sorted(self.app.transparent_objects, key=lambda obj: obj.dist_to_player)
        for obj in self.app.transparent_objects:
            obj.alpha_trigger = False
        if closest:
            closest[0].alpha_trigger = True

    def update(self):
        self.get_closest_object_to_player()










