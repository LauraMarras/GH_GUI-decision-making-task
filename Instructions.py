import tkinter as tk
from PIL import ImageTk, Image
import pygame
import Set_creation as sc

#Reads instructions from txt file and creates 3 sections
def read_instructions(language):
    with open ('{} instructions.txt'.format(language), 'rt', encoding='UTF-8') as instructions_file:
        instructions_text = instructions_file.read()
        lines = instructions_text.split('\n')             
        instructions = {1: '', 2: '', 3: ''}
       
        for line in lines:
            instructions[int(line[0])] += line[1:] + '\n'

    return instructions
    
#Creates GUI
class DMGUI_Istructions:
    language = 'ENG'
    instructions = read_instructions(language)
    page = 1
    im_path = 'C:/Users/laura/OneDrive/Documenti/GitHub/GUI-decision-making-task/Instr_images/{name}.jpg'
    
    #Set number of trials and windows durations
    numTrials = 2
    trialn = 0
    durationStimuli = 3
    durationCross = 0.5
    durationCue = 6
    durationFb = 3
    durationMessage = 2

    stim_path = ''
    coin_sound = (r'Sound Stimuli/coins.mp3')
    buzz_sound = (r'Sound Stimuli/buzz.mp3')


    def __init__(self, root):
        pygame.mixer.init()
        self.root = root
        self.set_train = sc.create_set()
        self.set = sc.create_runs(self.set_train)
        self.categories = sc.assign_categories(self.set_train)
        self.fb_color = sc.fb_color_association()
        self.presented_stim = {}
        self.press = ''
        for s in self.set:
            self.presented_stim[s] = 0
        
        #Layout
        self.width = self.root.winfo_screenwidth() * 3 / 3
        self.height = self.root.winfo_screenheight() * 3 / 3
        self.root.geometry('%dx%d+0+0' % (self.width, self.height))
        self.root.attributes('-fullscreen', True)
        self.root.title("Decision Making Task Instructions")
        self.root.configure(bg='black')

       
        #Press escape to close
        self.root.bind("<Escape>", self.close)

        #Press arrow to change page
        self.root.bind('<Right>', self.next_page)
        self.root.bind('<Left>', self.prev_page)

        self.root.after(0, self.objects)

    def objects(self):
        #language button
        if self.language == 'ENG':
            butt_text = 'DUTCH'
        elif self.language == 'DUTCH':
            butt_text = 'ENGLISH'
        self.lang_button = tk.Button(text=butt_text, fg='red', command=self.change_lang)
        self.lang_button.grid(columnspan=2, row=0, pady=20, sticky='')

    
        # Configuration instructions label
        self.instructions_label = tk.Label(anchor='w', justify='left', font=('Helvetica bold', 15), bg='black', fg='white')
        self.lblVar = tk.StringVar()
        self.instructions_label.configure(textvariable=self.lblVar)
        self.lblVar.set(self.instructions[self.page])
        self.instructions_label.grid(column=0, row=1, padx=50, ipady=20)
        self.root.update_idletasks

        # Configuration of instructions image label
        self.image_label = tk.Label(bg='black', fg='white')
        im = Image.open(self.im_path.format(name=self.language+str(self.page)))
        im = im.resize((450, 650), Image.ANTIALIAS)
        im2 = ImageTk.PhotoImage(im)
        self.image_label.configure(image=im2, bg='black', fg='white')
        self.image_label.image = im2
        self.image_label.grid(column=1, row=1, sticky='E')
    
        if self.page == 3:
             self.root.bind('<space>', self.start_train)

    # Changes language of instructions
    def change_lang(self):
        if self.language == 'ENG':
            self.language = 'DUTCH'
            self.instructions = read_instructions(self.language)
            self.lblVar.set(self.instructions[self.page])
            self.lang_button['text'] = "ENGLISH"
            im = Image.open(self.im_path.format(name=self.language+str(self.page)))
            im = im.resize((900, 300), Image.ANTIALIAS)
            im2 = ImageTk.PhotoImage(im)
            self.image_label.configure(image=im2, bg='black', fg='white')
            self.image_label.image = im2
        elif self.language == 'DUTCH':
            self.language = 'ENG'
            self.instructions = read_instructions(self.language)
            self.lblVar.set(self.instructions[self.page])
            self.lang_button['text'] = "DUTCH"
            im = Image.open(self.im_path.format(name=self.language+str(self.page)))
            im = im.resize((900, 300), Image.ANTIALIAS)
            im2 = ImageTk.PhotoImage(im)
            self.image_label.configure(image=im2, bg='black', fg='white')
            self.image_label.image = im2
    
    def next_page(self, event):
        if self.page < 3:
            self.page += 1
            self.root.after(0, self.remove_obj)
            self.root.after(0, self.objects)
        else:
            self.page = 3
    
    def prev_page(self, event):
        if self.page > 1:
            self.page -= 1
            self.root.after(0, self.remove_obj)
            self.root.after(0, self.objects)
        else:
            self.page = 1
    
    def remove_obj(self):
        self.lang_button.destroy()
        self.instructions_label.destroy()
        self.image_label.destroy()
    
    #closes windows
    def close(self, event):
        self.root.destroy()
    
    #Start train
    def start_train(self, event):
        self.root.after(0, self.remove_obj)
        self.root.unbind ('<Left>')
        self.root.unbind('<Right>')
        self.root.unbind('<space>')
        
        #Configuration Label
        self.label = tk.Label(font=('Helvetica bold', 30), bg='black', fg='white')
        self.root.configure(bg='black')
        self.lblVar = tk.StringVar()
        self.label.configure(textvariable=self.lblVar)
        self.lblVar.set('+')
        self.label.place(relx=0.5, rely=0.5)

        if self.numTrials == 0 or len(self.set) == 0:
            self.root.after(0, self.end)
        else:
            self.numTrials = self.numTrials - 1
            self.trialn = 2 - self.numTrials
            
            self.root.after(int(self.durationCross * 3000), self.stim)
            self.root.update_idletasks()
        
    #Stimulus presentation
    def stim(self):
        self.stimulus = self.set.pop(0)
        self.my_string = r'NOUN stimuli/{stim}{ext}'
        self.stim_path = self.my_string.format(stim=str(self.stimulus), ext='.jpg')  # files are stored in folder with names from 1 to 60
        image = Image.open(self.stim_path)
        image = image.resize((500, 500), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(image)
        self.label.configure(image=test, bg='black', fg='white')
        self.root.configure(bg='black')
        self.label.image = test
        self.label.place(relx = 0, rely=0)
        self.root.update_idletasks()

        self.root.after(int(self.durationStimuli * 1000), self.cue)

    #Cue that indicates to make decision
    def cue(self):
        if self.language == 'DUTCH':
            cue = 'DRUK W of L'
        elif self.language == 'ENG':
            cue = 'PRESS W or L'
        self.key_pressed_during_cue = False
        self.label.place(relx=0.4, rely=0.40)
        self.lblVar.set(cue)
        self.label.configure(image='', bg='black', fg='white')
        self.root.configure(bg='black')

        self.label_cue = tk.Label(bg='black', fg='white')
        im = Image.open(r'KEYB.jpg')
        im = im.resize((200, 100), Image.ANTIALIAS)
        im2 = ImageTk.PhotoImage(im)
        self.label_cue.configure(image=im2, bg='black', fg='white')
        self.label_cue.image = im2
        self.label_cue.place(relx=0.42, rely=0.510)

        self.root.update_idletasks()

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
        self.root.after(0, self.cross)
        self.press = 'w'
        correct = self.categories[self.stimulus]

        if correct == self.press:
            self.letter = 'W'
            self.color = self.fb_color['Correct']
            self.sound = self.coin_sound
        else:
            self.letter = 'L'
            self.color = self.fb_color['Incorrect']
            self.sound = self.buzz_sound

    #If L is pressed --> it is evaluated whether the decision was correct or not and stored in 'accuracy' and settings for feedback are defined
    def lpress(self, event):
        self.root.unbind('<Right>')
        self.root.unbind('<Left>')
        self.key_pressed_during_cue = True
        self.root.update_idletasks()
        self.root.after(0, self.cross)
        self.press = 'l'
        correct = self.categories[self.stimulus]

        if correct == self.press:
            self.letter = 'L'
            self.color = self.fb_color['Correct']
            self.sound = self.coin_sound
        else:
            self.letter = 'W'
            self.color = self.fb_color['Incorrect']
            self.sound = self.buzz_sound

    #Checks if button has been pressed, if not sends message
    def check_choice(self):
        if not self.key_pressed_during_cue:
            self.root.unbind('<Left>')
            self.root.unbind('<Right>')
            self.root.after(0, self.message)
            self.press = 'None'

    #Shows a message warning to be faster
    def message(self):
        self.label_cue.destroy()
        if self.language == 'DUTCH':
            message = 'De tijd is om, reageer alstublieft sneller'
        elif self.language == 'ENG':
            message = 'Time expired, please respond quicker'
        self.label.place(relx = 0, rely=0)
        self.lblVar.set(message)
        self.label.configure(bg='black', fg='red')
        self.root.configure(bg='black')
        self.root.update_idletasks()
        self.root.after(int(self.durationMessage * 1000), self.start_train)
        
    #Delay period with fixation cross of 500 ms
    def cross(self):
        self.label_cue.destroy()
        self.label.place(relx = 0, rely=0)
        self.lblVar.set('+')
        self.label.configure(bg='black', fg='white')
        self.root.configure(bg='black')
        self.root.update_idletasks()
        self.root.after(int(self.durationCross * 1000), self.fb)

    #Feedback presentation depending on accuracy on trial
    def fb(self):
        self.label.place(relx = 0, rely=0)
        self.lblVar.set(self.letter)
        self.label.configure(bg=self.color, fg='black', command=self.play_sound(self.sound))
        self.root.configure(bg=self.color)
        self.root.update_idletasks()

        self.root.after(int(self.durationFb * 1000), self.stop_sound)
        self.root.after(int(self.durationFb * 1000), self.start_train)

    #plays sound during FB
    def play_sound(self, sound):
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play(loops=0)

    #stops sound when FB ends
    def stop_sound(self):
        pygame.mixer.music.stop()

    #Ends the experiment
    def end(self):
        self.lblVar.set('Great job! Now you can start the experiment')
        self.label.configure(bg='black', fg='white')
        self.root.configure(bg='black')
        self.root.update_idletasks()
        

root = tk.Tk()
instr_gui = DMGUI_Istructions(root)
root.mainloop()
