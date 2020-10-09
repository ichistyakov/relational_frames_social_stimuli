import itertools
import pygame
import os
# Custom modules
import colors as c

_THISDIR = os.path.dirname(os.path.abspath(__file__))
COLORDICT = {
    'black': c.BLACK
}
# GUI parameters
BACKGROUND = c.IVORY1
FPS = 60
FONTNAME = 'Arial'
FONTSIZE = 40
CAPTION = 'Main window'
SCREEN_SIZE = (1000, 800)
SCORE = 0
# Session parameters
DEFAULT_NAME = 'A_girl_has_no_name'
DEFAULT_SESSION = 'Infinity'
DEFAULT_RATE = 0.33
DEFAULT_WRITE = True
# Experimental set-up
# Possible text stimuli
IMAGES = {
    'A':
        {
            'blank': pygame.image.load(os.path.join(_THISDIR, 'images', 'blank.png')),
            'red': pygame.image.load(os.path.join(_THISDIR, 'images', 'red_rect.png')),
            'green': pygame.image.load(os.path.join(_THISDIR, 'images', 'green_rect.png')),
            'blue': pygame.image.load(os.path.join(_THISDIR, 'images', 'blue_rect.png'))
        },
    'B':
        {
            'blank': pygame.image.load(os.path.join(_THISDIR, 'images', 'blank.png')),
            'red': pygame.image.load(os.path.join(_THISDIR, 'images', 'red_human.png')),
            'green': pygame.image.load(os.path.join(_THISDIR, 'images', 'green_human.png')),
            'blue': pygame.image.load(os.path.join(_THISDIR, 'images', 'blue_human.png'))
        }
}
WORDS = {'red': u'красный',
         'green': u'зеленый',
         'blue': u'синий',
         'left': u'левее, чем',
         'right': u'правее, чем',
         'score': f"Score: {SCORE}"}
V_LABELS = ['red', 'green', 'blue']
T_LABELS = {
    'colors': ['red', 'green', 'blue'],
    'relations': ['left', 'right']
}
# Possible colors of text stimuli
COLORS = ['black']
# Possible phases
PHASES = itertools.cycle(['A', 'B'])
# Response options
BUTTONS = {
    'first': {
        'bounds': pygame.Rect(300, 600, 150, 150),
        'state': 'normal',
        'reinforced_if': True,
        'color_dict': {
            'normal': c.GREEN1,
            'hover': c.GREEN2,
            'pressed': c.GREEN3,
        }
    },
    'second': {
        'bounds': pygame.Rect(550, 600, 150, 150),
        'state': 'normal',
        'reinforced_if': False,
        'color_dict': {
            'normal': c.RED1,
            'hover': c.RED2,
            'pressed': c.RED3,
        }
    }
}
# Stimuli presented
STIMULI = {
    'visual': {
        '0': {
            'label': 'red',
            'pos': (350, 250)
        },
        '1': {
            'label': 'green',
            'pos': (500, 250)
        },
        '2': {
            'label': 'blue',
            'pos': (650, 250)
        }
    },
    'textual': {
        '0': {
            'label': 'red',
            'pos': (300, 440)
        },
        '1': {
            'label': 'right',
            'pos': (500, 440)
        },
        '2': {
            'label': 'blue',
            'pos': (700, 440)
        }
    },
    'score': {
        'label': 'score',
        'pos': (50, 50)
    }
}
# Custom event to trigger changes in stimuli
CHANGE_STIMULI = pygame.USEREVENT + 1
# List to store collected data
DATA = [['time', 'responses', 'score', 'phase_name', 'phase_id', 'rate']]