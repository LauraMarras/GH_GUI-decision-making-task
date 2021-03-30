import tkinter as tk
from PIL import ImageTk, Image
import Set_creation as sc
import pygame

    
#Create GUI
class DMGUI_Istructions:
    coin_sound = ('./Sound Stimuli/coins.mp3')
    buzz_sound = ('./Sound Stimuli/buzz.mp3')

    
    def __init__(self, root, pp_n):
        self.language = 'ENG'    
        self.instructions = 'Press <spacebar> to start'
        self.root = root
        pygame.mixer.init()

        #Retrieve or create stimuli set (one per pp --> to avoid repetition of stimuli)
        try:
            self.all_sets = sc.read_set(pp_n)
        except FileNotFoundError:
            sc.store_set(pp_n)
            self.all_sets = sc.read_set(pp_n)

        self.setinitial = self.all_sets['ins']
        self.set = []
        for s in self.setinitial:
            for _ in range(2):
                self.set.append(s)
        self.categories = sc.assign_categories(self.set)
        self.fb_color = sc.fb_color_association()
        self.presented_stim = {}

        #Layout
        self.width = self.root.winfo_screenwidth() * 3 / 3
        self.height = self.root.winfo_screenheight() * 3 / 3
        self.root.geometry('%dx%d+0+0' % (self.width, self.height))
        self.root.attributes('-fullscreen', True)
        self.root.title("Decision Making Task Instructions")
        self.root.configure(bg='black')

        #Language button
        if self.language == 'ENG':
            butt_text = 'DUTCH'
        elif self.language == 'DUTCH':
            butt_text = 'ENGLISH'
        self.lang_button = tk.Button(text=butt_text, fg='red', command=self.change_lang)
        self.lang_button.pack(pady=20)
        
    
        #Instructions label
        self.label = tk.Label(bg='black', fg='white', font=('Helvetica bold', 30))
        self.lblVar = tk.StringVar()
        self.label.configure(textvariable=self.lblVar)            
        self.lblVar.set(self.instructions)
        self.label.pack(expand=1)           
        
        #Press escape to close
        self.root.bind("<Escape>", self.close)

        #Press Spacebar to start example
        self.root.bind('<space>', self.example)

    #Change language of instructions
    def change_lang(self):
        if self.language == 'ENG':
            self.language = 'DUTCH'
            self.instructions = 'Drukt u op <spatiebalk> om te beginnen'
            self.lblVar.set(self.instructions)
            self.lang_button['text'] = "ENGLISH"
        
        elif self.language == 'DUTCH':
            self.language = 'ENG'
            self.instructions = 'Press <spacebar> to start'
            self.lblVar.set(self.instructions)
            self.lang_button['text'] = "DUTCH"

    #start example trial --> manually timed
    def example(self, event):
        self.lang_button.destroy()
        self.root.unbind('<space>')
        self.my_string = r'NOUN stimuli/{stim}{ext}'            
        self.stimulus = self.set.pop(0)
        self.stim_path = self.my_string.format(stim=str(self.stimulus), ext='.jpg')  #files are stored in folder with names from 1 to 60
        image = Image.open(self.stim_path)
        image = image.resize((500, 500), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(image)
        self.label.configure(image=test, bg='black', fg='white')
        self.root.configure(bg='black')
        self.label.image = test
        self.label.pack(expand=1)
        self.correct = self.categories[self.stimulus]
        self.root.bind('<space>', self.cue)

    #show cue to make choice    
    def cue(self, event):
        self.root.unbind('<space>')
        if self.language == 'ENG':
            cue = 'PRESS W or L'
        elif self.language == 'DUTCH':
            cue = 'DRUK W of L'
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

        #Depending on which key is pressed, call different function
        self.root.bind('<Left>', self.wpress)
        self.root.bind('<Right>', self.lpress)

    #If W is pressed --> evaluate whether the decision was correct or not and set feedback color and sound
    def wpress(self, event):
        self.root.unbind('<Left>')
        self.root.unbind('<Right>')
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

    #If L is pressed --> evaluate whether the decision was correct or not and set feedback color and sound
    def lpress(self, event):
        self.root.unbind('<Right>')
        self.root.unbind('<Left>')
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

    #Show fixation cross after choice for 0.5 secs
    def cross(self):
        self.label_cue.destroy()
        self.lblVar.set('+')
        self.label.configure(font=('Helvetica bold', 30), bg='black', fg='white')
        self.root.configure(bg='black')
        self.label.place(rely=0.5, relx=0.5)
        self.root.update_idletasks()
        self.root.after(500, self.fb)
    
    #Show feedback --> color+sound encode right vs wrong answer    
    def fb(self):
        self.label.pack(expand=1)
        self.lblVar.set('')
        self.label.configure(bg=self.color, fg='black', command=self.play_sound(self.sound))
        self.root.configure(bg=self.color)
        self.root.after(5000, self.stop_sound)

        if len(self.set) > 0:
            self.root.bind('<space>', self.example)
        
        else:
            self.root.bind('<space>', self.close)


    #play sound during FB
    def play_sound(self, sound):
        pygame.mixer.music.load(sound)
        pygame.mixer.music.play(loops=0)

    #stop sound when FB ends
    def stop_sound(self):
        pygame.mixer.music.stop()

   
    #close windows
    def close(self, event):
        self.root.destroy()


#Call GUI
root = tk.Tk()
instr_gui = DMGUI_Istructions(root, 0)
root.mainloop()

