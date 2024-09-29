import sys
import pygame as pg
from settings import *
from stacked_sprite import StackedSprite
from cache import Cache
from player import Player
from scene import Scene
from terrain import Terrain
from chat_interface import ChatInterface
from entity import Entity

class App:
    def __init__(self):
        pg.init()
        pg.font.init()

        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0.01
        self.anim_trigger = False
        self.anim_event = pg.USEREVENT + 0
        pg.time.set_timer(self.anim_event, 100)
        # groups
        self.main_group = pg.sprite.LayeredUpdates()
        self.transparent_objects = []
        # game objects
        self.cache = Cache()
        self.player = Player(self)
        self.scene = Scene(self)
        self.terrain = Terrain(self)
        # Initialize Chat Interface
        self.chat_interface = ChatInterface(self)
        
        self.running = True

    def update(self):
        self.scene.update()
        self.main_group.update()
        self.chat_interface.update()
        pg.display.set_caption(f'{self.clock.get_fps(): .1f}')
        self.delta_time = self.clock.tick(60)

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.main_group.draw(self.screen)
        # self.terrain.render(self.screen)

        # Draw collision shapes
        for sprite in self.main_group:
            if hasattr(sprite, 'draw_collision_shape'):
                sprite.draw_collision_shape(self.screen)
        
        self.chat_interface.draw(self.screen)
        pg.display.flip()

    def check_events(self):
        self.anim_trigger = False
        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
                self.running = False
            elif e.type == self.anim_event:
                self.anim_trigger = True
            self.chat_interface.handle_event(e)

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def find_nearby_entities(self):
        nearby_entities = []
        chat_radius = WIDTH // 5  # One fifth of the screen width
        for entity in self.main_group:
            if isinstance(entity, Entity) and entity != self.player:
                distance = (entity.pos - self.player.offset).length()
                if distance <= chat_radius:
                    nearby_entities.append(entity)
        return nearby_entities

    def run(self):
        while self.running:
            self.check_events()
            self.get_time()
            self.update()
            self.draw()

def main():
    app = App()
    app.run()

if __name__ == '__main__':
    main()