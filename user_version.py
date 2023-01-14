# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 12:18:34 2023

@author: Administrator
"""

import tkinter as tk
#from tkinter import *
import os

#Acyclic parameter
No_line_conf = False
No_col_conf = False

#Main window of the input part
window_dir = tk.Tk()
window_dir.title('Data-importing Tool')
window_dir.geometry('900x700')

#frm_main = tk.Frame(window_dir)
#frm_main.pack()

#frm_l = tk.Frame(frm_main)
#frm_l.pack(side='left')

# =============================================================================
# File directory
# =============================================================================
#Label for address
var_l_1 = tk.StringVar()
var_l_1.set('''1. Please input the file directory like: "D:\\MyFile\\MineData.csv". ''')
l_1 = tk.Label(window_dir, textvariable=var_l_1, bg='white', font=('Times New Roman', 12), height=4)
l_1.place(x=0, y=0, anchor='nw')


#Entry for address
# e = tk.Entry(window, show="*")
e_1 = tk.Entry(window_dir, show="")#Input text window
e_1.place(x=600, y=10, anchor='nw')

#Confirm bottom 
def get_dir_string():
    global dir_string
    dir_string = e_1.get()
    #t.insert('insert', var)
    #display_str = ''
    tk.messagebox.showinfo(title='Input updated', message='Your directory is:'+str(dir_string))
    var_l_1.set('1. Please input the file directory like: "D:\\MyFile\\MineData.csv". \nFile directory received.')
    return 

tk.Button(window_dir, text='1. Confirm', width=15,
              height=2, command=get_dir_string).place(x=600, y=35, anchor='nw')


#print(tk.messagebox.showinfo(title='Your directory is:', message=str(var)))

#t = tk.Text(window_dir, height=2)
#t.pack()

# =============================================================================
# Start line and column
# =============================================================================
var_l_2 = tk.StringVar()
#var_l_3 = tk.StringVar()

var_l_2.set('''2. Please input which LINE & COLUMN you want to start reading from: ''')
#var_l_3.set('''2. Please input which COLUMN you want to start reading from: ''')

l_2 = tk.Label(window_dir, textvariable=var_l_2, bg='white', font=('Times New Roman', 12), height=4)
l_2.place(x=0, y=70, anchor='nw')#y+70 from last label

#Entry for line and column
# e = tk.Entry(window, show="*")
e_2_1 = tk.Entry(window_dir, show="", width=30)#Input line window
e_2_1.place(x=500, y=85, anchor='nw')

e_2_2 = tk.Entry(window_dir, show="", width=30)#Input column window
e_2_2.place(x=700, y=85, anchor='nw')

#Confirm bottom 


def get_No_line():
    global No_lin, No_line_conf
    try:
        No_lin = int(e_2_1.get())
        tk.messagebox.showinfo(title='Input updated', message='Read from the line of:'+str(No_lin))
        No_line_conf = True
        if No_col_conf:
            var_l_2.set('''2. Please input which LINE (Confirmed) & COLUMN (Confirmed) \nyou want to start reading from: ''')
        else:
            var_l_2.set('''2. Please input which LINE (Confirmed) & COLUMN \nyou want to start reading from: ''')
        return
    except Exception as ex:
        tk.messagebox.showerror(title='Wrong No. of line', message=ex)
        if No_col_conf:
            var_l_2.set('''2. Please input which LINE & COLUMN (Confirmed) \nyou want to start reading from: ''')
        else:
            var_l_2.set('''2. Please input which LINE & COLUMN you want to start reading from: ''')
        return


def get_No_col():
    global No_col, No_col_conf
    try:
        No_col = int(e_2_2.get())
        tk.messagebox.showinfo(title='Input updated', message='Read from the column of:'+str(No_col))
        No_col_conf = True
        if No_line_conf:
            var_l_2.set('''2. Please input which LINE (Confirmed) & COLUMN (Confirmed) \nyou want to start reading from: ''')
        else:
            var_l_2.set('''2. Please input which LINE & COLUMN (Confirmed) \nyou want to start reading from: ''')
        return
    except Exception as ex:
        tk.messagebox.showerror(title='Wrong No. of column', message=ex)
        if No_line_conf:
            var_l_2.set('''2. Please input which LINE (Confirmed) & COLUMN \nyou want to start reading from: ''')
        else:
            var_l_2.set('''2. Please input which LINE & COLUMN you want to start reading from: ''')
        return

tk.Button(window_dir, text='2.1. Confirm No. of line', width=20,
              height=2, command=get_No_line).place(x=500, y=108, anchor='nw')
tk.Button(window_dir, text='2.2. Confirm No. of column', width=20,
              height=2, command=get_No_col).place(x=700, y=108, anchor='nw')

# =============================================================================
# The end of the Input window 
# =============================================================================
tk.Button(window_dir, text="Save & Continue", command=window_dir.destroy).pack(side='bottom') #button to close the window
window_dir.mainloop()














# =============================================================================
# Panel
# =============================================================================


try:
    os.chdir(dir_string)
    tk.messagebox.showinfo(title='Directory is fine', message='The directory has been set')
except Exception as ex:
    tk.messagebox.showerror(title='Wrong directory', message=ex)
    #window_panel.destroy
    #print(ex)






# =============================================================================
# Testing codes
# =============================================================================










