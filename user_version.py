# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 12:18:34 2023

@author: Administrator
"""

import tkinter as tk
#from tkinter import *
import os
import pandas as pd
#import math

#Acyclic parameter
No_line_conf = False#confirm that the no. of line has been got
No_col_conf = False#confirm that the no. of column has been got

#Main window of the input part
window_dir = tk.Tk()
window_dir.title('Data-importing Tool')
window_dir.geometry('1000x700')

#frm_main = tk.Frame(window_dir)
#frm_main.pack()

#frm_l = tk.Frame(frm_main)
#frm_l.pack(side='left')

# =============================================================================
# File directory to get 'dir_string'
# =============================================================================
#Label for address
var_l_1 = tk.StringVar()
var_l_1.set('''1. Please input the file directory like: "D:\\MyFile\\MineData.csv". ''')
l_1 = tk.Label(window_dir, textvariable=var_l_1, bg='white', font=('Times New Roman', 12), height=4)
l_1.place(x=0, y=0, anchor='nw')

#Entry for address
# e = tk.Entry(window, show="*")
e_1 = tk.Entry(window_dir, show="", width=30)#Input text window
e_1.place(x=600, y=10, anchor='nw')

#Confirm bottom 
def get_dir_string():
    global dir_string
    dir_string = e_1.get()
    #t.insert('insert', var)
    #display_str = ''
    tk.messagebox.showinfo(title='Input updated', message='Your file directory is:'+str(dir_string))
    
    var_l_1.set('1. Please input the file directory like: "D:\\MyFile\\MineData.csv". \nFile directory received.')
    return 

tk.Button(window_dir, text='1. Confirm file directory', width=30,
              height=2, command=get_dir_string).place(x=600, y=32, anchor='nw')


#print(tk.messagebox.showinfo(title='Your directory is:', message=str(var)))

#t = tk.Text(window_dir, height=2)
#t.pack()

# =============================================================================
# Start line and column to get 'No_lin' & 'No_col'
# =============================================================================
var_l_2 = tk.StringVar()
#var_l_3 = tk.StringVar()

var_l_2.set('''2. Please input which line & column you want to start reading from: ''')
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
            var_l_2.set('''2. Please input which line (Confirmed) & column (Confirmed) \nyou want to start reading from: ''')
        else:
            var_l_2.set('''2. Please input which line (Confirmed) & column \nyou want to start reading from: ''')
        return
    except Exception as ex:
        tk.messagebox.showerror(title='Wrong No. of line', message=ex)
        if No_col_conf:
            var_l_2.set('''2. Please input which line & column (Confirmed) \nyou want to start reading from: ''')
        else:
            var_l_2.set('''2. Please input which line & column you want to start reading from: ''')
        return


def get_No_col():
    global No_col, No_col_conf
    try:
        No_col = int(e_2_2.get())
        tk.messagebox.showinfo(title='Input updated', message='Read from the column of:'+str(No_col))
        No_col_conf = True
        if No_line_conf:
            var_l_2.set('''2. Please input which line (Confirmed) & column (Confirmed) \nyou want to start reading from: ''')
        else:
            var_l_2.set('''2. Please input which line & column (Confirmed) \nyou want to start reading from: ''')
        return
    except Exception as ex:
        tk.messagebox.showerror(title='Wrong No. of column', message=ex)
        if No_line_conf:
            var_l_2.set('''2. Please input which line (Confirmed) & column \nyou want to start reading from: ''')
        else:
            var_l_2.set('''2. Please input which line & column you want to start reading from: ''')
        return



tk.Button(window_dir, text='2.1. Confirm No. of line', width=30,
              height=2, command=get_No_line).place(x=500, y=108, anchor='nw')
tk.Button(window_dir, text='2.2. Confirm No. of column', width=30,
              height=2, command=get_No_col).place(x=700, y=108, anchor='nw')

# =============================================================================
# Use columns list to get 'use_col'
# =============================================================================
#Label for use_col
var_l_3 = tk.StringVar()
var_l_3.set('''3. Please input which column/line you want to read (e.g., 1, 2, ...): ''')

l_3 = tk.Label(window_dir, textvariable=var_l_3, bg='white', font=('Times New Roman', 12), height=4)
l_3.place(x=0, y=140, anchor='nw')#y+70 from last label

#Entry for use_col
e_3 = tk.Entry(window_dir, show="", width=30)#Input line window
e_3.place(x=600, y=160, anchor='nw')

#Confirm bottom 
def get_use_col():
    global use_col
    use_col = []
    str_use_col = e_3.get()
    str_use_col = str_use_col.split(sep=',')
    try:
        for num in str_use_col:
            use_col.append(int(num.strip())-1)
        use_col = list(set(use_col))#Deduplication
        use_col_prt = []
        for x in use_col:
            x += 1
            use_col_prt.append(x)
        var_l_3.set('''3. Please input which column you want to read (e.g., 1, 2, ...)(Confirmed): ''')
        tk.messagebox.showinfo(title='Input updated', message='Use the column: '+str(use_col_prt))
        return
    except Exception as ex:
        tk.messagebox.showerror(title='Wrong No. of column', message=ex)
        return

tk.Button(window_dir, text='3. Confirm the used column', width=30,
              height=2, command=get_use_col).place(x=600, y=181, anchor='nw')

# =============================================================================
# Choose which feature is Datetime to get date_col
# =============================================================================
#Label
var_l_4 = tk.StringVar()
var_l_4.set('''4. Please input which Column/line is the datetime: ''')

l_4 = tk.Label(window_dir, textvariable=var_l_4, bg='white', font=('Times New Roman', 12), height=4)
l_4.place(x=0, y=210, anchor='nw')#y+70 from last label

#Entry
e_4 = tk.Entry(window_dir, show="", width=30)#Input line window
e_4.place(x=600, y=235, anchor='nw')

#Confirm bottom
def get_date_col():
    global date_col
    try:
        date_col = int(e_4.get())-1
        tk.messagebox.showinfo(title='Input updated', message='Datetime is the column/line of:'+str(date_col+1))
        var_l_4.set('''4. Please input which column/line is the datetime (Confirmed): ''')
    except Exception as ex:
        tk.messagebox.showerror(title='Wrong No. of column/line', message=ex)
    #if date_col in use_col:
        #use_col.remove(date_col)
    return

tk.Button(window_dir, text='4. Confirm the datetime column/line', width=30,
              height=2, command=get_date_col).place(x=600, y=254, anchor='nw')#y+=73

# =============================================================================
# If line/column a feature to get use_col_conf.get()
# =============================================================================
def print_l_5_selection():
    #print(use_col_conf.get())
    if use_col_conf.get() == 1: 
        #tk.messagebox.showinfo(title='Testing line/col selection', 
        #                       message='4. Is each column or each line a feature? (Columns are features.)')
        str_print = '5. Is each column or each line a feature? (Columns are features.)'
    else:
        #tk.messagebox.showinfo(title='Testing line/col selection', 
        #                       message='4. Is each column or each line a feature? (Lines are features.)')
        str_print = '5. Is each column or each line a feature? (Lines are features.)'
    var_l_5.set(str_print)
    #return

#Label 
var_l_5 = tk.StringVar()
var_l_5.set('''5. Is each column or each line a feature? ''')

l_5 = tk.Label(window_dir, textvariable=var_l_5, bg='white', font=('Times New Roman', 12), height=4)
l_5.place(x=0, y=280, anchor='nw')#y+70 from last label

#If use column as feature
use_col_conf = tk.IntVar(value=1)#By default each column is a feature

r1 = tk.Radiobutton(window_dir, text='Each Column is a feature.',
                    variable=use_col_conf, value=1,
                    command=print_l_5_selection)
r1.place(x=500, y=315, anchor='nw')

r2 = tk.Radiobutton(window_dir, text='Each Line is a feature.',
                    variable=use_col_conf, value=0,
                    command=print_l_5_selection)
r2.place(x=700, y=315, anchor='nw')


# =============================================================================
# Output directory to get out_string
# =============================================================================
#Label 
var_l_6 = tk.StringVar()
var_l_6.set('''6. Please input the output directory like: "D:\\MyFile\\myMineData". ''')

l_6 = tk.Label(window_dir, textvariable=var_l_6, bg='white', font=('Times New Roman', 12), height=4)
l_6.place(x=0, y=350, anchor='nw')#y+70 from last label

#Entry for address
# e = tk.Entry(window, show="*")
e_6 = tk.Entry(window_dir, show="", width=65)#Input text window
e_6.place(x=475, y=360, anchor='nw')

#Confirm bottom 
def get_out_string():
    global out_string
    out_string = e_6.get()
    #t.insert('insert', var)
    #display_str = ''
    tk.messagebox.showinfo(title='Input updated', message='Your output directory is:'+str(out_string))
    
    var_l_6.set('6. Please input the output directory like: "D:\\MyFile\\myMineData". \nOutput directory received.')
    return 

tk.Button(window_dir, text='6. Confirm output directory', width=30,
              height=2, command=get_out_string).place(x=600, y=380, anchor='nw')

# =============================================================================
# The end of the Input window 
# =============================================================================
def save_and_continue():
    #run with the parameters received
    global raw_data
    #Output file directory
    try:
        os.chdir(out_string)
        tk.messagebox.showinfo(title='Directory is fine', message='The output directory has been set')
    except Exception as ex:
        tk.messagebox.showerror(title='Wrong directory', message=ex)
        return
        #window_panel.destroy
        #print(ex)
    
    #Read file
    if use_col_conf.get() == 1:
        use_col_boolen = True
    elif use_col_conf.get() == 0:
        use_col_boolen = False
    print(use_col_boolen)
    
    if use_col_boolen:
        try:
            raw_data = pd.read_csv(filepath_or_buffer=dir_string, skiprows=No_lin-2,
                                   usecols=use_col, header=1)
            raw_data.index = range(0,len(raw_data))
        except Exception as ex:
            tk.messagebox.showerror(title='Failed to open the data file', message=ex)
            return
    else:
        try:
            raw_data = pd.read_csv(filepath_or_buffer=dir_string, skiprows=No_lin-2,
                                   usecols=use_col).T
            raw_data.index = range(0,len(raw_data))
            raw_data.columns = raw_data.iloc[0,:]
            raw_data = raw_data.iloc[1:,:]
            raw_data.index = range(0,len(raw_data))
        except Exception as ex:
            tk.messagebox.showerror(title='Failed to open the data file', message=ex)
            return
    
    raw_data.dropna(axis=1, how='all',inplace=True)
    raw_data.dropna(axis=0, how='all',inplace=True)
    
    #save the file to the output directory
    try:
        raw_data.to_csv(path_or_buf=out_string+'\\ExOutData.csv',index=False)
        tk.messagebox.showinfo(title='Processed data saved', 
                               message='The processed data has been saved successfully.')
    except Exception as ex:
        tk.messagebox.showerror(title='Failed to save the data file', message=ex)
        return

    #window_dir.destroy
    return

tk.Button(window_dir, text="Save & Continue", command=save_and_continue).pack(side='bottom') #button to close the window
window_dir.mainloop()

