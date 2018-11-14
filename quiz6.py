# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 18:08:45 2018

@author: schwa
"""
#import tkinter as tk
import tkinter as tk
import re
from time import asctime
import webbrowser

class ATM_GUI(tk.Frame):
    aver = 0
    
    def __init__(self, master=None):
        self.main_window = master
        self.display_CANVAS(self.main_window)

        
    def display_CANVAS(self, main_window):
        global canvas, logo
        #-------------------------------------------
        #Make canvaas child of root
        canvas = tk.Canvas(master = main_window)
        canvas.pack(side = tk.TOP)   

        # A frame is an invisible widget that holds other widgets. This frame goes 
        # on the right hand side of the window and holds the buttons and Entry widgets.
        self.frame1 = tk.Frame(master = canvas)
        self.frame1.pack(side = tk.TOP,fill=tk.BOTH, ipadx = 8, ipady = 2)
        self.frame2 = tk.Frame(master = canvas)
        self.frame2.pack(side = tk.TOP,fill=tk.BOTH, ipadx = 8, ipady = 2)
        self.frame3 = tk.Frame(master = canvas)
        self.frame3.pack(side = tk.TOP,fill=tk.BOTH, ipadx = 8, ipady = 2)
        self.frame4 = tk.Frame(master = canvas)
        self.frame4.pack(side = tk.TOP,fill=tk.BOTH, ipadx = 8, ipady = 2)
        self.frame5 = tk.Frame(master = canvas)
        self.frame5.pack(side = tk.TOP) #fill=tk.BOTH,
#        self.frame6 = tk.Frame(master = canvas,  background="green")
#        self.frame6.pack(side = tk.RIGHT,fill=tk.BOTH, ipadx = 8, ipady = 2)

        self.lb1 = tk.Label(master = self.frame1, text = 'Enter the score for test 1:')
        self.lb1.pack(side = tk.LEFT, anchor='center', expand=True)
        self.en1 = tk.Entry(master = self.frame1)
        self.en1.pack(side = tk.LEFT, anchor='w',  expand=True)
        
        self.lb2 = tk.Label(master = self.frame2, text = 'Enter the score for test 2:')
        self.lb2.pack(side = tk.LEFT, anchor='center', expand=True)
        self.en2 = tk.Entry(master = self.frame2)
        self.en2.pack(side = tk.LEFT, anchor='w',  expand=True)
    
        self.lb3 = tk.Label(master = self.frame3, text = 'Enter the score for test 3:')
        self.lb3.pack(side = tk.LEFT, anchor='center', expand=True)
        self.en3 = tk.Entry(master = self.frame3)
        self.en3.pack(side = tk.LEFT, anchor='w', expand=True)
        
        self.lb4 = tk.Label(master = self.frame4, text = 'Avarage: ')
        self.lb4.pack(side = tk.LEFT, anchor='center', expand=True)
        
        self.btAverage = tk.Button(master = self.frame5, text = "Average:", command = self.average)
        self.btAverage.pack(side = tk.LEFT, anchor='center')
        
        self.btQuit = tk.Button(master = self.frame5, text="Quit", command= self.main_window.destroy )
        self.btQuit.pack(side = tk.RIGHT)
        
    def average(self):
       self.aver = (float(re.sub('[^0-9.]+', '', self.en1.get()))+ float(re.sub('[^0-9.]+', '', self.en2.get()))+  float(re.sub('[^0-9.]+', '', self.en3.get())))/3
#       self.aver = (float(self.en1.get())+ float(self.en1.get())+  float(self.en1.get()))/3
  
       string = 'Average: %s' % str(self.aver)
       self.lb4['text'] = string
       
        
root = tk.Tk()
ATM = ATM_GUI(root)
ATM.main_window.mainloop()
