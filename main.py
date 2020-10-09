import random
import pygame
import sys
import csv
import os
import itertools
from math import log, exp
from datetime import datetime
# Custom modules
import config as c


# Controls general flow of the program
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, S_CHANGE_RATE, WRITE_CSV, FILENAME

    # Asks for inputs to create unique filename
    name = str(input("Enter a participant's name: ") or c.DEFAULT_NAME)
    session = str(input("Enter # of a session: ") or c.DEFAULT_SESSION)
    S_CHANGE_RATE = get_float("Enter rate as float (default is 0.33, 1/0.33 seconds per SD): ", c.DEFAULT_RATE)
    WRITE_CSV = get_bool("Write to csv? [True/False] (default is True): ", c.DEFAULT_WRITE)
    date = datetime.strftime(datetime.now(), "%Y_%b_%d_%H%M")
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    FILENAME = f"{_thisDir}{os.sep}data{os.path.sep}{name}_{session}_{date}"

    # Initialize GUI
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode(c.SCREEN_SIZE)
    SURFWIDTH, SURFHEIGHT = pygame.display.get_surface().get_size()
    BASICFONT = pygame.font.SysFont(c.FONTNAME, c.FONTSIZE)
    pygame.display.set_caption(c.CAPTION)

    # Main routine
    while True:
        experiment()


# Controls flow of the experiment
def experiment():

    phase = {  # Dictionary to store current phase
        'name': next(c.PHASES),
        'id': 1,
    }
    rf_available = True  # Tracks availability of reinforcement
    responses = 0  # Tracks number of responses
    rate = S_CHANGE_RATE  # Stores copy of global S_CHANGE_RATE for consequent manipulations

    pygame.time.set_timer(c.CHANGE_STIMULI, int(1000 / rate))
    while True:
        DISPLAYSURF.fill(c.BACKGROUND)
        buttons = c.BUTTONS
        # Updates states
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate(FILENAME, c.DATA, WRITE_CSV)
            if event.type == c.CHANGE_STIMULI:
                if rf_available:
                    rate = rate_change_handler('down', rate)
                #     print('No response, rate is reduced!')
                # print(rate)
                random.shuffle(c.V_LABELS)
                random.shuffle(c.T_LABELS['colors'])
                random.shuffle(c.T_LABELS['relations'])
            phase = phase_handler(event, **phase)
            rf_available = reinforcement_refresher(event, rf_available)
            for k in c.STIMULI['visual']:
                c.STIMULI['visual'][k] = visual_stimuli_handler(event, k, **c.STIMULI['visual'][k])
            for m in c.STIMULI['textual']:
                c.STIMULI['textual'][m] = text_stimuli_handler(event, m, **c.STIMULI['textual'][m])
            for i in buttons:
                buttons[i] = button_state_handler(event, **buttons[i])
                responses, c.SCORE, rf_available, rate = responses_handler(*[buttons[i][key] for key in ['state', 'reinforced_if']],
                                                                     responses, c.SCORE, rf_available, rate,
                                                                     **c.STIMULI)
                if buttons[i]['state'] == 'pressed':
                    # print(c.SCORE)
                    c.DATA.append([pygame.time.get_ticks()/1000, responses, c.SCORE, phase['name'], phase['id'], rate])
        # Draws states
        for k in c.STIMULI['visual']:
            image_object(phase['name'], **c.STIMULI['visual'][k])
        for m in c.STIMULI['textual']:
            text_object(**c.STIMULI['textual'][m])
        for i in buttons:
            button_object(*[buttons[i][key] for key in ['bounds', 'state', 'color_dict']])
        score_object(c.SCORE, c.STIMULI['score']['pos'])
        # Updates screen
        pygame.display.update()
        FPSCLOCK.tick(c.FPS)


# Receives current responses count and button state
# Outputs new responses count
def responses_handler(button_state, reinforced_if, responses, count, available, rate, **current_sd_state):
    responses, score, available = responses, count, available
    if button_state == 'pressed':
        responses += 1
        score, available, rate = reinforcement_handler(reinforced_if, score, available, rate, **current_sd_state)
    return responses, score, available, rate


# Receives current reinforcement state and updates availability
def reinforcement_refresher(ivent, available):
    if ivent.type == c.CHANGE_STIMULI:
        available = True
    return available


# Checks button state and updates score
# Only one correct response per stimuli is reinforced
def reinforcement_handler(reinforced_if, count, available, rate, **current_sd_state):
    complex_sd = complex_sd_handler(reinforced_if, **current_sd_state)
    if complex_sd and available:
        count += 1
        rate = rate_change_handler('up', rate)
    else:
        rate = rate_change_handler('down', rate)
    pygame.time.set_timer(c.CHANGE_STIMULI, int(1000 / rate))
    available = False  # Consequence becomes unavailable until nearest stimuli change
    return count, available, rate


# Checks whether criteria for reinforcement are satisfied
# Accepts parameter for check and parameters dictionary
def complex_sd_handler(reinforced_if, **current_sd_state):
    v_stimuli_list = [current_sd_state['visual'][k]['label'] for k in current_sd_state['visual']]
    # print(v_stimuli_list)
    t_stimuli_list = [current_sd_state['textual'][k]['label'] for k in current_sd_state['textual']]
    # print(t_stimuli_list)
    # print(list(itertools.takewhile(lambda x: x != t_stimuli_list[0], v_stimuli_list)))
    check = t_stimuli_list[2] not in list(itertools.takewhile(lambda x: x != t_stimuli_list[0], v_stimuli_list))
    if t_stimuli_list[1]=='right':
        check = not check
    # print(check)
    # print(reinforced_if)
    # print(reinforced_if==check)
    return reinforced_if==check


# Receives current state of rate
# Scroll-up: increases rate, scroll-down: decreases rate
def rate_change_handler(ivent, rate):
    if ivent=='up':
         rate = exp(log(rate) + 0.01)
    if ivent=='down':
        rate = exp(log(rate) - 0.01)
    return rate


# Inputs: event, bounds of the button, state of the button
# Outputs: same bounds, but new state if necessary
def button_state_handler(ivent, bounds, state, reinforced_if, color_dict):
    if state == 'pressed' and ivent.type != pygame.MOUSEBUTTONDOWN:
        state = 'hover'
    if ivent.type == pygame.MOUSEMOTION:
        if bounds.collidepoint(ivent.pos):
            state = 'hover'
        else:
            state = 'normal'
    elif ivent.type == pygame.MOUSEBUTTONDOWN:
        if ivent.button == 1:
            if bounds.collidepoint(ivent.pos):
                state = 'pressed'
    new_state = {
        'bounds': bounds,
        'state': state,
        'reinforced_if': reinforced_if,
        'color_dict': color_dict
    }
    return new_state


# # Generates new stimuli configuration every CHANGE_STIMULI
# # Produced stimuli depend on the current phase
# def stimuli_handler(ivent, phase, text, color, pos):
#     if ivent.type == c.CHANGE_STIMULI:
#         text = random.choice(c.WORDS[phase])
#         color = random.choice(c.COLORS)
#     new_state = {
#         'text': text,
#         'color': color,
#         'pos': pos
#     }
#     return new_state


# Generates new stimuli configuration every CHANGE_STIMULI
# Produced stimuli depend on the current phase
def visual_stimuli_handler(ivent, k, label, pos):
    if ivent.type == c.CHANGE_STIMULI:
        label = c.V_LABELS[int(k)]
    new_state = {
        'label': label,
        'pos': pos
    }
    return new_state


# Generates new stimuli configuration every CHANGE_STIMULI
# Produced stimuli depend on the current phase
def text_stimuli_handler(ivent, k, label, pos):
    if ivent.type == c.CHANGE_STIMULI:
        if k == '0' or k == '2':
            label = c.T_LABELS['colors'][int(k)]
        if k == '1':
            label = c.T_LABELS['relations'][int(k)]
    new_state = {
        'label': label,
        'pos': pos
    }
    return new_state


# Receives current phase name and id
# If Q is pressed - returns next name and id from infinite iterator PHASES (defined at the beginning)
def phase_handler(ivent, name, id):
    if ivent.type == pygame.KEYDOWN and ivent.key == pygame.K_q:
        name = next(c.PHASES)
        id += 1
    new_state = {
        'name': name,
        'id': id
    }
    return new_state


# Receives a dict of button parameters and modifies the global surface
# This side effect is intended
def button_object(bounds, state, color_dict):
    color = color_dict.get(state)
    pygame.draw.rect(DISPLAYSURF, color, bounds)


def score_object(score, pos):
    text = f"Score: {score}"
    color = c.COLORDICT['black']
    font = BASICFONT
    text_surface, bounds = get_surface(font, text, color)
    DISPLAYSURF.blit(text_surface, pos)


# Receives a dict of stimulus paramaters and modifies the global surface
# This side effect is intended
def text_object(label, pos, align=True):
    text = c.WORDS[label]
    color = c.COLORDICT['black']
    font = BASICFONT
    text_surface, bounds = get_surface(font, text, color)
    if align:
        pos = centralize(pos, bounds.width)
    DISPLAYSURF.blit(text_surface, pos)


def image_object(phase, label, pos):
    image_base = c.IMAGES[phase].get(label)
    image = pygame.transform.rotozoom(image_base, 0, 0.5)
    image_rect = image.get_rect(center=pos)
    DISPLAYSURF.blit(image, image_rect)


# Align toward center horizontally
def centralize(pos, width):
    return pos[0] - width // 2, pos[1]


# Converts raw data to the surface
def get_surface(font, text, color):
    text_surface = font.render(text, False, color)
    return text_surface, text_surface.get_rect()


# Finishes program
def terminate(filename, data, write=False):
    if write:
        write_to_csv(filename, data)
    pygame.quit()
    sys.exit()


# Writes input to a csv file
def write_to_csv(filename, data):
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(_thisDir + os.sep + u'data'):
        print(u"Data folder created")
        os.makedirs(_thisDir + os.sep + u'data')
    output_writer = csv.writer(open(filename + '.csv', 'w'), lineterminator='\n')
    for i in range(0, len(data)):
        output_writer.writerow(data[i])


# Functions to ensure correct start of the script
# Converts a string to a boolean, repeats prompt if input is not a boolean
def get_bool(prompt, default):
    while True:
        try:
            return {"true": True, "false": False}[input(prompt).lower() or default]
        except KeyError:
            print("That is not a boolean! Enter True or False")


# Repeats prompt if input is not a float
def get_float(prompt, default):
    while True:
        try:
            return float(input(prompt) or default)
        except ValueError:
            print('That is not a float! Example: 3.0')


# Starts main()
if __name__ == '__main__':
    main()