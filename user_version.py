# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 12:18:34 2023

@author: Administrator
"""

import tkinter as tk
import os

window_dir = tk.Tk()
window_dir.title('Please type the file directory')

var = tk.StringVar()
var.set('''Please input the file directory like: "D:\\MyFile\\MineData" 
        Close this window after you confirm the directory.''')
l = tk.Label(window_dir, textvariable=var, bg='white', font=('Times New Roman', 12), height=4)
l.pack()


window_dir.geometry('400x200')
# e = tk.Entry(window, show="*")
e = tk.Entry(window_dir, show="")#Input text window
e.pack()

def get_dir_string():
    global dir_string
    dir_string = e.get()
    #t.insert('insert', var)
    #display_str = ''
    print(tk.messagebox.showinfo(title='Input updated', message='Your directory is:'+str(dir_string)))
    return 

b1 = tk.Button(window_dir, text='Confirm', width=15,
              height=2, command=get_dir_string)
b1.pack()

#print(tk.messagebox.showinfo(title='Your directory is:', message=str(var)))
tk.Button(window_dir, text="Quit", command=window_dir.destroy).pack() #button to close the window

#t = tk.Text(window_dir, height=2)
#t.pack()









window_dir.mainloop()



# =============================================================================
# Panel
# =============================================================================
window_panel = tk.Tk()
window_panel.title('Title')


try:
    os.chdir(dir_string)
    tk.messagebox.showinfo(title='Directory is fine', message='The directory has been set')
except Exception as ex:
    tk.messagebox.showerror(title='Wrong directory', message=ex)
    window_panel.destroy
    #print(ex)



window_dir.mainloop()















