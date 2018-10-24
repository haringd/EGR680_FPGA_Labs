# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import time
import re

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
    print(" Main Menu")
    print("----------------------- \n")
    print(" 1. CHECK BALANCE")
    print(" 2. WITHDRAW CASH")
    print(" 3. DEPOSIT CASH")
    print(" 4. CHANGE PIN")
    print(" 5. EXIT ")
    return

def delay( msec ):
    cnt = 0
    while cnt < msec:
        cnt += 0.0001
    return

# Star program
print("\n    $$$$$          $$          $$$          $$   $$     $  ")
print("    $    $        $$$$         $$ $         $$   $$    $   ")
print("    $     $       $   $        $$  $        $$   $$   $    ") 
print("    $     $      $$   $$       $$   $       $$   $$  $     ")  
print("    $    $      $$     $$      $$    $      $$   $$ $      ")  
print("    $$$$$       $$     $$      $$     $     $$   $$$       ")  
print("    $$$$$       $$$$$$$$$      $$      $    $$   $$$       ")  
print("    $    $     $$       $$     $$       $   $$   $$ $      ")    
print("    $     $   $$         $$    $$        $  $$   $$  $     ")   
print("    $     $   $$         $$    $$         $ $$   $$   $    ")   
print("    $    $   $$           $$   $$          $$$   $$    $   ")  
print("    $$$$$    $$           $$   $$           $$   $$     $  \n") 
print("             $$$          $$   $$$$$$$$$$$$$$$  ")
print("             $$ $        $$$   $$$$$$$$$$$$$$$   ")
print("             $$  $      $ $$   $$      ") 
print("             $$   $    $  $$   $$     ")  
print("             $$    $  $   $$   $$     ")  
print("             $$     $$    $$   $$$$$$$$$$$$$$$       ")  
print("             $$           $$   $$$$$$$$$$$$$$$       ")  
print("             $$           $$   $$      ")    
print("             $$           $$   $$      ")   
print("             $$           $$   $$      ")   
print("             $$           $$   $$$$$$$$$$$$$$$   ")  
print("             $$           $$   $$$$$$$$$$$$$$$  ")  
print("------------------------------------------------------------")
print("                    Welcome to Bank Me  ")
print("============================================================")

# PIN validation
while True:
    inVal = input("Please enter your PIN: ") # regex
    if not re.match("^[0-9]{4}$", inVal):
        print ("Error! Make sure you only use numbers from 0-9 in PIN")
        inVal = 'Z'             
    else:
        if inVal == PIN :    
            #print("\nCorect PIN") # debug only
            print("\n")
            mainMenue()
            inVal = 'Z'  
            break             
        else:        
            print("\nInvalid PIN!")
            inVal = 'Z'  

# Main menu
while  select != "5":
    
    inVal = input("PLEASE SELECT FROM THE ABOVE OTPIONS: ")
    if not re.match("^[1-5]*$", inVal):
        print ("Error! Make sure you only use numbers from 1-5 in selecion")
    else:
        select = inVal
#    
    if select == '5': # exit
        exit
    elif select == '4': # change PIN
        while True:
            inVal = input("ENTER YOUR NEW PIN: ") # regex
            if not re.match("^[0-9]{4}$", inVal):
                print ("Error! Make sure you only use numbers from 0-9 in PIN")
                inVal = 'Z'             
            else:
                PIN = inVal
                inVal = 'Z'  
                print("\nYOUR NEW PIN IS", PIN, "\n")    
                delay(3000)
                mainMenue()
                break
    elif select == '3': # deposit
        while True:
            inVal = input("ENTER YOUR DEPOSIT AMOUNT: ") # regex
            if not re.match("^[0-9]*$", inVal):  
                amount = 0
                print("\nInvalid Input only nmbers are alowed.\n")
                delay(3000)
                mainMenue( )
                break
            else:    
                amount = int(inVal)
                if amount > AMOUNT_MIN and amount <= AMOUNT_MAX :  
                    account_value = account_value + amount
                    print("\nDEPOSIT AMOUNT $%.2f\n" % amount)    
                    amount = 0  
                    delay(3000)
                    mainMenue( )
                    break
                else:
                    print("\nDEPOSIT AMOUNT $%.2f TOO BIG OR TOO SMALL\n" % amount) 
                    print("\nENTER YOUR DEPOSIT AMOUNT: ")
            
    elif select == '2': # Whithdraw
        while True:
            inVal = input("ENTER YOUR WITHDRAW AMOUNT: ") # regex
            if not re.match("^[0-9]*$", inVal):  
                amount = 0
                print("\nInvalid Input only nmbers are alowed.\n")
                delay(3000)
                mainMenue( )
                break
            else:    
                amount = int(inVal)
                if amount >= AMOUNT_MIN and amount <= account_value :  
                    account_value = account_value - amount
                    print("\nWITHDRAW AMOUNT $%.2f\n" % amount)     
                    amount = 0  
                    delay(3000)
                    mainMenue( )
                    break
                else:
                    print("\nWITHDRAW AMOUNT $%.2f TOO BIG OR TOO SMALL\n" % amount) 
                    print("\nENTER YOUR WITHDRAW AMOUNT: ")            
    elif select == '1': # Balance
        print("\nYOUR BALANCE IS $%.2f \n \n\r" % account_value)
        delay(3000)
        mainMenue( )
    else:
        print("\nIncorrect Selecion!")
        
print("\nThank you for chosing BANK ME!")
        
