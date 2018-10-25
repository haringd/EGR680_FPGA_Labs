# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 18:34:49 2018

@author: schwa
"""
import re
# Print Receipt
def receipt(filename, file):
    file.write('THANK YOU FOR CHOOSING BANK ME!')
    file.close()
    file = open(filename, "r")
    for line in file:
        print(line, end='')
    file.close()
    return 1
# Balance 
def balance( account_value , file):
    print("\nYOUR BALANCE IS $%.2f \n \n\r" % account_value)
    file.write('Your checking account balance is----> $'\
               +str(account_value)+'\n\n')
    delay(3000)
    mainMenue( )
    return 1
# Withdraw money
def withdraw( inVal, AMOUNT_MIN, AMOUNT_MAX, account_value, file ):
    ret = [0, 0]; # no error 1, error 0
    amount = 0
    if not re.match("^[0-9]*$", inVal):  
        amount = 0
        print("\nInvalid Input only nmbers are alowed.\n")
        ret=[0, inVal]
    else:    
        amount = int(inVal)
        if amount >= AMOUNT_MIN and amount <= account_value :  
            account_value = account_value - amount
            print("\nWITHDRAW AMOUNT $%.2f\n" % amount)   
            file.write('Your withdraw amounte is------------> $'\
                       +str(amount)+'\n\n')
            amount = 0  
            delay(3000)
            mainMenue( )
            ret=[1, account_value]
        else:
            ret=[0, inVal]
            print("\nWITHDRAW AMOUNT $%.2f TOO BIG OR TOO SMALL\n" % amount) 
    return ret
# Deposit money
def deposit( inVal, AMOUNT_MIN, AMOUNT_MAX, account_value, file ):
    ret = [0, 0]; # no error 1, error 0
    amount = 0
    if not re.match("^[0-9]*$", inVal):  
        amount = 0
        print("\nInvalid Input only numbers are alowed.\n")
        ret=[0, inVal]
    else:    
        amount = int(inVal)
        if amount >= AMOUNT_MIN and amount <= AMOUNT_MAX :  
            account_value = account_value + amount
            print("\nDEPOSIT AMOUNT $%.2f\n" % amount)   
            file.write('Your deposit amounte is-------------> $'\
                       +str(amount)+'\n\n')
            amount = 0  
            delay(3000)
            mainMenue( )
            ret=[1, account_value]
        else:
            ret=[0, inVal]
            print("\nDEPOSIT AMOUNT $%.2f TOO BIG OR TOO SMALL\n" % amount) 
    return ret
# set new pin
def newPin( inVal, file ):
    ret = [0, 0]; # no error 1, error 0
    if not re.match("^[0-9]{4}$", inVal):
        print ("Error! Make sure you only use numbers from 0-9 in PIN")
        delay(3000)
        mainMenue( )
        inVal = 'Z'      
        ret=[0, inVal]
    else:
        ret =[1, inVal]  
#        print(ret) # debug only
        print("\nYOUR NEW PIN IS", inVal, "\n")   
        file.write('You have changed your PIN number\n\n')
        delay(3000)
        mainMenue()
    return ret
# selection main menue
def selMainMenue( inVal ):
    ret = 0; # no error 1, error 0
    if not re.match("^[1-5]*$", inVal):
        print ("Error! Make sure you only use numbers from 1-5 in selecion")
        ret=[0, inVal]
    else:
        ret =[1, inVal]
    return ret
# PIN validation
def pin( inVal, PIN ):
    ret = 0; # no error 1, error 0
#    while True:
    if not re.match("^[0-9]{4}$", inVal):
        print ("Error! Make sure you only use numbers from 0-9 in PIN")
        inVal = 'Z'    
        ret = 0
    else:
        if inVal == PIN :    
            #print("\nCorect PIN") # debug only
            print("\n")
            mainMenue()
            inVal = 'Z'  
            ret = 1
#                break             
        else:        
            print("\nInvalid PIN!")
            inVal = 'Z'  
            ret = 0
    return ret

def delay( msec ):
    cnt = 0
    while cnt < msec:
        cnt += 0.0001
    return 1  # no error 1, error 0

def mainMenue( ):
    print(" Main Menu")
    print("----------------------- \n")
    print(" 1. CHECK BALANCE")
    print(" 2. WITHDRAW CASH")
    print(" 3. DEPOSIT CASH")
    print(" 4. CHANGE PIN")
    print(" 5. EXIT ")
    return 1  # no error 1, error 0

def welcome( ):
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
    return 1  # no error 1, error 0