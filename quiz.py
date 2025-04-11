#!/usr/bin/env python3
import pygame
import sys
import colorsys
import json
import random
import time
import math
import re
import subprocess
from glob import glob

from pygame.locals import *

from modules.persistence import *
from modules.elements import *
from modules.gameModes import *
from modules.searchQuiz import search_str_in_file
from modules.pygameTextInput.pygame_textinput import TextInputVisualizer


def preferences(BACKGROUND_COLOUR, BUTTON_COLOUR, music):
    while True:
        volume = pygame.mixer.music.get_volume()
        screen.fill(BACKGROUND_COLOUR)
        display_message("Preferences", 50, 75)
        display_message(f"Volume: {str(round(volume*100))}%", SCREEN_HEIGHT // 2 - 75, 50)
        button_decrease = Button("Decrease volume", (SCREEN_WIDTH // 2 + 200 , SCREEN_HEIGHT // 2 - 100), 250, 60)
        button_increase = Button("Increase volume", (SCREEN_WIDTH // 2 - 400 , SCREEN_HEIGHT // 2 - 100), 250, 60)
        button_colour = Button("Change Colour", (SCREEN_WIDTH // 2 - 400, SCREEN_HEIGHT // 2 + 50), 250, 60)
        button_music = Button("Change Music", (SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 + 50), 250, 60)
        button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2+200), 250, 60)                    
        button_increase.draw(screen, BUTTON_COLOUR)
        button_decrease.draw(screen, BUTTON_COLOUR)
        button_music.draw(screen, BUTTON_COLOUR)
        button_colour.draw(screen, BUTTON_COLOUR)
        button_go_back.draw(screen, BUTTON_COLOUR)                    
        pygame.display.update()
        for event in pygame.event.get(): 
            if event.type == QUIT:
                print(asciiartend)
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_increase.is_clicked(pos):
                    if volume <= 1:    
                        volume += 0.05
                    else:
                        pass  
                    pygame.mixer.music.set_volume(volume)
                elif button_decrease.is_clicked(pos):
                    if volume >= 0:
                        volume -= 0.05
                    else:
                        if volume < 0:
                            pass  
                    pygame.mixer.music.set_volume(volume)
                elif button_music.is_clicked(pos):
                    music_list = ['music/music1.ogg', 'music/music2.ogg', 'music/music3.ogg', 'music/music4.ogg', 'music/music5.ogg', 'music/music6.ogg', 'music/music7.ogg']
                    pygame.mixer.music.stop
                    pygame.mixer.music.unload
                    music = (random.choice(music_list))
                    pygame.mixer.music.load(music)
                    pygame.mixer.music.play(-1)
                elif button_colour.is_clicked(pos):
                    col_bg = random.uniform(0,1)
                    BACKGROUND_COLOUR = tuple(map(lambda x: 255.0*x, colorsys.hsv_to_rgb(col_bg,1,0.9))) 
                    BUTTON_COLOUR = tuple(map(lambda x: 255.0*x, colorsys.hsv_to_rgb(col_bg,1,1))) 
                elif button_go_back.is_clicked(pos):
                    return BACKGROUND_COLOUR, BUTTON_COLOUR

def choose(BACKGROUND_COLOUR, BUTTON_COLOUR):
    
    textinput = TextInputVisualizer()
    pygame.key.set_repeat(200, 25)

    searchTerm = ""
    user_answer = None
    while True:
        screen.fill(BACKGROUND_COLOUR)
        display_message("Enter Quiz Keyword:", 30, 50, BLACK)
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                quit()
        textinput.update(events)

        screen.blit(textinput.surface, (500, 100))

        if [ev for ev in events if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN]:
            searchTerm = textinput.value
            break

        pygame.display.update()
        pygame.time.wait(30)

    quizfiles = glob('./Quizzes/**/*.json', recursive=True)

    quizfileSearchResults = []
    for file in quizfiles:
        if search_str_in_file(file, searchTerm):
            quizfileSearchResults.append(file)

    if not quizfileSearchResults:
        display_message("No Quiz Results found!", SCREEN_HEIGHT // 2, 75, (255,0,0))
        pygame.display.update()
        pygame.time.wait(250)
        choose(BACKGROUND_COLOUR, BUTTON_COLOUR)
        return
        

    scrollbar = Scrollbar((SCREEN_WIDTH - 40, ANSWER_OFFSET), SCREEN_HEIGHT - ANSWER_OFFSET - 50, len(quizfileSearchResults), 10)
    buttons = []
    for idx, quizfile in enumerate(quizfileSearchResults):
        try:
            with open(quizfile, "r", errors="ignore") as file:
                quiztitle = json.load(file)["title"]
            button = Button(quiztitle, (SCREEN_WIDTH // 2 - 150, ANSWER_OFFSET + idx * OPTION_HEIGHT), 300, 40)
            buttons.append(button)
        except json.decoder.JSONDecodeError as ex:
            print(f"Error in quizfile {quizfile}! {ex}")
            continue

    running = True
    while running:
        screen.fill(BACKGROUND_COLOUR)
        for button in buttons:
            button.draw(screen, BUTTON_COLOUR if user_answer is None else BACKGROUND_COLOUR)
        if len(buttons) > 12:    
           scrollbar.draw(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP or event.type == MOUSEMOTION:
                scrollbar.handle_event(event)
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for idx, button in enumerate(buttons):
                    if button.is_clicked(pos):
                        user_answer = idx

        offset = scrollbar.get_offset()
        for idx, button in enumerate(buttons):
            button.position = (SCREEN_WIDTH // 2 - 150, 100 + (idx - offset) * OPTION_HEIGHT)
            button.rect.topleft = button.position

        if user_answer is not None:
            filename = quizfileSearchResults[user_answer]

            try:
                questionList, titleofquiz  = load_quiz(filename)
            except Exception as ex:
                messagebox.showinfo(title='Error', message=f'This is not a quiz file: {ex}!')
                continue
            print("Questions:", questionList)
            
            running = True
            while running:
                screen.fill(BACKGROUND_COLOUR)
                display_message("Select Game Mode:", SCREEN_HEIGHT // 2 - 300, 75, BLACK)
                button_classic = Button("Classic", (SCREEN_WIDTH // 2 - 600, SCREEN_HEIGHT // 2 - 200), 250, 60)
                button_classicV2 = Button("Classic v2.0", (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 200), 250, 60)
                button_speed = Button("Speed Run", (SCREEN_WIDTH // 2 , SCREEN_HEIGHT // 2 - 200), 250, 60)
                button_survival = Button("Survival", (SCREEN_WIDTH // 2 + 300, SCREEN_HEIGHT // 2 - 200), 250, 60)
                button_practice = Button("Practice", (SCREEN_WIDTH // 2 - 600, SCREEN_HEIGHT // 2 - 100), 250, 60)
                button_classic.draw(screen, BUTTON_COLOUR)
                button_classicV2.draw(screen, BUTTON_COLOUR)
                button_speed.draw(screen, BUTTON_COLOUR)
                button_survival.draw(screen, BUTTON_COLOUR)
                button_practice.draw(screen, BUTTON_COLOUR)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == QUIT:
                        quit()
                    if event.type == MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        event_time = pygame.time.get_ticks()
                        # Start game mode functions
                        if button_classic.is_clicked(pos):
                            classic(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
                            return
                        elif button_classicV2.is_clicked(pos):
                            classicV2(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
                            return
                        elif button_speed.is_clicked(pos):
                            speed(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
                            return
                        elif button_survival.is_clicked(pos):
                            survival(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
                            return
                        elif button_practice.is_clicked(pos):
                            practice(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
                            return
                
def main(music, BACKGROUND_COLOUR, BUTTON_COLOUR):
    while True:
        screen.fill(BACKGROUND_COLOUR)
        button_play = Button("Play a Quiz", (SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2 - 50), 350, 70)
        button_make = Button("Make a Quiz", (SCREEN_WIDTH // 2 - 400, SCREEN_HEIGHT // 2 - 50), 350, 70)
        button_preferences = Button("Preferences", (SCREEN_WIDTH // 2 - 400, SCREEN_HEIGHT // 2 + 100), 350, 70)
        button_quit = Button("Quit", (SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2 + 100), 350, 70)
        display_message("Welcome to QuizMaster!", SCREEN_HEIGHT // 8, 75, BLACK)
        button_make.draw(screen, BUTTON_COLOUR)
        button_play.draw(screen, BUTTON_COLOUR)
        button_preferences.draw(screen, BUTTON_COLOUR)
        button_quit.draw(screen, BUTTON_COLOUR)
        pygame.display.update()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_play.is_clicked(pos):
                    choose(BACKGROUND_COLOUR, BUTTON_COLOUR)
                elif button_make.is_clicked(pos):
                    try:
                        subprocess.Popen(["python", "quizcreator"])
                    except:
                        subprocess.Popen(["python3", "quizcreator"])
                elif button_preferences.is_clicked(pos):
                    BACKGROUND_COLOUR, BUTTON_COLOUR = preferences(BACKGROUND_COLOUR, BUTTON_COLOUR, music)
                elif button_quit.is_clicked(pos):
                    quit()
                
if __name__ == '__main__':
    
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()

    print(asciiartstart)
    music_list = ['music/music1.ogg', 'music/music2.ogg', 'music/music3.ogg', 'music/music4.ogg', 'music/music5.ogg', 'music/music6.ogg', 'music/music7.ogg']
    music = (random.choice(music_list))
    col_bg = random.uniform(0,1)
    BACKGROUND_COLOUR = tuple(map(lambda x: 255.0*x, colorsys.hsv_to_rgb(col_bg,1,0.9))) 
    BUTTON_COLOUR = tuple(map(lambda x: 255.0*x, colorsys.hsv_to_rgb(col_bg,1,1))) 

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('QuizMaster')
    pygame.mixer.init()
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(-1)
    main(music, BACKGROUND_COLOUR, BUTTON_COLOUR)