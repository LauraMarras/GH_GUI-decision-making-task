import random
import tkinter as tk
from pylsl import StreamInfo, StreamOutlet
from PIL import ImageTk, Image


# Create three random sets of 20 stimuli
def create_set():
    set1 = random.sample(range(1, 61), 30)
    set2 = random.sample((set(range(1, 61)) - set(set1)), 30)
    #set3 = random.sample((set(range(1, 61)) - set(set2)), 20)

    return set1, set2 #,set3

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

    def __init__(self, root, my_set):
        self.root = root
        self.set = create_runs(my_set)
        self.categories = assign_categories(my_set)
        self.fb_color = fb_color_association()

        #Layout
        self.width = self.root.winfo_screenwidth() * 3 / 3
        self.height =self.root.winfo_screenheight() * 3 / 3
        self.root.geometry('%dx%d+0+0' % (self.width, self.height))
        self.root.title("Decision Making Task")
        self.root.configure(bg='black')

        #Initialize LSL
        # I am not sure about this part
        info = StreamInfo('DMmarkerStream', 'Markers', 1, 0, 'string')
        # next make an outlet
        self.outlet = StreamOutlet(info)

        #Configuration Label
        self.label = tk.Label(font=('Helvetica bold', 30), bg='black', fg='white')
        self.lblVar = tk.StringVar()
        self.label.configure(textvariable=self.lblVar)
        self.lblVar.set('Press <spacebar> to start')
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
        self.outlet.push_sample(['NewTrialStarted'])
        self.label.pack(expand=1)
        self.root.update_idletasks()
        if self.numTrials == 0 or len(self.set) == 0:
            self.root.after(0, self.end)
        else:
            self.numTrials = self.numTrials-1
            self.lblVar.set('+')
            self.label.configure(bg='black', fg='white')
            self.root.configure(bg='black')

            self.root.after(int(self.durationCross * 1000), self.outlet.push_sample(['endCross']))
            self.root.after(int(self.durationCross * 1000), self.stim)
            self.root.update_idletasks()

    #Stimulus presentation
    def stim(self):
        #set which stimulus to present: each image has one number from 1 to 60, number is taken from randomized set
        self.count += 1 #to signal trial number for later
        self.stimulus = self.set.pop(0)
        self.my_string = r'C:\Users\laura\OneDrive\Documenti\Internship\Python\NOUN stimuli\{stim}{ext}'
        self.stim_path = self.my_string.format(stim=str(self.stimulus), ext='.jpg') #files are stored in folder with names from 1 to 60
        self.label.pack(expand=1)
        image = Image.open(self.stim_path)
        image = image.resize((500, 500), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(image)
        self.label.configure(image=test, bg='black', fg='white')
        self.root.configure(bg='black')
        self.label.image = test
        self.root.update_idletasks()

        self.root.after(int(self.durationStimuli * 1000), self.outlet.push_sample(['start;' + str(self.stimulus)]))
        self.root.after(int(self.durationStimuli * 1000), self.cue)

    #Cue that indicates to make decision
    def cue(self):
        self.label.pack(expand=1)
        self.outlet.push_sample(['startCue'])
        self.lblVar.set('PRESS W or L')
        self.label.configure(image='', bg='black', fg='white')
        self.root.configure(bg='black')
        self.root.update_idletasks()
        self.root.after(int(self.durationCue * 1000), self.outlet.push_sample(['endCue']))

    #Depending on which key is pressed, different functions are called
        self.root.bind('w', self.wpress)
        self.root.bind('l', self.lpress)

    # #If no key is pressed, after 1 second the window expires and a message to be quicker is shown
    #     self.root.after(int(self.durationCue * 1000), self.check_choice())

    #If W is pressed --> it is evaluated whether the decision was correct or not and stored in 'accuracy'
    def wpress(self, event):
        self.root.unbind('w')
        self.outlet.push_sample(['wpress'])
        self.root.after(0, self.cross)
        press = 'w'
        correct = self.categories[self.stimulus]

        if correct == press:
            self.letter = 'W'
            self.color = self.fb_color['Correct']
            self.accuracy[self.count] = 'Correct'

            self.outlet.push_sample(['CorrectChoice - W'])
            self.root.update_idletasks()
        else:
            self.letter = 'L'
            self.color = self.fb_color['Incorrect']
            self.accuracy[self.count] = 'Incorrect'

            self.outlet.push_sample(['IncorrectChoice - W'])
            self.root.update_idletasks()

    # If L is pressed --> it is evaluated whether the decision was correct or not and stored in 'accuracy' and settings for feedback are defined
    def lpress(self, event):
        self.root.unbind('l')
        self.outlet.push_sample(['lpress'])
        self.root.after(0, self.cross)
        press = 'l'
        correct = self.categories[self.stimulus]

        if correct == press:
            self.letter = 'L'
            self.color = self.fb_color['Correct']
            self.accuracy[self.count] = 'Correct'

            self.outlet.push_sample(['CorrectChoice - L'])
            self.root.update_idletasks()
        else:
            self.letter = 'W'
            self.color = self.fb_color['Incorrect']
            self.accuracy[self.count] = 'Incorrect'

            self.outlet.push_sample(['IncorrectChoice - L'])
            self.root.update_idletasks()

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
        self.label.configure(bg = self.color, fg = 'black')
        self.root.configure(bg= self.color)
        self.root.update_idletasks()

        self.root.after(int(self.durationFb * 1000), self.outlet.push_sample(['endFb']))
        self.root.after(int(self.durationFb * 1000), self.trial)

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

