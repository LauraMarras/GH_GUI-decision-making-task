import random

# Create 2 random sets of 20 stimuli
def create_set():
    stimuli_set = range(1, 61)
    set1 = random.sample(stimuli_set, 15)
    #set2 = [n for n in random.sample(stimuli_set, 60) if n not in set1]

    return set1

# Create runs and randomize stimuli order
def create_runs(set_n):
    runs = []
    one_long_run = []

    def chunks(set_n):
        for i in range(0, len(set_n), 5):
            yield set_n[i:i + 5]

    for run in list(chunks(set_n)):
        run = (run * 4)
        random.shuffle(run)
        runs.append(run)

    for run in runs:
        for trial in run:
            one_long_run.append(trial)
    return one_long_run


# Randomly assign half of the stimuli to the winning category and half to the losing category for each set
def assign_categories(set_n):
    win = random.sample(set_n, 10)
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

