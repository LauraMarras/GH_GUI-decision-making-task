import Set_creation as sc
import tkinter as tk
import Instructions as ins
import Training as tr
import Test as test


#Create sets
set_train, set_test = sc.create_set()

#Create Root
root = tk.Tk()

#instr_gui = ins.DMGUI_Istructions(root)
#train_gui = tr.DMGUI_Training(root, set_train)
test_gui = test.DMGUI_Test(root, set_test)

#root.mainloop()
#root.mainloop()
root.mainloop()
