import tkinter as tk
from pylsl import StreamInfo, StreamOutlet
from PIL import ImageTk, Image
import pygame
import Set_creation as sc


###GUI
class DMGUI_Test:

    #Set number of trials and windows durations
    durationStimuli = 1
    durationCross = 0.5
    durationCue = 2
    durationFb = 1
    durationMessage = 1

    #store stimuli path
    stim_path = ''
    coin_sound = ('./Sound Stimuli/coins.mp3')
    buzz_sound = ('./Sound Stimuli/buzz.mp3')
    
    #save instructions text
    dutch_instructions = 'Als u klaar bent, drukt u op <spatiebalk> om te beginnen'
    eng_instructions = 'When you are ready, press <spacebar> to start'
    instructions = eng_instructions

    def __init__(self, root, pp_n):
        pygame.mixer.init()
        self.numTrials = 120
        self.trialn = 0
        self.n_run = 0

        #Retrieve sets for pp
        try:
            self.all_sets = sc.read_set(pp_n)
        except FileNotFoundError:
            sc.store_set(pp_n)
            self.all_sets = sc.read_set(pp_n)

        self.root = root
        self.initial_set = self.all_sets['test']
        self.set = sc.create_runs(self.initial_set)
        self.categories = sc.assign_categories(self.initial_set)
        self.fb_color = sc.fb_color_association()
        self.accuracy = {}
        self.count = 0
        self.results = {}
        self.presented_stim = {}
        self.press = ''
        for s in self.set:
            self.presented_stim[s] = 0

        #Layout
        self.root.attributes('-fullscreen', True)
        self.width = self.root.winfo_screenwidth() * 3 / 3
        self.height = self.root.winfo_screenheight() * 3 / 3
        self.root.geometry('%dx%d+0+0' % (self.width, self.height))
        self.root.title("Decision Making Task Test")
        self.root.configure(bg='black')

        #Initialize LSL
        info = StreamInfo('DMmarkerStream', 'Markers', 1, 0, 'string')
        #next make an outlet
        self.outlet = StreamOutlet(info)

        #Configuration language button
        self.lang_button = tk.Button(text='ENG', fg='red', command=self.change_lang)

        #Configuration Label
        self.label = tk.Label(anchor='w', justify='left', font=('Helvetica bold', 15), bg='black', fg='white')
        self.lblVar = tk.StringVar()
        self.label.configure(textvariable=self.lblVar)
        self.lang_button.pack(pady=10)
        self.lblVar.set(self.instructions)
        self.label.pack(expand=1)

        #Press spacebar to start
        self.root.bind('<space>', self.run)

        #Press escape to close
        self.root.bind("<Escape>", self.close)

    #Changes language of instructions
    def change_lang(self):
        if self.instructions == self.dutch_instructions:
            self.instructions = self.eng_instructions
            self.lblVar.set(self.instructions)
            self.lang_button['text'] = "DUTCH"
        elif self.instructions == self.eng_instructions:
            self.instructions = self.dutch_instructions
            self.lblVar.set(self.instructions)
            self.lang_button['text'] = "ENGLISH"



    #Signals start of session
    def run(self, event):
        self.root.unbind('<space>')
        self.outlet.push_sample(['Start Session'])
        self.root.after(0, self.trial)
        self.lang_button.destroy()

    #Start of new trial
    def trial(self):
        self.label.pack(expand=1)
        self.root.update_idletasks()
        self.root.bind('<Left>', self.wpress2)
        self.root.bind('<Right>', self.lpress2)

        if self.numTrials == 0 or len(self.set) == 0:
            self.root.after(0, self.end)
        else:
            self.numTrials = self.numTrials - 1
            self.trialn = 120 - self.numTrials

            if (self.trialn - 1) % 9 == 0:
                self.outlet.push_sample([f'Start Trial n.{self.trialn}'])
                self.n_run += 1
                self.root.after(0, self.run_break)
            else:
                self.outlet.push_sample([f'Start Trial n.{self.trialn}'])
                self.lblVar.set('+')
                self.label.configure(font=('Helvetica bold', 30), bg='black', fg='white')
                self.root.configure(bg='black')

                self.root.after(int(self.durationCross * 1000), self.stim)
                self.root.update_idletasks()

    #Breaks
    def run_break(self):
        self.outlet.push_sample(['Start Break'])
        break_string = 'Group N. {}'.format(self.n_run)
        self.lblVar.set(break_string)
        self.label.configure(font=('Helvetica bold', 30), bg='black', fg='white')
        self.root.configure(bg='black')

        self.root.after(10000, self.stim)
        self.root.update_idletasks()

    #Stimulus presentation
    def stim(self):
        self.outlet.push_sample(['End Cross'])

        #set which stimulus to present: each image has one number from 1 to 60, number is taken from randomized set
        self.count += 1  #to signal trial number for later
        self.stimulus = self.set.pop(0)
        self.presented_stim[self.stimulus] += 1
        self.my_string = './NOUN stimuli/{stim}{ext}'
        self.stim_path = self.my_string.format(stim=str(self.stimulus), ext='.jpg')  # files are stored in folder with names from 1 to 60
        self.label.pack(expand=1)
        image = Image.open(self.stim_path)
        image = image.resize((500, 500), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(image)
        self.label.configure(image=test, bg='black', fg='white')
        self.root.configure(bg='black')
        self.label.image = test
        self.root.update_idletasks()

        self.outlet.push_sample(['Start Stim n.: ' + str(self.stimulus) + ' - Rep n.: ' + str(self.presented_stim[self.stimulus])])

        self.root.after(int(self.durationStimuli * 1000), self.cue)

    #Cue that indicates to make decision
    def cue(self):
        if self.instructions == self.dutch_instructions:
            cue = 'DRUK W of L'
        elif self.instructions == self.eng_instructions:
            cue = 'PRESS W or L'
        self.root.unbind('<Left>')
        self.root.unbind('<Right>')
        self.outlet.push_sample(['end Stim'])
        self.key_pressed_during_cue = False
        self.label.place(relx=0.4, rely=0.40)
        self.lblVar.set(cue)
        self.label.configure(image='', bg='black', fg='white')
        self.root.configure(bg='black')

        self.label_cue = tk.Label(bg='black', fg='white')
        im = Image.open('./KEYB.jpg')
        im = im.resize((200, 100), Image.ANTIALIAS)
        im2 = ImageTk.PhotoImage(im)
        self.label_cue.configure(image=im2, bg='black', fg='white')
        self.label_cue.image = im2
        self.label_cue.place(relx=0.42, rely=0.510)

        self.root.update_idletasks()
        self.outlet.push_sample(['Start Cue'])

        #Depending on which key is pressed, different functions are called
        self.root.bind('<Left>', self.wpress)
        self.root.bind('<Right>', self.lpress)

        #If no key is pressed, after 1 second the window expires and a message to be quicker is shown
        self.root.after(int(self.durationCue * 1000), self.check_choice)

    #If W is pressed --> it is evaluated whether the decision was correct or not and stored in 'accuracy'
    def wpress(self, event):
        self.root.unbind('<Left>')
        self.root.unbind('<Right>')
        self.key_pressed_during_cue = True
        self.root.update_idletasks()
        self.outlet.push_sample(['W Press'])
        self.root.after(0, self.cross)
        self.press = 'w'
        correct = self.categories[self.stimulus]

        if correct == self.press:
            self.letter = 'W'
            self.color = self.fb_color['Correct']
            self.accuracy[self.count] = 'Correct'
            self.sound = self.coin_sound

            self.outlet.push_sample(['Correct W'])
            self.root.update_idletasks()
        else:
            self.letter = 'L'
            self.color = self.fb_color['Incorrect']
            self.accuracy[self.count] = 'Incorrect'
            self.sound = self.buzz_sound

            self.outlet.push_sample(['Incorrect W'])
            self.root.update_idletasks()

    #If L is pressed --> it is evaluated whether the decision was correct or not and stored in 'accuracy' and settings for feedback are defined
    def lpress(self, event):
        self.root.unbind('<Right>')
        self.root.unbind('<Left>')
        self.key_pressed_during_cue = True
        self.root.update_idletasks()
        self.outlet.push_sample(['L Press'])
        self.root.after(0, self.cross)
        self.press = 'l'
        correct = self.categories[self.stimulus]

        if correct == self.press:
            self.letter = 'L'
            self.color = self.fb_color['Correct']
            self.accuracy[self.count] = 'Correct'
            self.sound = self.coin_sound

            self.outlet.push_sample(['Correct L'])
            self.root.update_idletasks()
        else:
            self.letter = 'W'
            self.color = self.fb_color['Incorrect']
            self.accuracy[self.count] = 'Incorrect'
            self.sound = self.buzz_sound

            self.outlet.push_sample(['Incorrect L'])
            self.root.update_idletasks()

    #Checks if button has been pressed, if not sends message
    def check_choice(self):
        if not self.key_pressed_during_cue:
            self.root.unbind('<Left>')
            self.root.unbind('<Right>')
            self.root.bind('<Left>', self.wpress2)
            self.root.bind('<Right>', self.lpress2)
            self.root.update_idletasks()
            self.outlet.push_sample(['Time Expired - No Choice'])
            self.root.after(0, self.message)
            self.press = 'None'

    #Shows a message warning to be faster
    def message(self):
        self.label_cue.destroy()
        if self.instructions == self.dutch_instructions:
            message = 'De tijd is om, reageer alstublieft sneller'
        elif self.instructions == self.eng_instructions:
            message = 'Time expired, please respond quicker'
        self.outlet.push_sample(['End cue - Start Warning'])
        self.label.pack(expand=1)
        self.lblVar.set(message)
        self.label.configure(bg='black', fg='red')
        self.root.configure(bg='black')
        self.root.update_idletasks()
        self.accuracy[self.count] = 'No answer'
        self.root.after(int(self.durationMessage * 1000), self.trial)
        self.root.after(0, self.stream)

    #Delay period with fixation cross of 500 ms
    def cross(self):
        self.outlet.push_sample(['Start Cross'])
        self.label_cue.destroy()
        self.label.pack(expand=1)
        self.lblVar.set('+')
        self.label.configure(bg='black', fg='white')
        self.root.configure(bg='black')
        self.root.update_idletasks()
        self.root.after(int(self.durationCross * 1000), self.fb)

    #Feedback presentation depending on accuracy on trial
    def fb(self):
        self.root.bind('<Left>', self.wpress2)
        self.root.bind('<Right>', self.lpress2)
        self.outlet.push_sample(['End Cross'])
        self.label.pack(expand=1)
        self.outlet.push_sample(['start Fb'])
        self.lblVar.set('')
        self.label.configure(bg=self.color, fg='black', command=self.play_sound(self.sound))
        self.root.configure(bg=self.color)
        self.root.update_idletasks()

        self.root.after(0, self.stream)
        self.root.after(int(self.durationFb * 1000), self.stop_sound)
        self.root.after(int(self.durationFb * 1000), self.trial)

    #plays sound during FB
    def play_sound(self, sound):
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play(loops=0)

    #stops sound when FB ends
    def stop_sound(self):
        pygame.mixer.music.stop()

    #Ends the experiment
    def end(self):
        self.outlet.push_sample(['End Experiment'])
        self.lblVar.set('End of experiment')
        self.label.configure(bg='black', fg='white')
        self.root.configure(bg='black')
        self.root.update_idletasks()

    #Closes window
    def close(self, event):
        self.outlet.push_sample(['Experiment Ended - ESC pressed'])
        self.root.destroy()

    #pushes stream when l is pressed at the wrong time
    def lpress2(self, event):
        self.outlet.push_sample(['L Press - wrong time'])

    #pushes stream when w is pressed at the wrong time
    def wpress2(self, event):
        self.outlet.push_sample(['W Press - wrong time'])

    #sends stream with summary trial info
    def stream(self):
        trial = self.trialn
        stimulus = self.stimulus
        repetition = self.presented_stim[self.stimulus]
        choice = self.press
        accuracy = self.accuracy[self.count]

        self.results[trial] = [stimulus, repetition, choice, accuracy]
        self.outlet.push_sample(['Sum Trail: ' + str(trial) + ', ' + str(stimulus) + ', ' + str(repetition) + ', ' + choice + ', ' + accuracy])



#Call the GUI
root = tk.Tk()
train_gui = DMGUI_Test(root, 0)
root.mainloop()