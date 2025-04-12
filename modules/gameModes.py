"""
Module for the "basic" game modes: Classic, Classic V2, Speed Run, Survival and Practice. More complex game modes will be placed in seperate files due to length.
"""

import pygame
import random
import time

from pygame.locals import *
from modules.elements import *

def countdown(titleofquiz, BACKGROUND_COLOUR):
    for i in range(3, 0, -1):
        screen.fill(BACKGROUND_COLOUR)
        display_message(titleofquiz, QUESTION_OFFSET, 70)
        display_message((f"{i}!"), QUESTION_OFFSET + 200, 150)
        pygame.display.update()
        pygame.time.delay(1000)
    screen.fill(BACKGROUND_COLOUR)
    display_message(("Go!"), QUESTION_OFFSET + 200, 150, BLACK)
    pygame.display.update()
    pygame.time.delay(1000)
    return

def show_incorrect_answers(incorrect_questions, BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK):
    running = True
    total_items = len(incorrect_questions)
    items_per_page = 10
    scrollbar = Scrollbar((SCREEN_WIDTH - 40, 100), SCREEN_HEIGHT - 150, total_items, items_per_page)
    offset = 0

    while running:
        screen.fill(BACKGROUND_COLOUR)
        y_position = 50
        button_back = Button("Back to Results", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 100), 300, 50)
        button_back.draw(screen, BUTTON_COLOUR)
        for idx in range(offset, min(offset + items_per_page, total_items)):
            question = incorrect_questions[idx]
            y_position = display_message(question.question, y_position, 30, BLACK)
            y_position = display_message(f"Correct Answer: {question.correctAnswer}", y_position, 30, BLACK)
            y_position += 20

        if total_items > items_per_page:
            scrollbar.draw(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_back.is_clicked(pos):
                    return
            if total_items > items_per_page:
                scrollbar.handle_event(event)

        offset = scrollbar.get_offset()

def standard_end_window(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, titleofquiz, totalQuestions, correctAnswers, questionIndex, incorrect_questions):
    good_praise = f"Well Done! You know a lot about {titleofquiz.lower()}!"
    medium_praise = f"A commendable effort in {titleofquiz.lower()}!"
    bad_praise = f"You are terrible at {titleofquiz.lower()}!"
    while True:
        screen.fill(BACKGROUND_COLOUR)
        y_position = display_message(f"Quiz completed! You got {correctAnswers} out of {totalQuestions} questions correct.", SCREEN_HEIGHT // 2-200,40, BLACK)
        try:
            if correctAnswers/totalQuestions > 0.4 and correctAnswers/totalQuestions <= 0.8:
                display_message(medium_praise, y_position,40, BLACK)
            if correctAnswers/totalQuestions > 0.8:
                display_message(good_praise, y_position,40, BLACK)
            if correctAnswers/totalQuestions <= 0.4:
                display_message(bad_praise, y_position,40, BLACK)
        except ZeroDivisionError:
                display_message("No questions attempted!", y_position,40, BLACK)
    
        button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50), 250, 40)
        button_replay = Button("Replay", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100), 250, 40)
        button_quit = Button("Quit", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 150), 250, 40)
        if incorrect_questions:
          button_show_incorrect = Button("Show Incorrect Answers", (SCREEN_WIDTH // 2 - 150 , SCREEN_HEIGHT // 2), 250, 40)
          button_show_incorrect.draw(screen, BUTTON_COLOUR)
        button_go_back.draw(screen, BUTTON_COLOUR)
        button_replay.draw(screen, BUTTON_COLOUR)
        button_quit.draw(screen, BUTTON_COLOUR)
        
        pygame.display.update()

        for event in pygame.event.get(): 
            if event.type == QUIT:
               quit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if incorrect_questions and questionIndex > 0:
                    if button_show_incorrect.is_clicked(pos):
                        show_incorrect_answers(incorrect_questions, BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK)
                if button_go_back.is_clicked(pos):
                    return False
                if button_replay.is_clicked(pos):
                    return True
                if button_quit.is_clicked(pos):
                    quit()

def classic(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR):
    if questionList is None:
        pass
        return
    incorrect_questions = []
    running = True
    questionIndex = 0
    correctAnswers = 0
    totalQuestions = len(questionList)
    
    countdown(titleofquiz, BACKGROUND_COLOUR)

    while running and questionIndex < totalQuestions:
        currentQuestion = questionList[questionIndex]

        user_answer = None
        time_remaining = currentQuestion.timeout
        
        answerOptions = [currentQuestion.correctAnswer] + currentQuestion.wrongAnswers
        random.shuffle(answerOptions)

        buttons = []
        for idx, answer in enumerate(answerOptions):
            button = Button(f"{idx + 1}. {answer}", (SCREEN_WIDTH // 2 - 200, ANSWER_OFFSET + idx * OPTION_HEIGHT), 400, 40)
            buttons.append(button)

        while running and time_remaining > 0 and user_answer is None:
            screen.fill(BACKGROUND_COLOUR)
            display_message(f"Question {questionIndex + 1} out of {totalQuestions} : {currentQuestion.question}", QUESTION_OFFSET, 50)

            for button in buttons:
                button.draw(screen, BUTTON_COLOUR if user_answer is None else BACKGROUND_COLOUR)
            button_end = Button("End Quiz", (SCREEN_WIDTH // 2+350 , SCREEN_HEIGHT // 2+200), 250, 40)  
            button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2+350 , SCREEN_HEIGHT // 2+250), 250, 40)
            button_leave = Button("Quit", (SCREEN_WIDTH // 2+350 , SCREEN_HEIGHT // 2+300), 250, 40)
            display_message(f"Time remaining: {time_remaining}", SCREEN_HEIGHT - QUESTION_OFFSET, 40)
            button_end.draw(screen, BUTTON_COLOUR)
            button_go_back.draw(screen, BUTTON_COLOUR)
            button_leave.draw(screen, BUTTON_COLOUR)
            pygame.display.update()
            pygame.time.wait(1000)

            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos() 
                    if button_end.is_clicked(pos):
                        running = False
                        break
                    if button_go_back.is_clicked(pos):
                       return
                    if button_leave.is_clicked(pos):
                       quit()
                    for idx, button in enumerate(buttons):
                        if button.is_clicked(pos):
                            user_answer = idx
 
                if event.type == KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9]:
                        user_answer = event.key - pygame.K_1

            time_remaining -= 1

        correct_answer_index = answerOptions.index(currentQuestion.correctAnswer)
        if user_answer is not None:
            if user_answer == correct_answer_index:
                correctAnswers += 1
            else:
                incorrect_questions.append(currentQuestion)

        questionIndex += 1

    replay = standard_end_window(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, titleofquiz, totalQuestions, correctAnswers, questionIndex, incorrect_questions)
    if replay:
        classic(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
    else:       
        return

                    
def classicV2(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR):
    if questionList is None:
        pass
        return
    
    incorrect_questions = []
    running = True
    questionIndex = 0
    correctAnswers = 0
    totalQuestions = len(questionList)
    
    total_time = sum(q.timeout-3 for q in questionList)+10
    start_time = time.time()
    
    countdown(titleofquiz, BACKGROUND_COLOUR)

    while running and questionIndex < totalQuestions:
        currentQuestion = questionList[questionIndex]

        user_answer = None

        answerOptions = [currentQuestion.correctAnswer] + currentQuestion.wrongAnswers
        random.shuffle(answerOptions)

        buttons = []
        for idx, answer in enumerate(answerOptions):
            button = Button(f"{idx + 1}. {answer}", (SCREEN_WIDTH // 2 - 200, ANSWER_OFFSET + idx * OPTION_HEIGHT), 400, 40)
            buttons.append(button)

        while running and user_answer is None:
            elapsed_time = time.time() - start_time
            time_remaining = total_time - int(elapsed_time)

            if time_remaining <= 0:
                running = False
                break

            screen.fill(BACKGROUND_COLOUR)
            display_message(f"Question {questionIndex + 1} out of {totalQuestions} : {currentQuestion.question}", QUESTION_OFFSET, 50)

            for button in buttons:
                button.draw(screen, BUTTON_COLOUR if user_answer is None else BACKGROUND_COLOUR)
            button_end = Button("End Quiz", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 200), 250, 40)
            button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 250), 250, 40)
            button_leave = Button("Quit", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 300), 250, 40)
            display_message(f"Time remaining: {time_remaining}", SCREEN_HEIGHT - QUESTION_OFFSET, 40)
            button_end.draw(screen, BUTTON_COLOUR)
            button_go_back.draw(screen, BUTTON_COLOUR)
            button_leave.draw(screen, BUTTON_COLOUR)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if button_end.is_clicked(pos):
                        running = False
                        break
                    if button_go_back.is_clicked(pos):
                        return
                    if button_leave.is_clicked(pos):
                        quit()
                    pygame.time.wait(40)
                    for idx, button in enumerate(buttons):
                        if button.is_clicked(pos):
                            user_answer = idx

                if event.type == KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                        user_answer = event.key - pygame.K_1

        correct_answer_index = answerOptions.index(currentQuestion.correctAnswer)
        if user_answer is not None:
            if user_answer == correct_answer_index:
                correctAnswers += 1
            else:
                incorrect_questions.append(currentQuestion)

        questionIndex += 1

    replay = standard_end_window(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, titleofquiz, totalQuestions, correctAnswers, questionIndex, incorrect_questions)
    if replay:
        classicV2(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
    else:       
        return


def speed(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR):
    if questionList is None:
        pass
        return
    originalQuestions = questionList[:]
    incorrect_questions = []
    running = True
    correctAnswers = 0
    totalQuestions = len(originalQuestions)
    lives = int(len(questionList) // 3 + 1)
    
    countdown(titleofquiz, BACKGROUND_COLOUR)

    while running:
        if not questionList:
            break

        currentQuestion = questionList.pop(0)
        user_answer = None

        answerOptions = [currentQuestion.correctAnswer] + currentQuestion.wrongAnswers
        random.shuffle(answerOptions)

        buttons = []
        for idx, answer in enumerate(answerOptions):
            button = Button(f"{idx + 1}. {answer}", (SCREEN_WIDTH // 2 - 200, ANSWER_OFFSET + idx * OPTION_HEIGHT), 400, 40)
            buttons.append(button)

        while running and user_answer is None:
            screen.fill(BACKGROUND_COLOUR)
            display_message(f"Question: {currentQuestion.question}", QUESTION_OFFSET, 50, BLACK)

            for button in buttons:
                button.draw(screen, BUTTON_COLOUR if user_answer is None else BACKGROUND_COLOUR)
            button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 250), 250, 40)
            button_leave = Button("Quit", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 300), 250, 40)
            elapsed_time = time.time() - start_time
            display_message(f"Time: {int(elapsed_time)}", SCREEN_HEIGHT - QUESTION_OFFSET, 40, BLACK)
            display_message(f"Lives: {lives}", SCREEN_HEIGHT - (QUESTION_OFFSET + 40), 40, BLACK)
            button_go_back.draw(screen, BUTTON_COLOUR)
            button_leave.draw(screen, BUTTON_COLOUR)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for idx, button in enumerate(buttons):
                        if button_go_back.is_clicked(pos):
                           return
                        if button_leave.is_clicked(pos):
                           quit()
                        if button.is_clicked(pos):
                            user_answer = idx

                if event.type == KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                        user_answer = event.key - pygame.K_1

        correct_answer_index = answerOptions.index(currentQuestion.correctAnswer)
        if user_answer is not None:
            if user_answer == correct_answer_index:
                correctAnswers += 1
                continue
            else:
                questionList.append(currentQuestion)
                lives -= 1
                if lives < 0:
                    questionList = originalQuestions[:]
                    correctAnswers = 0
                    lives = 3

    end_time = time.time()
    total_time = int(end_time - start_time)

    while True:
        screen.fill(BACKGROUND_COLOUR)
        y_position = display_message(f"Speed Run completed! You answered all questions correctly in {total_time} seconds.", SCREEN_HEIGHT // 2 - 200, 40, BLACK)
        button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50), 250, 40)
        button_replay = Button("Replay", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100), 250, 40)
        button_quit = Button("Quit", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 150), 250, 40)
        button_go_back.draw(screen, BUTTON_COLOUR)
        button_replay.draw(screen, BUTTON_COLOUR)
        button_quit.draw(screen, BUTTON_COLOUR)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_go_back.is_clicked(pos):
                    return
                if button_replay.is_clicked(pos):
                    speed(originalQuestions[:], titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
                    return
                if button_quit.is_clicked(pos):
                    quit()

def survival(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR):
    if questionList is None:
        pass
        return
        
    incorrect_questions = []
    running = True
    questionIndex = 0
    correctAnswers = 0
    totalQuestions = len(questionList)
    lives = int(len(questionList) // 3+1)

    countdown(titleofquiz, BACKGROUND_COLOUR)
    
    while running and questionIndex < totalQuestions and lives > 0:
        currentQuestion = questionList[questionIndex]

        user_answer = None

        answerOptions = [currentQuestion.correctAnswer] + currentQuestion.wrongAnswers
        random.shuffle(answerOptions)

        buttons = []
        for idx, answer in enumerate(answerOptions):
            button = Button(f"{idx + 1}. {answer}", (SCREEN_WIDTH // 2 - 200, ANSWER_OFFSET + idx * OPTION_HEIGHT), 400, 40)
            buttons.append(button)

        while running and user_answer is None:
            screen.fill(BACKGROUND_COLOUR)
            display_message(f"Question {questionIndex + 1} out of {totalQuestions} : {currentQuestion.question}", QUESTION_OFFSET, 50, BLACK)

            for button in buttons:
                button.draw(screen, BUTTON_COLOUR if user_answer is None else BACKGROUND_COLOUR)
            
            button_end = Button("End Quiz", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 200), 250, 40)
            button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 250), 250, 40)
            button_leave = Button("Quit", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 300), 250, 40)
            display_message(f"Lives remaining: {lives}", SCREEN_HEIGHT - QUESTION_OFFSET, 40, BLACK)
            button_end.draw(screen, BUTTON_COLOUR)
            button_go_back.draw(screen, BUTTON_COLOUR)
            button_leave.draw(screen, BUTTON_COLOUR)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if button_end.is_clicked(pos):
                        running = False
                        break
                    if button_go_back.is_clicked(pos):
                        return
                    if button_leave.is_clicked(pos):
                        quit()
                    pygame.time.wait(40)
                    for idx, button in enumerate(buttons):
                        if button.is_clicked(pos):
                            user_answer = idx

                if event.type == KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                        user_answer = event.key - pygame.K_1

        correct_answer_index = answerOptions.index(currentQuestion.correctAnswer)
        if user_answer is not None:
            if user_answer == correct_answer_index:
                correctAnswers += 1
            else:
                incorrect_questions.append(currentQuestion)
                lives -= 1

        questionIndex += 1

    replay = standard_end_window(BACKGROUND_COLOUR, BUTTON_COLOUR, BLACK, titleofquiz, totalQuestions, correctAnswers, questionIndex, incorrect_questions)
    if replay:
        survival(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
    else:       
        return

def practice(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR):
    if questionList is None:
        pass
        return
        
    running = True
    questionIndex = 0
    totalQuestions = len(questionList)
    
    if BUTTON_COLOUR[1] > 220:
        BUTTON_COLOUR = (BUTTON_COLOUR[0], 220, BUTTON_COLOUR[2]) # Improve visibility of answer reveal
    
    countdown(titleofquiz, BACKGROUND_COLOUR)
    
    while running and questionIndex < totalQuestions:
        currentQuestion = questionList[questionIndex]

        user_answer = None
        reveal_answer = False 

        answerOptions = [currentQuestion.correctAnswer] + currentQuestion.wrongAnswers
        random.shuffle(answerOptions)

        buttons = []
        for idx, answer in enumerate(answerOptions):
            button = Button(f"{idx + 1}. {answer}", (SCREEN_WIDTH // 2 - 200, ANSWER_OFFSET + idx * OPTION_HEIGHT), 400, 40)
            buttons.append(button)

        while running and user_answer is None:
            screen.fill(BACKGROUND_COLOUR)
            display_message(f"Question {questionIndex + 1} out of {totalQuestions} : {currentQuestion.question}", QUESTION_OFFSET, 50, BLACK)
            button_show = Button("Reveal Answer", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 300), 300, 50)
            button_end = Button("End Quiz", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 250), 250, 40)
            button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 300), 250, 40)
            button_leave = Button("Quit", (SCREEN_WIDTH // 2 + 350, SCREEN_HEIGHT // 2 + 350), 250, 40)
            button_show.draw(screen, BUTTON_COLOUR)
            button_end.draw(screen, BUTTON_COLOUR)
            button_go_back.draw(screen, BUTTON_COLOUR)
            button_leave.draw(screen, BUTTON_COLOUR)
            
            for idx, button in enumerate(buttons):
                if reveal_answer and answerOptions[idx] == currentQuestion.correctAnswer:
                    button.draw(screen, (0, 255, 0))
                    button_show.draw(screen, (0, 255, 0))
                else:
                    button.draw(screen, BUTTON_COLOUR if user_answer is None else BACKGROUND_COLOUR)
            
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()
                if event.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if button_show.is_clicked(pos):
                        reveal_answer = True
                    if button_end.is_clicked(pos):
                        running = False
                        break
                    if button_go_back.is_clicked(pos):
                        return
                    if button_leave.is_clicked(pos):
                        quit()
                    pygame.time.wait(40)
                    for idx, button in enumerate(buttons):
                        if button.is_clicked(pos):
                            user_answer = idx

                if event.type == KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                        user_answer = event.key - pygame.K_1

        correct_answer_index = answerOptions.index(currentQuestion.correctAnswer)
        questionIndex += 1

    while True:
        screen.fill(BACKGROUND_COLOUR)
        y_position = display_message(f"Quiz completed!", SCREEN_HEIGHT // 2 - 200, 40, BLACK)
        
        button_go_back = Button("Main Menu", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50), 250, 40)
        button_replay = Button("Replay", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100), 250, 40)
        button_quit = Button("Quit", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 150), 250, 40)
        button_go_back.draw(screen, BUTTON_COLOUR)
        button_replay.draw(screen, BUTTON_COLOUR)
        button_quit.draw(screen, BUTTON_COLOUR)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if button_go_back.is_clicked(pos):
                    return
                if button_replay.is_clicked(pos):
                    practice(questionList, titleofquiz, BACKGROUND_COLOUR, BUTTON_COLOUR)
                    return
                if button_quit.is_clicked(pos):
                    quit()
