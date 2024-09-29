from settings import *

class BaseEntity(pg.sprite.Sprite):
    def __init__(self, app, name):
        self.app = app
        self.name = name
        self.group = app.main_group
        super().__init__(self.group)

        self.attrs = ENTITY_SPRITE_ATTRS[name]
        entity_cache = self.app.cache.entity_sprite_cache
        self.images = entity_cache[name]['images']
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.frame_index = 0

    def animate(self):
        if self.app.anim_trigger:
            self.frame_index = (self.frame_index + 1) % len(self.images)
            self.image = self.images[self.frame_index]

    def update(self):
        self.animate()


class Entity(BaseEntity):
    def __init__(self, app, name, pos):
        super().__init__(app, name)
        self.pos = vec2(pos) * TILE_SIZE
        self.player = app.player
        self.y_offset = vec2(0, self.attrs['y_offset'])
        self.screen_pos = vec2(0)
        self.conversation_history = []
        self.character_profile = self.get_character_profile()

    def update(self):
        super().update()
        self.transform()
        self.set_rect()
        self.change_layer()

    def transform(self):
        pos = self.pos - self.player.offset
        pos = pos.rotate_rad(self.player.angle)
        self.screen_pos = pos + CENTER

    def change_layer(self):
        self.group.change_layer(self, self.screen_pos.y)

    def set_rect(self):
        self.rect.center = self.screen_pos + self.y_offset

    def add_to_conversation(self, message, sender):
        self.conversation_history.append({"sender": sender, "message": message})

    def get_conversation_history(self):
        return self.conversation_history

    def get_character_profile(self):
        profiles = {
            'kitty': "You are a curious and playful kitten named Whiskers. You speak in short, simple sentences and often use cat-like expressions. You're always eager to learn about the world around you and make new friends.",
            'blue_tree': "You are an ancient, wise tree spirit named Elderbark. You speak slowly and thoughtfully, often using nature metaphors. You have vast knowledge about the forest and its history.",
            'car': "You are a sentient car named Speedy. You're energetic and love to talk about racing and adventures on the road. You use a lot of car-related puns and metaphors.",
            'van': "You are a laid-back, hippie-style van named Groovy. You speak in a relaxed manner, often using 60s and 70s slang. You love to talk about travel and the 'good old days'.",
            'tank': "You are a retired military tank named Sarge. You speak in a gruff, no-nonsense manner, often using military jargon. You have a strong sense of duty and discipline."
            # Add more profiles for other entity types as needed
        }
        return profiles.get(self.name, "You are a mysterious character in this world. Be creative and develop your own personality based on your appearance and surroundings.")