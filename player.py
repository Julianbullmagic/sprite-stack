from entity import BaseEntity
from settings import *
import math


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
        self.debug = True


    def check_collisions(self):
        player_world_pos = self.offset
        for sprite in self.app.main_group:
            if hasattr(sprite, 'collision_shape') and sprite != self:
                if self.collides_with(sprite, player_world_pos):
                    if self.debug:
                        print(f"Collision detected with {sprite.name} at {sprite.pos}")
                    self.handle_collision(sprite, player_world_pos)
                elif self.debug and self.is_close_to(sprite, player_world_pos):
                    print(f"Close to {sprite.name} at {sprite.pos}")

    def collides_with(self, sprite, player_world_pos):
        if isinstance(sprite.collision_shape, pg.Rect):
            return sprite.collision_shape.collidepoint(player_world_pos)
        elif isinstance(sprite.collision_shape, tuple):
            shape_pos, shape_radius = sprite.collision_shape
            return (player_world_pos - shape_pos).length() < (self.collision_radius + shape_radius)
        return False

    def is_close_to(self, sprite, player_world_pos):
        distance = (player_world_pos - sprite.pos).length()
        return distance < 100  # Adjust this value as needed

    def handle_collision(self, sprite, player_world_pos):
        if isinstance(sprite.collision_shape, pg.Rect):
            collision_normal = self.get_rect_collision_normal(player_world_pos, sprite.collision_shape)
        elif isinstance(sprite.collision_shape, tuple):
            collision_normal = self.get_circle_collision_normal(player_world_pos, sprite.collision_shape[0])
        else:
            return

        if self.debug:
            print(f"Collision normal with {sprite.name}: {collision_normal}")

        dot_product = self.inc.dot(collision_normal)
        
        if dot_product < 0:  # Moving towards the object
            self.offset -= self.inc  # Move back to previous position
            if self.debug:
                print(f"Moving back, new position: {self.offset}")
            
            # Slide along the object if collision is not head-on
            if abs(dot_product) < 0.9:  # Adjust this threshold as needed
                slide_vector = self.inc - collision_normal * dot_product
                self.offset += slide_vector
                if self.debug:
                    print(f"Sliding, new position: {self.offset}")

    def get_rect_collision_normal(self, player_world_pos, rect):
        closest_point = vec2(
            max(rect.left, min(player_world_pos.x, rect.right)),
            max(rect.top, min(player_world_pos.y, rect.bottom))
        )
        
        difference = player_world_pos - closest_point
        
        if difference.length_squared() < 1e-10:
            # If player is inside the rectangle, push them out in the direction of the nearest edge
            edges = [
                (vec2(1, 0), rect.right - player_world_pos.x),
                (vec2(-1, 0), player_world_pos.x - rect.left),
                (vec2(0, 1), rect.bottom - player_world_pos.y),
                (vec2(0, -1), player_world_pos.y - rect.top)
            ]
            normal, _ = min(edges, key=lambda x: x[1])
            return normal
        
        return difference.normalize()

    def get_circle_collision_normal(self, player_world_pos, circle_center):
        difference = player_world_pos - circle_center
        
        if difference.length_squared() < 1e-10:
            return vec2(1, 0)  # Return an arbitrary normal if player is at the center
        
        return difference.normalize()

    def update(self):
        super().update()
        self.control()
        self.move()
        self.check_collisions()

    def move(self):
        self.offset += self.inc

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

