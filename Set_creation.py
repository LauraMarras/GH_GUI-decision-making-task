import random
import json

# Create 2 random sets of 20 stimuli
def create_set():
    stimuli_set = range(1, 61)
    set1 = random.sample(stimuli_set, 30)
    
    set_test = [n for n in random.sample(stimuli_set, 60) if n not in set1] #30 stimuli
    
    set_ins = set1[0:3] #3 stimuli
    set_train = set1[3:30] #27 stimuli

    return set_test, set_ins, set_train

# Create runs and randomize stimuli order
def create_runs(set_n):
    runs = []
    one_long_run = []

    def chunks(set_n):
        for i in range(0, len(set_n), 3):
            yield set_n[i:i + 3]

    for run in list(chunks(set_n)):
        run = (run * 3)
        random.shuffle(run)
        runs.append(run)

    for run in runs:
        for trial in run:
            one_long_run.append(trial)
    return one_long_run

# Randomly assign half of the stimuli to the winning category and half to the losing category for each set
def assign_categories(set_n):
    if len(set_n)%2 == 0:
        tot_numb = int((len(set_n))/2)
    else:
        tot_numb = int(((len(set_n))-1)/2)

    win = random.sample(set_n, tot_numb)
    lose = [n for n in set_n if n not in win]
    categories = {}
    for trial in set_n:
        if trial in win:
            categories[trial] = 'w'
        elif trial in lose:
            categories[trial] = 'l'
    return categories

# Randomize colour-feedback association
def random_fb_color_association():
    colors = ['yellow', 'blue']
    feedbacks = ['Correct', 'Incorrect']
    random_fb_color = {}
    for f in feedbacks:
        c = random.choice(colors)
        random_fb_color[f] = c
        colors.remove(c)
    return random_fb_color

# Create colour-feedback association
def fb_color_association():
    fb_color = {'Correct': 'blue', 'Incorrect': 'yellow'}
    return fb_color


def create_pp_sets():
    set_test, set_ins, set_train = create_set()
    all_sets = [set_test, set_ins, set_train]
    keys = ['test', 'ins', 'train']
    all_data = {}
    for n in range(0,len(keys)):
        all_data[keys[n]] = all_sets[n]
    return all_data

def store_set(pp_n):    
    file_name = 'Info_pp{}.txt'.format(str(pp_n))
    data = create_pp_sets()
    with open(file_name, 'w+') as file:
       file.write(json.dumps(data)) 

def read_set(pp_n):
    file_name = 'Info_pp{}.txt'.format(str(pp_n))
    with open(file_name, 'r') as file:
       my_string = file.read()
       data = json.loads(my_string)

    return data
