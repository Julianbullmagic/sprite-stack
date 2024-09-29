from settings import *
import math
from entity import BaseEntity


class Player(BaseEntity):
    def __init__(self, app, name='player'):
        super().__init__(app, name)
        self.group.change_layer(self, CENTER.y)

        self.rect = self.image.get_rect(center=CENTER)
        self.offset = vec2(0)
        self.inc = vec2(0)
        self.angle = 0
        self.diag_move_corr = 1 / math.sqrt(2)
        self.collision_radius = 20 

    def control(self):
        self.inc = vec2(0)
        speed = PLAYER_SPEED * self.app.delta_time
        rot_speed = PLAYER_ROT_SPEED * self.app.delta_time

        key_state = pg.key.get_pressed()

        if key_state[pg.K_LCTRL]:
            self.angle += rot_speed
        if key_state[pg.K_RCTRL]:
            self.angle -= rot_speed

        if key_state[pg.K_UP]:
            self.inc += vec2(0, -speed).rotate_rad(-self.angle)
        if key_state[pg.K_DOWN]:
            self.inc += vec2(0, speed).rotate_rad(-self.angle)
        if key_state[pg.K_LEFT]:
            self.inc += vec2(-speed, 0).rotate_rad(-self.angle)
        if key_state[pg.K_RIGHT]:
            self.inc += vec2(speed, 0).rotate_rad(-self.angle)

        if self.inc.x and self.inc.y:
            self.inc *= self.diag_move_corr

    def update(self):
        super().update()
        self.control()
        self.move()
        self.check_collisions()


    def move(self):
        self.offset += self.inc
    
    def check_collisions(self):
        print("Checking collisions")
        for sprite in self.app.main_group:
            if hasattr(sprite, 'collision_shape') and sprite != self:
                if self.collides_with(sprite.collision_shape):
                    print(f"Collision detected with {sprite.name}")
                    self.handle_collision(sprite)
        print("Collision check completed")

    def collides_with(self, shape):
        player_pos = CENTER + self.offset
        if isinstance(shape, pg.Rect):
            return shape.collidepoint(player_pos)
        elif isinstance(shape, tuple):
            return (player_pos - shape[0]).length() < (self.collision_radius + shape[1])
        return False

    def handle_collision(self, sprite):
        print(f"Handling collision with {sprite.name}")
        player_pos = CENTER + self.offset
        collision_normal = (player_pos - sprite.pos).normalize()
        dot_product = self.inc.dot(collision_normal)
        
        if dot_product < 0:  # Moving towards the object
            self.offset -= self.inc  # Move back to previous position
            
            # Slide along the object if collision is not head-on
            if abs(dot_product) < 0.9:  # Adjust this threshold as needed
                slide_vector = self.inc - collision_normal * dot_product
                self.offset += slide_vector
        print("Collision handled")