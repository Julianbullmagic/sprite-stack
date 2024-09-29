import pygame as pg
import threading
import requests
import json
from queue import Queue
from settings import *

class ChatInterface:
    def __init__(self, app):
        self.app = app
        self.font = self.initialize_font()
        
        self.padding = 20
        self.chat_box = pg.Rect(self.padding, HEIGHT - 230, WIDTH - 2*self.padding, 220)
        self.message_area = pg.Rect(self.chat_box.x + self.padding, self.chat_box.y + self.padding, 
                                    self.chat_box.width - 2*self.padding, self.chat_box.height - 60)
        self.input_box = pg.Rect(self.chat_box.x + self.padding, HEIGHT - 50, WIDTH - 4*self.padding - 80, 30)
        self.send_button = pg.Rect(self.input_box.right + self.padding, HEIGHT - 50, 70, 30)
        
        self.color_inactive = pg.Color('lightskyblue3')
        self.color_active = pg.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = ''
        self.active = False
        self.current_entity = None
        self.in_range_message = ""
        self.waiting_for_response = False
        
        self.message_queue = Queue()
        self.response_thread = threading.Thread(target=self.process_messages, daemon=True)
        self.response_thread.start()

    def initialize_font(self):
        try:
            return pg.font.Font(None, 24)
        except pg.error:
            try:
                return pg.font.SysFont(None, 24)
            except pg.error:
                print("Warning: Could not load any font. Text rendering will be disabled.")
                return None

    def render_text(self, text, color):
        if self.font:
            return self.font.render(text, True, color)
        else:
            print(f"Text rendering disabled: {text}")
            return pg.Surface((0, 0))

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos):
                self.active = True
            elif self.send_button.collidepoint(event.pos):
                self.send_message(self.text)
                self.text = ''
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.send_message(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def send_message(self, message):
        if message.strip() and self.current_entity:
            self.current_entity.add_to_conversation("You", message)
            self.message_queue.put(message)
            self.waiting_for_response = True

    def process_messages(self):
        while True:
            message = self.message_queue.get()
            if self.current_entity:
                conversation_for_qwen = [
                    {"role": "system", "content": self.current_entity.character_profile},
                    {"role": "user", "content": "Let's start our conversation. Remember to stay in character."},
                    {"role": "assistant", "content": "Understood, I'll stay in character. How may I assist you today?"}
                ]
                
                for msg in self.current_entity.get_conversation_history():
                    role = "user" if msg["sender"] == "You" else "assistant"
                    conversation_for_qwen.append({"role": role, "content": msg["message"]})
                
                conversation_for_qwen.append({"role": "user", "content": message})
                
                try:
                    response = requests.post('http://localhost:11434/api/chat', 
                                             json={"model": "qwen2.5:1.5b", "messages": conversation_for_qwen},
                                             stream=True)
                    response.raise_for_status()
                    
                    full_response = ""
                    for line in response.iter_lines():
                        if line:
                            try:
                                chunk = json.loads(line)
                                if 'message' in chunk and 'content' in chunk['message']:
                                    full_response += chunk['message']['content']
                                if chunk.get('done', False):
                                    break
                            except json.JSONDecodeError as json_err:
                                print(f"JSON Decode Error: {json_err}")
                                print("Response chunk:", line)
                    
                    print("Full response:", full_response)
                    self.current_entity.add_to_conversation(self.current_entity.name, full_response)
                except requests.RequestException as req_err:
                    print(f"Request Error: {req_err}")
                    self.current_entity.add_to_conversation(self.current_entity.name, "Sorry, I'm having trouble connecting to the AI service.")
                except Exception as e:
                    print(f"Error processing response from qwen2.5:1.5b: {e}")
                    self.current_entity.add_to_conversation(self.current_entity.name, "Sorry, I'm having trouble understanding the response.")
                finally:
                    self.waiting_for_response = False

    def update(self):
        nearby_entities = self.app.find_nearby_entities()
        if nearby_entities:
            self.current_entity = nearby_entities[0]  # For simplicity, use the first nearby entity
            self.in_range_message = f"You can talk to {self.current_entity.name}"
        else:
            self.current_entity = None
            self.in_range_message = ""

    def draw(self, screen):
        # Draw chat box background
        pg.draw.rect(screen, pg.Color('white'), self.chat_box)
        pg.draw.rect(screen, pg.Color('black'), self.chat_box, 2)

        # Draw in-range message
        if self.in_range_message:
            message_surface = self.render_text(self.in_range_message, pg.Color('green'))
            screen.blit(message_surface, (self.chat_box.x + self.padding, self.chat_box.y + self.padding))

        # Draw messages
        if self.current_entity:
            conversation = self.current_entity.get_conversation_history()
            y = self.message_area.top + 30  # Start below the in-range message
            for message in conversation[-7:]:  # Display last 7 messages to make room for the in-range message
                sender = message['sender']
                content = message['message']
                full_message = f"{sender}: {content}"
                
                words = full_message.split()
                line = ''
                for word in words:
                    test_line = line + word + ' '
                    test_surface = self.render_text(test_line, pg.Color('black'))
                    if test_surface.get_width() > self.message_area.width:
                        text_surface = self.render_text(line, pg.Color('black'))
                        screen.blit(text_surface, (self.message_area.x, y))
                        y += 25
                        line = word + ' '
                    else:
                        line = test_line
                text_surface = self.render_text(line, pg.Color('black'))
                screen.blit(text_surface, (self.message_area.x, y))
                y += 25

        # Draw input box
        pg.draw.rect(screen, self.color, self.input_box, 2)
        text_surface = self.render_text(self.text, self.color)
        screen.blit(text_surface, (self.input_box.x + 5, self.input_box.y + 5))

        # Draw send button
        pg.draw.rect(screen, pg.Color('lightblue'), self.send_button)
        pg.draw.rect(screen, pg.Color('black'), self.send_button, 2)
        send_text = self.render_text('Send', pg.Color('black'))
        send_text_rect = send_text.get_rect(center=self.send_button.center)
        screen.blit(send_text, send_text_rect)

        # Draw waiting message
        if self.waiting_for_response:
            waiting_text = self.render_text("Waiting for response...", pg.Color('red'))
            screen.blit(waiting_text, (self.chat_box.x + self.padding, self.chat_box.bottom - 30))