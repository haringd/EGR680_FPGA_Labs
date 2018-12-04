# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 19:22:46 2018

@author: schwa
"""

import turtle

class Exam():

    tr = turtle.Turtle()
    
    def __init__(self, AccountValue, Pin):  

    
    def mainMenue(self):
        print('Enter 1 -> Paint screen in Blue color')
        print('Enter 2 -> To draw SUN')
        print('Enter 3 -> To draw HOUSE')
        print('Enter 4 -> To draw DOOR')
        print('Enter 5 -> To draw DRIVEWAY')
        print('Enter 6 -> Exit Programr')
        
    # Print Receipt
    def sun(self, tr):
        tr.circle(100)

app = Exam()
