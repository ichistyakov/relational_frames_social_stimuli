# Free operant conceptual replication of Kalkstein, D. A., et al, 2020

### Schedule of reinforcement
Regressive-interval multiple schedule of reinforcement is a compound schedule of reinforcement consisting of two or more basic schedules of reinforcement (elements) that occur in an alternating random sequence; interval between two consecutive changes is not fixed - reinforced responses shorten it; a discriminative stimulus is correlated with the presence or absence of each element of the schedule, and reinforcement is delivered for meeting the response requirements of the element in effect at any time.
### Structure of the experiment
Current script consists of concurrent fixed-interval multiple schedule of reinforcement. Basic FI MULT consist of two schedules - responses increase or decrease score. Two response options are available, green and red buttons; when presented description of relations between visual stimuli is correct - green button click is reinforced and red button clicks are under extinction, when B is present - correlations are opposite.
### Flow control
Q changes phase values over `itertools.cycle(['A', 'B'])`, where A and B correspond to aforementioned experimental conditions.</br>

## Requirements
Tested only for Python 3.6</br>
Libraries: `pygame, numpy`

## Installation
Ubuntu 16.04 or later:
```
git clone https://github.com/ichistyakov/free-operant_reaction_time.git
cd ~/free-operant_reaction_time
# Optional: create virtual environment
# Run sudo apt install python3-venv if necessary
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Starting
From venv:
```
python3 main.py
```
If everything is okay, script will prompt several inputs in terminal to create distinct filename and start PyGame GUI
