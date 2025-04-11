import pygame
import sys
import colorsys

from pygame.locals import *

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 800
FONT_SIZE = 40
QUESTION_OFFSET = 50
ANSWER_OFFSET = 200
OPTION_HEIGHT = 50
BLACK = (0,0,0)

asciiartstart=(r"""
  ___                _            ___  ___                     __                        __
 / _ \     _   _    (_)    ____   |  \/  |     __ _     ___    | |_      ___     _ __    | |
| | | |   | | | |   | |   |_  /   | |\/| |    / _` |   / __|   | __|    / _ \   | '__|   | |
| |_| |   | |_| |   | |    / /    | |  | |   | (_| |   \__ \   | |_    |  __/   | |      |_|
 \__\_\    \__,_|   |_|   /___|   |_|  |_|    \__,_|   |___/    \__|    \___|   |_|      (_)
                                                                     
""")          

asciiartend=(r"""

 ____                         _ 
| __ )     _   _      ___    | |
|  _ \    | | | |    / _ \   | |
| |_) |   | |_| |   |  __/   |_|
|____/     \__, |    \___|   (_)
           |___/                

""")


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def quit():
    print(asciiartend)
    pygame.quit()
    sys.exit()

class Button:
    def __init__(self, text, position, width=0, height=0):
        self.text = text
        self.position = position
        self.font = pygame.font.Font(None, FONT_SIZE)
        text_width, text_height = self.font.size(text)
        self.width = max(width, text_width + 20)
        self.height = max(height, text_height + 20) 
        self.rect = pygame.Rect(position[0], position[1], width, height)

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, self.rect)
        font = pygame.font.Font(None, FONT_SIZE)
        label = font.render(self.text, True, BLACK)
        text_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Scrollbar:
    def __init__(self, position, height, total_items, items_per_page):
        self.position = position
        self.height = height
        self.total_items = total_items
        self.items_per_page = items_per_page
        self.rect = pygame.Rect(position[0], position[1], 20, height)
        self.handle_rect = pygame.Rect(position[0], position[1], 20, int(height * items_per_page // total_items))
        self.dragging = False
        self.offset_y = 0

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        pygame.draw.rect(screen, (100, 100, 100), self.handle_rect)

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True
                self.offset_y = event.pos[1] - self.handle_rect.y
        elif event.type == MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == MOUSEMOTION:
            if self.dragging:
                new_y = event.pos[1] - self.offset_y
                new_y = max(self.rect.y, min(new_y, self.rect.y + self.rect.height - self.handle_rect.height))
                self.handle_rect.y = new_y

    def get_offset(self):
        return int((self.handle_rect.y - self.rect.y) * self.total_items // self.height)

def display_message(message, y_position, font_size, colour = BLACK):
    font = pygame.font.Font(None, font_size)
    words = message.split()
    
    if len(message) > 60:
        text_lines = []
        line = ""
        
        for word in words:
            if font.size(line + word)[0] < SCREEN_WIDTH * 0.9: # padding
                line += word + " "
            else:
                text_lines.append(line)
                line = word + " "
        
        if line:
            text_lines.append(line)

        for line in text_lines:
            text = font.render(line, True, colour)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2 , y_position))
            screen.blit(text, text_rect)
            y_position += text.get_height()
    else:
        text = font.render(message, True, colour)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_position))
        screen.blit(text, text_rect)
        
        y_position += text.get_height()

    return y_position

