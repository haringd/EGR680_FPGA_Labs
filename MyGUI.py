# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 19:22:21 2018

@author: schwa
"""

#import tkinter as tk

from tkinter import Tk, Label, Button, messagebox

class SimplGui:
    def __init__(self, master):
        self.master = master
        master.title("My Simple GUI")
        
        self.label = Label(master, text="Press the button below to send a greeting!")
        self.label.pack()
        
        self.greet_button = Button(master, text="Hello", command=self.greet)
        self.greet_button.pack()
        
        self.msg_button = Button(master, text="Click Me", command=self.message)
        self.msg_button.pack()
        
        self.close_button = Button(master, text="Goodby!", command=self.master.destroy)
        self.close_button.pack()
        
        
    def greet(self):
        print("Hello!")
        
    def message(self):
        messagebox.showinfo('Test1','Think you did part I!')
        
GUI =Tk()
My_simpe_gui = SimplGui(GUI)
GUI.mainloop()