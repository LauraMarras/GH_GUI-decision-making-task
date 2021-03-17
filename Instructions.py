import tkinter as tk
from PIL import ImageTk, Image

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
    
    def __init__(self, root):
        self.root = root
        
        #Layout
        self.width = self.root.winfo_screenwidth() * 3 / 3
        self.height = self.root.winfo_screenheight() * 3 / 3
        self.root.geometry('%dx%d+0+0' % (self.width, self.height))
        #self.root.attributes('-fullscreen', True)
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
        self.lang_button.grid(pady=20)

    
        # Configuration instructions label
        self.instructions_label = tk.Label(anchor='w', justify='left', font=('Helvetica bold', 15), bg='black', fg='white')
        self.lblVar = tk.StringVar()
        self.instructions_label.configure(textvariable=self.lblVar)
        self.lblVar.set(self.instructions[self.page])
        self.instructions_label.grid(padx=150, ipady=20)
        self.root.update_idletasks

        # Configuration of instructions image label
        self.image_label = tk.Label(bg='black', fg='white')
        im = Image.open(self.im_path.format(name=self.language+str(self.page)))
        im = im.resize((900, 300), Image.ANTIALIAS)
        im2 = ImageTk.PhotoImage(im)
        self.image_label.configure(image=im2, bg='black', fg='white')
        self.image_label.image = im2
        self.image_label.grid()

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
    
    # closes windows
    def close(self, event):
        self.root.destroy()
