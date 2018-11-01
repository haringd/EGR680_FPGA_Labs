# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 19:22:21 2018

@author: schwa
"""

#import tkinter as tk
import tkinter as tk
import turtle
import re
import atm_class
from time import asctime
import webbrowser
#from tkinter import Tk, Label, Button, messagebox\
#,Canvas

class ATM_GUI(tk.Frame):
    balance ='$0'
    withdraw ='$0'
    deposit = '$0'
    pin = '1234'
    file_error = 'error_log.txt'
    file_receipt = 'atm_receipt.txt'
    fo = None 
    fr = None
    
    def __init__(self, master=None):
        self.fo = self.init_error_file(self.fo, self.file_error)
        self.fr = self.init_receipt_file(self.fr, self.file_receipt)
        self.main_window = master
        
#        self.main_window = tk.Tk()
        self.main_window.title("ATM Bank Me")
        # .geometry() fixes windows size instead of downsizing with pack() 
        # but does not work with turtle
#        self.main_window.geometry('800x600+10+50') 
        self.display_CANVAS(self.main_window)
        self.welcomeAnim(self.t)
        self.frameQuit(self.frameBottom)
        self.framePin(self.frameWelcome)
        # Enter the tkinter main loop
#        self.main_window.mainloop()
        
    def init_error_file(self, file_descriptor, file_name):
        try:
            file_descriptor = open(file_name, "a")
            file_descriptor.write(asctime()+ ' ATM program starts '+ '\n')
            return file_descriptor
        except IOError as e:
            print('File '+e.filename+' could not be opened or writen to!') 
    
    def init_receipt_file(self, file_descriptor, file_name):
        try:
            file_descriptor = open(file_name, "w")
            file_descriptor.write('\n-------------------Bank Me-------------------\n')
            file_descriptor.write('---------------Transaction Receipt-----------\n')
            file_descriptor.write('*********************************************\n\n')
            return file_descriptor
        except IOError as e:
            print('File '+e.filename+' could not be opened or writen to!') 
            
    def log_error(self, string_error):
        if self.fo != None:
            self.fo.write(asctime()+' '+string_error+'\n')
        else:
            print('No error log file defined or initialiesd, use funtion \
                  init_error_file(self, file_descriptor, file_name)')
    def log_receipt(self, string_add_to_receipt):
        if self.fr != None:
            self.fr.write(string_add_to_receipt)
        else:
            print('No receipt file defined or initialiesd, use funtion \
                  init_receipt_file(self, file_descriptor, file_name)')
            self.log_error('No receipt file defined or initialiesd, use funtion \
                  init_receipt_file(self, file_descriptor, file_name)')
            
    def clsoeFile(self, file_descriptor):
        file_descriptor.close()
        
    def withdraw(self):
#        print("Withdraw!") # debugging only
#        print(int(re.sub('[^0-9]+', '', self.enWithdraw.get())) )  # debugging only
        if int(re.sub('[^0-9]+', '', self.balance)) >= int(re.sub('[^0-9]+', '', self.enWithdraw.get())):
            self.log_receipt('Your withdraw amounte is------------> $'\
                           +re.sub('[^0-9]+', '', self.enWithdraw.get())+'\n\n')
            self.setBalance( str(int(re.sub('[^0-9]+', '', self.balance)) - \
                                 int(re.sub('[^0-9]+', '', self.enWithdraw.get())) ) )
        else:
            self.log_error('Withdraw amount too big or not anouth balance')
#        print("Withdraw: " + self.balance) # debugging only
        self.setWithdraw('0')
        self.enWithdraw.delete(0, tk.END)
        self.enWithdraw.insert(0, self.withdraw)
    
    def messagebox(self): # only for debugin
        tk.messagebox.showinfo('Test1','Think you did part I!')
#        print("messagebox!") # debug only
        
    def deposit(self):
        #tk.messagebox.showinfo('Test1','Think you did part I!')
#        print(int(re.sub('[^0-9]+', '', self.enDeposit.get())) ) # debugging only
        self.log_receipt('Your deposit amounte is-------------> $'\
                           +re.sub('[^0-9]+', '', self.enDeposit.get())+'\n\n')
        self.setBalance( str(int(re.sub('[^0-9]+', '', self.balance)) + \
                             int(re.sub('[^0-9]+', '', self.enDeposit.get())) ) )
#        print("Deposit: " + self.balance) # debugging only
        self.setDeposit('0')
#        print(self.deposit) # debug only
        self.enDeposit.delete(0, tk.END)
        self.enDeposit.insert(0, self.deposit)
#        self.setDeposit(self.enDeposit.get())
        
    def getBalance(self):
        return int(re.sub('[^0-9]+', '', self.balance))
    
    def setBalance(self, balance):
        string = re.sub('[^0-9]+', '', balance)
        self.balance = '$'+str(string) 
        self.lbBalanceAmount['text'] = self.balance
    
    def getWithdraw(self):
        return int(re.sub('[^0-9]+', '', self.withdraw))
    
    def setWithdraw(self, withdraw):
        string = re.sub('[^0-9]+', '', withdraw)
        self.withdraw = '$'+str(string)
        
    def getDeposit(self):
        return int(re.sub('[^0-9]+', '', self.withdraw))
    
    def setDeposit(self, deposit):
        string = re.sub('[^0-9]+', '', deposit)
        self.deposit = '$'+str(string) 
        
    def pinValidation(self, inVal, pin):
#        print('Enter\n') # debug only
#        print(inVal) # debug only
        ret = 0
#        if self.pin == pin:
        if not re.match("^[0-9]{4}$", inVal):
#            print("Error! Make sure you only use numbers from 0-9 in PIN\n")
            self.log_error("Error! Make sure you only use numbers from 0-9 in PIN")
            inVal = 'Z'    
            ret = 0
        else:
            if inVal == pin:    
#                print("\nCorect PIN") # debug only
                self.enPIN.pack_forget()
                self.lbEnterPin.pack_forget()
                self.btPIN.pack_forget()
                self.enPIN.destroy()
                self.lbEnterPin.destroy()
                self.btPIN.destroy()
#                self.framePIN.pack_forget()
                self.welcome(self.frameWelcome)
                self.frameLabel(self.frameLeft)
                self.frameInput(self.frameCenter)
                self.frameCommand(self.frameRight)
                inVal = 'Z'  
                ret = 1
    #                break             
            else:        
                self.log_error("Invalid PIN!") 
#                print("Invalid PIN!\n")
                inVal = 'Z'  
                ret = 0
        return ret

    def closeProgram(self):
        self.log_error('Program Closed')
        self.log_receipt('Your checking account balance is----> $'\
                   +re.sub('[^0-9]+', '', self.balance)+'\n\n')
        self.log_receipt('THANK YOU FOR CHOOSING BANK ME!')
        self.clsoeFile(self.fo) # to ensure file is closed
        self.clsoeFile(self.fr) # to ensure file is closed
        webbrowser.open(self.file_receipt)
        self.main_window.destroy()
#        print('Goodby!')  # only for debuging
        
    def display_CANVAS(self, main_window):
        global canvas, logo
        #-------------------------------------------
        #Make canvaas child of root
        canvas = tk.Canvas(master = main_window, width = 500, height = 300, bg = 'green')
#        canvas.pack(side = 'top', fill = 'both', expand = 'yes')
#        explain = """Welcome to Bank Me's ATM """
#        canvas.create_text(170, 50, text=explain, font=('times',18), fill = 'blue')
#        close_button = tk.Button(canvas, text="Goodby!", 
#                                 command=self.main_window.destroy)
#        close_button.configure(width = 10, activebackground = "#33B5E5", relief = 'flat')
#        canvas.create_window(10, 10, anchor='nw', window=close_button)
        canvas.pack(side = tk.TOP)
                
        self.t = turtle.RawTurtle(canvas)
        screen = self.t.getscreen()# print(t.Screen().screensize()) 
        # This sets the lower left corner to 0,0 and the upper right corner to 600,600. 
        screen.setworldcoordinates(0,0,250,200)
        screen.bgcolor("green")
        
        # With the lines below, the "turtle" will look like a pencil.
        screen.register_shape("dollar_resize.gif")
        self.t.shape("dollar_resize.gif")

        # A frame is an invisible widget that holds other widgets. This frame goes 
        # on the right hand side of the window and holds the buttons and Entry widgets.
        self.frameControl = tk.Frame(master = main_window, width=500, height=100, background="green")
        self.frameControl.pack(side = tk.TOP,fill=tk.BOTH, ipady = 50)
        self.frameWelcome = tk.Frame(master = self.frameControl, width=300, height=20, background="green")
        self.frameWelcome.pack(side = tk.TOP,fill=tk.BOTH, ipady = 8)
#        self.framePIN = tk.Frame(master = self.frameControl, width=300, height=20, background="green")
#        self.framePIN.pack(side = tk.TOP,fill=tk.BOTH, ipady = 8)
        self.frameLeft = tk.Frame(master = self.frameControl, width=50, height=80, background = 'green')
        self.frameLeft.pack(side = tk.LEFT,fill=tk.BOTH, ipadx = 10)
        self.frameCenter = tk.Frame(master = self.frameControl, width=50, height=80, background = 'green')
        self.frameCenter.pack(side = tk.LEFT,fill=tk.BOTH, ipadx = 10)
        self.frameRight = tk.Frame(master = self.frameControl, width=50, height=80, background="green")
        self.frameRight.pack(side = tk.RIGHT,fill=tk.BOTH, ipadx = 10)
        self.frameBottom = tk.Frame(master = main_window, width=150, height=80, background="green")
        self.frameBottom.pack(side = tk.BOTTOM,fill=tk.BOTH, ipadx =8, ipady = 8)
          
    def framePin(self, frame ):
        self.lbEnterPin = tk.Label(master = frame, text = 'Enter PIN:', background='green', foreground = 'white')
        self.lbEnterPin.pack(side = tk.LEFT, anchor='center', ipadx=41, expand=True)
        self.enPIN = tk.Entry(master = frame)
        self.enPIN.pack(side = tk.LEFT, anchor='w', ipadx=0, expand=True)
        self.enPIN["textvariable"] = 'test'
#        self.enPIN.bind("<Return>", lambda: self.pinValidation(self.enPIN.get(), self.pin)) # problem with lambda
#        print('enPIN: ' + self.enPIN.get() +'\n')  # only for debuging
        self.btPIN = tk.Button(master = frame, text = "Enter", command = lambda: self.pinValidation(self.enPIN.get(), self.pin))
        self.btPIN.pack(side = tk.LEFT, anchor='w', ipadx=25, expand = True)
#        btTEST = tk.Button(master = frameWelcome, text = "Test", command = self.messagebox) # only for debuging
#        btTEST.pack(side = tk.LEFT, anchor='w', ipadx=20)
        
    def welcome(self, frame ):
        tk.Label(master = frame, 
                 text = 'Welcome to Bank ME', 
                 background='green', 
                 foreground = 'white').pack(side = tk.TOP, anchor='center', expand=True)
        
    def frameLabel(self, frame):
        # frameLeft
        lbWithdraw = tk.Label(master = frame, text = "Withdraw $", background = "green", foreground='white')
        lbWithdraw.pack(side = tk.TOP, anchor='center', ipadx=20, expand=True)
        lbDeposit = tk.Label(master = frame, text = "Deposit $", background = "green", foreground='white')
        lbDeposit.pack(side = tk.TOP, anchor='center', ipadx=20, expand=True)
        lbBalance = tk.Label(master = frame, text = "Balance $", background = "green", foreground='white')
        lbBalance.pack(side = tk.TOP, anchor='center', ipadx=20, expand=True)
        
    def frameInput(self, frameCenter):
        # frameCenter
        self.enWithdraw = tk.Entry(master = frameCenter)
        self.enWithdraw.pack(side = tk.TOP, anchor='w', ipadx=20, expand=True)
        self.enWithdraw.insert(0,'$0')
        self.enDeposit = tk.Entry(master = frameCenter)
        self.enDeposit.pack(side = tk.TOP, anchor='w', ipadx=20, expand=True)
        self.enDeposit.insert(0, '$0')
        self.lbBalanceAmount = tk.Label(master = frameCenter, text=self.balance)
        self.lbBalanceAmount.pack(side = tk.TOP, anchor='w', ipadx=20, expand=True)
        
    def frameCommand(self, frameRight):
        # frameRight
        btWithdraw = tk.Button(master = frameRight, text = "Withdraw", command = self.withdraw)
        btWithdraw.pack(side = tk.TOP, anchor='w', ipadx=20, expand=True)
        btDeposit = tk.Button(master = frameRight, text = "Deposit", command = self.deposit)
        btDeposit.pack(side = tk.TOP, anchor='w', ipadx=25, expand=True)
#        tk.Button(master = frameRight, text = "space",background = "green", 
#                  activebackground = "green", relief=tk.FLAT).pack(side = tk.TOP, anchor='w', ipadx=20, expand=True)
        tk.Label(master = frameRight, text='',background = "green").pack(side = tk.TOP, anchor='w', ipadx=20, expand=True)
    
    def frameQuit(self, frameBottom):
        # frameRight
        btQuit = tk.Button(master = frameBottom, text="Goodby!", background = "#FFFFFF", 
                  activebackground = "#33B5E5", 
                  command=self.closeProgram)
        btQuit.pack(side = tk.TOP, anchor='center', ipadx=25)
        
    def welcomeAnim(self, t):       
        # Animation
        t.pencolor("#FFFFFF") # WHITE
        t.pensize(2)
           
        t.penup()   # Regarding one of the comments
        t.forward(10)
        t.left(90)
        t.forward(10)
        t.pendown() # Regarding one of the comments
        # B
        t.right(90)
        t.circle(40, 180)
        
        t.right(180)
        t.circle(40, 180)
        t.stamp()
        t.left(90)
        t.forward(160)
        t.penup()   # Regarding one of the comments
        t.left(90)
        t.forward(40)
        t.pendown()   # Regarding one of the comments
        # A
        t.left(85)
        t.forward(160)
        t.stamp()
        t.right(170)
        t.forward(160)
        t.backward(80)
        t.left(265)
        t.forward(15)
        t.penup()   # Regarding one of the comments
        t.backward(25)
        t.left(90)
        t.pendown()   # Regarding one of the comments
        # N
        t.forward(80)
        t.backward(160)
        t.right(360-10)
        t.forward(160)
        t.left(180-10)
        t.forward(155)
        t.stamp()
        t.penup()   # Regarding one of the comments
        t.right(90)
        t.forward(10)
        t.pendown()   # Regarding one of the comments
        # K
        t.right(90)
        t.forward(160)
        t.backward(80)
        t.left(180-10)
        t.forward(80)
        t.stamp()
        t.backward(80)
        t.right(160)
        t.forward(80)
        t.penup()   # Regarding one of the comments
        t.left(90)
        t.forward(20)
        t.pendown()   # Regarding one of the comments
        # M
        t.left(80)
        t.forward(160)
        t.right(180-10)
        t.forward(80)
        t.left(180-20)
        t.forward(80)
        t.right(180-10)
        t.stamp()
        t.forward(160)
        t.penup()   # Regarding one of the comments
        t.left(90)
        t.forward(10)
        t.pendown()   # Regarding one of the comments
        # E
        t.left(90)
        t.forward(160)
        t.right(90)
        t.forward(40)
        t.stamp()
        t.backward(40)
        t.right(90)
        t.forward(80)
        t.left(90)
        t.forward(45)
        t.backward(45)
        t.right(90)
        t.forward(80)
        t.left(90)
        t.forward(40)
        t.stamp()
        
        
#GUI =Tk()
root = tk.Tk()
ATM = ATM_GUI(root)
ATM.main_window.mainloop()
#GUI.mainloop()