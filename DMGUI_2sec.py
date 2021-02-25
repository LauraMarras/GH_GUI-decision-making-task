import random
import tkinter as tk
from pylsl import StreamInfo, StreamOutlet
from PIL import ImageTk, Image
import pygame

# Create three random sets of 20 stimuli
def create_set():
    stimuli_set = range(1, 61)
    set1 = random.sample(stimuli_set, 30)
    set2 = [n for n in random.sample(stimuli_set, 60) if n not in set1]
    # set3 = random.sample(stimuli_set, 30)
    return set1, set2

set1, set2 = create_set()


# Create runs and randomize stimuli order
def create_runs(set_n):
    runs = []
    one_long_run = []

    def chunks(set_n):
        for i in range(0, len(set_n), 5):
            yield set_n[i:i + 5]

    for run in list(chunks(set_n)):
        run = (run*4)
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
def fb_color_association():
    colors = ['yellow', 'blue']
    feedbacks = ['Correct', 'Incorrect']
    fb_color = {}
    for f in feedbacks:
        c = random.choice(colors)
        fb_color[f] = c
        colors.remove(c)
    return fb_color

pygame.mixer.init()

### GUI
class DecisionMakingGui:
    numTrials = 120
    durationStimuli = 1
    durationCross = 0.5
    durationCue = 1
    durationFb = 1
    durationMessage = 1
    accuracy = {}
    count = 0
    stim_path = ''
    coin_sound = (r'Sound Stimuli/coins.mp3')
    buzz_sound = (r'Sound Stimuli/buzz.mp3')
    instructions = '''
    Task Instructions:
    During this task, a total of 30 stimuli will be presented. There will be 5 runs of 6 stimuli each,
        where each stimulus is repeated 4 times in randomized order.
    Half of the stimuli will be “winning” stimuli, the other half will be “losing” stimuli.
    Your goal is to choose, each time a stimulus is presented, whether it belongs to the winning or losing category.
    Note that each stimulus is randomly assigned to one of the categories, so you will have to guess them at first,
        and learn trial by trial, there is no hidden logic behind the associations.

    1. At the beginning of each trial, you will see a cross in the middle of the screen, please try to maintain
        central fixation throughout the trial.
    2. Then, a stimulus will be presented, you should fixate the stimulus and withhold any response until the
        stimulus disappears.
    3. At stimulus offset, you will be asked to press either the W or L key on the keyboard, indicating whether the
        stimulus belongs to the Winning or Losing category. You will have 1 second to press the key, after which
        the time will expire and the trial will be lost, so try to choose as soon as possible.
    4. After you press the key (if you did it on time), you will get a feedback indicating whether you did the
        correct choice or not.
    5. Right after a new trial will begin.
    '''

    def __init__(self, root, my_set):
        self.root = root
        self.set = create_runs(my_set)
        self.categories = assign_categories(my_set)
        self.fb_color = fb_color_association()
        self.presented_stim = {}
        for s in self.set:
            self.presented_stim[s] = 0

        #Layout
        self.width = self.root.winfo_screenwidth() * 3 / 3
        self.height = self.root.winfo_screenheight() * 3 / 3
        self.root.geometry('%dx%d+0+0' % (self.width, self.height))
        self.root.title("Decision Making Task")
        self.root.configure(bg='black')

        #Initialize LSL
        # I am not sure about this part
        info = StreamInfo('DMmarkerStream', 'Markers', 1, 0, 'string')
        # next make an outlet
        self.outlet = StreamOutlet(info)

        #Configuration Label
        self.label = tk.Label(font=('Helvetica bold', 18), bg='black', fg='white')
        self.lblVar = tk.StringVar()
        self.label.configure(textvariable=self.lblVar)
        self.lblVar.set(self.instructions + '\n Press <spacebar> to start')
        self.label.pack(expand=1)

        #Press spacebar to start
        self.root.bind('<space>', self.run)

        #Press escape to close
        self.root.bind("<Escape>", self.close)

    #Signals start of run
    def run(self, event):
        self.root.unbind('<space>')
        self.outlet.push_sample(['RunStarted'])
        self.root.after(0, self.trial)

    #Start of new trial
    def trial(self):
        self.label.pack(expand=1)
        self.root.update_idletasks()
        if self.numTrials == 0 or len(self.set) == 0:
            self.root.after(0, self.end)
        else:
            self.numTrials = self.numTrials-1
            trialn = 120-self.numTrials
            self.outlet.push_sample([f'start Trial n.{trialn}'])
            self.lblVar.set('+')
            self.label.configure(font=('Helvetica bold', 30), bg='black', fg='white')
            self.root.configure(bg='black')

            self.root.after(int(self.durationCross * 1000), self.stim)
            self.root.update_idletasks()

    #Stimulus presentation
    def stim(self):
        # set which stimulus to present: each image has one number from 1 to 60, number is taken from randomized set
        self.root.unbind('w')
        self.root.unbind('l')
        self.outlet.push_sample(['end Cross']))
        self.count += 1 # to signal trial number for later
        self.stimulus = self.set.pop(0)
        self.presented_stim[self.stimulus] += 1
        self.my_string = r'NOUN stimuli/{stim}{ext}'
        self.stim_path = self.my_string.format(stim=str(self.stimulus), ext='.jpg') #files are stored in folder with names from 1 to 60
        self.label.pack(expand=1)
        image = Image.open(self.stim_path)
        image = image.resize((500, 500), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(image)
        self.label.configure(image=test, bg='black', fg='white')
        self.root.configure(bg='black')
        self.label.image = test
        self.root.update_idletasks()

        self.outlet.push_sample(['start Stim n.: ' + str(self.stimulus)])
        self.outlet.push_sample(['Stim rep n.: ' + str(self.presented_stim[self.stimulus])
                                 
        self.root.after(int(self.durationStimuli * 1000), self.cue)

    #Cue that indicates to make decision
    def cue(self):
        self.outlet.push_sample(['end Stim'])                                 
        self.key_pressed_during_cue = False
        self.label.pack(expand=1)
        self.lblVar.set('PRESS W or L')
        self.label.configure(image='', bg='black', fg='white')
        self.root.configure(bg='black')
        self.root.update_idletasks()
        self.outlet.push_sample(['start Cue'])


    #Depending on which key is pressed, different functions are called
        self.root.bind('w', self.wpress)
        self.root.bind('l', self.lpress)

    #If no key is pressed, after 1 second the window expires and a message to be quicker is shown
        self.root.after(int(self.durationCue * 2000), self.check_choice)


    #If W is pressed --> it is evaluated whether the decision was correct or not and stored in 'accuracy'
    def wpress(self, event):
        self.root.unbind('w')
        self.root.unbind('l')
        self.key_pressed_during_cue = True
        self.root.update_idletasks()
        self.outlet.push_sample(['w Press'])
        self.root.after(0, self.cross)
        press = 'w'
        correct = self.categories[self.stimulus]

        if correct == press:
            self.letter = 'W'
            self.color = self.fb_color['Correct']
            self.accuracy[self.count] = 'Correct'
            self.sound = self.coin_sound

            self.outlet.push_sample(['CorrectChoice - W'])
            self.root.update_idletasks()
        else:
            self.letter = 'L'
            self.color = self.fb_color['Incorrect']
            self.accuracy[self.count] = 'Incorrect'
            self.sound = self.buzz_sound

            self.outlet.push_sample(['IncorrectChoice - W'])
            self.root.update_idletasks()

    # If L is pressed --> it is evaluated whether the decision was correct or not and stored in 'accuracy' and settings for feedback are defined
    def lpress(self, event):
        self.root.unbind('l')
        self.root.unbind('w')
        self.key_pressed_during_cue = True
        self.root.update_idletasks()
        self.outlet.push_sample(['lpress'])
        self.root.after(0, self.cross)
        press = 'l'
        correct = self.categories[self.stimulus]

        if correct == press:
            self.letter = 'L'
            self.color = self.fb_color['Correct']
            self.accuracy[self.count] = 'Correct'
            self.sound = self.coin_sound

            self.outlet.push_sample(['CorrectChoice - L'])
            self.root.update_idletasks()
        else:
            self.letter = 'W'
            self.color = self.fb_color['Incorrect']
            self.accuracy[self.count] = 'Incorrect'
            self.sound = self.buzz_sound

            self.outlet.push_sample(['IncorrectChoice - L'])
            self.root.update_idletasks()

    # Checks if button has been pressed, if not sends message
    def check_choice(self):
        if not self.key_pressed_during_cue:
            self.root.unbind('w')
            self.root.unbind('l')
            self.root.update_idletasks()
            self.outlet.push_sample(['Time expired - no choice'])
            self.root.after(0, self.message)

    def message(self):
        self.outlet.push_sample(['End cue-start warning'])
        self.label.pack(expand=1)
        self.lblVar.set('Time expired, please respond quicker')
        self.label.configure(bg='black', fg='red')
        self.root.configure(bg='black')
        self.root.update_idletasks()
        self.accuracy[self.count] = 'No answer'


        self.root.after(int(self.durationMessage * 1000), self.trial)
        self.root.after(int(self.durationMessage * 1000), self.outlet.push_sample(['End warning']))


    #Delay period with fixation cross of 500 ms
    def cross(self):
        self.outlet.push_sample(['StartCross'])
        self.label.pack(expand=1)
        self.lblVar.set('+')
        self.label.configure(bg='black', fg='white')
        self.root.configure(bg='black')
        self.root.update_idletasks()
        self.root.after(int(self.durationCross * 1000), self.outlet.push_sample(['endCross']))
        self.root.after(int(self.durationCross * 1000), self.fb)

    #Feedback presentation depending on accuracy on trial
    def fb(self):
        self.label.pack(expand=1)
        self.outlet.push_sample(['startFb'])
        self.lblVar.set(self.letter)
        self.label.configure(bg = self.color, fg = 'black', command=self.play_sound(self.sound))
        self.root.configure(bg= self.color)
        self.root.update_idletasks()


        self.root.after(int(self.durationFb * 1000), self.stop_sound)
        self.root.after(int(self.durationFb * 1000), self.outlet.push_sample(['endFb']))
        self.root.after(int(self.durationFb * 1000), self.trial)

    # plays sound during FB
    def play_sound(self, sound):
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play(loops=0)

    # stops sound when FB ends
    def stop_sound(self):
        pygame.mixer.music.stop()


    def end(self):
        self.outlet.push_sample(['experimentEnded'])
        self.lblVar.set('End of experiment')
        self.label.configure(bg='black', fg='white')
        self.root.configure(bg='black')
        self.root.update_idletasks()

    def close(self, event):
        self.root.destroy()

root = tk.Tk()
my_gui = DecisionMakingGui(root, set1)
root.mainloop()

# DecisionMakingGui.accuracy stores accuracy for each trial
