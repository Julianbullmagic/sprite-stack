import pygame as pg
import math
from settings import vec2, PLAYER_SPEED, PLAYER_ROT_SPEED, CENTER, TILE_SIZE
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
        self.debug = True

    def update(self):
        super().update()
        self.control()
        self.move()

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

    def move(self):
        self.original_inc = self.inc.copy()
        self.check_collisions()
        self.offset += self.inc

    def check_collisions(self):
        player_world_pos = self.offset + self.inc
        for sprite in self.app.main_group:
            if hasattr(sprite, 'collision_shape') and sprite != self:
                if self.collides_with(sprite, player_world_pos):
                    if self.debug:
                        print(f"Collision detected with {sprite.name} at {sprite.pos}")
                    self.handle_collision(sprite, player_world_pos)

    def collides_with(self, sprite, player_world_pos):
        if isinstance(sprite.collision_shape, pg.Rect):
            return sprite.collision_shape.collidepoint(player_world_pos)
        elif isinstance(sprite.collision_shape, tuple):
            shape_pos, shape_radius = sprite.collision_shape
            return (player_world_pos - shape_pos).length() < (self.collision_radius + shape_radius)
        return False

    def handle_collision(self, sprite, player_world_pos):
        if isinstance(sprite.collision_shape, pg.Rect):
            collision_normal = self.get_rect_collision_normal(player_world_pos, sprite.collision_shape)
        elif isinstance(sprite.collision_shape, tuple):
            collision_normal = self.get_circle_collision_normal(player_world_pos, sprite.collision_shape[0])
        else:
            return

        collision_angle = self.calculate_collision_angle(self.inc, collision_normal)
        if self.debug:
            print(f"Collision with {sprite.name} at angle: {collision_angle:.2f} degrees")
            print(f"Collision normal: {collision_normal}")

        # Calculate slide movement
        self.inc = self.calculate_slide_movement(collision_normal, collision_angle)

        if self.debug:
            print(f"New movement after collision: {self.inc}")

    def calculate_slide_movement(self, collision_normal, collision_angle):
        # Ensure we're not dividing by zero
        if collision_angle == 0:
            return vec2(0, 0)

        # Calculate slide factor (1 at 90 degrees, 0 at 0 or 180 degrees)
        slide_factor = math.sin(math.radians(collision_angle))

        # Project movement onto the surface
        surface_tangent = vec2(-collision_normal.y, collision_normal.x)
        projected_movement = surface_tangent * self.inc.dot(surface_tangent)

        # Apply slide factor to projected movement
        slide_movement = projected_movement * slide_factor

        # Ensure minimum sliding speed
        min_slide_speed = 0.1 * PLAYER_SPEED
        if slide_movement.length() < min_slide_speed:
            slide_movement = slide_movement.normalize() * min_slide_speed

        return slide_movement

    def calculate_collision_angle(self, movement_vector, collision_normal):
        if movement_vector.length_squared() == 0:
            return 180.0

        movement_vector = movement_vector.normalize()
        collision_normal = collision_normal.normalize()

        dot_product = movement_vector.dot(collision_normal)
        dot_product = max(min(dot_product, 1), -1)

        angle_rad = math.acos(dot_product)
        angle_deg = math.degrees(angle_rad)

        return angle_deg

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

    def is_close_to(self, sprite, player_world_pos):
        distance = (player_world_pos - sprite.pos).length()
        return distance < 100  # Adjust this value as needed

    def toggle_debug(self):
        self.debug = not self.debug
        print(f"Debug mode: {'ON' if self.debug else 'OFF'}")