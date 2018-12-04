# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 19:43:49 2018

@author: schwa
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import time
import re
import turtle

AMOUNT_MIN = 0
AMOUNT_MAX = 1000

user = 0
PIN  = "1234"
newPIN = "99999999999999"
select = 0
account_value = 0
amount = 0
inVal = 'Z'

def mainMenue( ):
#    print(" Main Menu")
#    print("----------------------- \n")
#    print(" 1. CHECK BALANCE")
#    print(" 2. WITHDRAW CASH")
#    print(" 3. DEPOSIT CASH")
#    print(" 4. CHANGE PIN")
#    print(" 5. EXIT ")
    print('Enter 1 -> Paint screen in Blue color')
    print('Enter 2 -> To draw SUN')
    print('Enter 3 -> To draw HOUSE')
    print('Enter 4 -> To draw DOOR')
    print('Enter 5 -> To draw DRIVEWAY')
    print('Enter 6 -> Exit Programr')
    return

def delay( msec ):
    cnt = 0
    while cnt < msec:
        cnt += 0.0001
    return

# Star program


## PIN validation
#while True:
#    inVal = input("Please enter your PIN: ") # regex
#    if not re.match("^[0-9]{4}$", inVal):
#        print ("Error! Make sure you only use numbers from 0-9 in PIN")
#        inVal = 'Z'             
#    else:
#        if inVal == PIN :    
#            #print("\nCorect PIN") # debug only
#            print("\n")
#            mainMenue()
#            inVal = 'Z'  
#            break             
#        else:        
#            print("\nInvalid PIN!")
#            inVal = 'Z'  
mainMenue()
turtle.pendown()
# Main menu
while  select != "6":
    
    inVal = input("PLEASE SELECT FROM THE ABOVE OTPIONS: ")
    if not re.match("^[1-6]*$", inVal):
        print ("Error! Make sure you only use numbers from 1-6 in selecion")
    else:
        select = inVal
#    
    if select == '6': # exit
        turtle.bye()
        exit
    elif select == '5': # DRIVEWAY
        turtle.penup()
        turtle.goto(5,0)
        turtle.setheading(0)
        turtle.pendown()
        turtle.fillcolor("gray")
        turtle.begin_fill()
        turtle.goto(105,0)
        turtle.goto(110,-100)
        turtle.goto(-5,-100)
        turtle.end_fill()
        turtle.penup()
        mainMenue( )
    elif select == '4': # DOOR
        turtle.penup()
        turtle.goto(20,0)
        turtle.setheading(0)
        turtle.pendown()
        turtle.fillcolor("black")
        turtle.begin_fill()
        turtle.left(90)
        turtle.forward(80)
        turtle.right(90)
        turtle.forward(40)
        turtle.right(90)
        turtle.forward(80)
        turtle.end_fill()
        # 
        turtle.penup()
        turtle.goto(30,40)
        turtle.setheading(0)
        turtle.pendown()
        turtle.fillcolor("yellow")
        turtle.begin_fill()
        turtle.circle(5)
        turtle.end_fill()
        mainMenue( )  

    elif select == '3': # HOUSE
#        turtle.reset()
        turtle.penup()
        turtle.goto(0,0)
        turtle.setheading(0)
        turtle.pendown()
        turtle.left(90)
        turtle.forward(100)
        turtle.right(45)
        turtle.fillcolor("red")
        turtle.begin_fill()
        turtle.forward(141)
        turtle.right(90)
        turtle.forward(141)
        turtle.end_fill()
        turtle.right(45)
        turtle.forward(100)
        turtle.fillcolor("white")
        turtle.begin_fill()
        turtle.right(90)
        turtle.forward(200)
        turtle.right(90)
        turtle.forward(100)
        turtle.right(90)
        turtle.forward(200)
        turtle.right(90)
        turtle.forward(100)
        turtle.end_fill()
        mainMenue( )  
            
    elif select == '2': # Sun
        turtle.penup()
        turtle.goto(200,200)
        turtle.pendown()
        turtle.fillcolor("yellow")
        turtle.begin_fill()
        turtle.circle(80)
        turtle.end_fill()
        mainMenue( )      
    elif select == '1': # Balance
        screen = turtle.Screen()
        screen.bgcolor('blue')
        mainMenue( )
    else:
        print("\nIncorrect Selecion!")
        
print("\nThank you!")
        
