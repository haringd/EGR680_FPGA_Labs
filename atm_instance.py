# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from time import asctime
import re
#from atm_class import welcome, pin, \
#selMainMenue, newPin, deposit, withdraw, balance, receipt, delay
from atm_class import Atm

atm = Atm(100,'2345') # instantiate class Atm to atm object

# Open a file
try:
    fo = open("07_lab_error_log.txt", "a")
    fr = open(atm.ReceiptFile, "w")
    fo.write(asctime()+ ' ATM program starts '+ '\n')
    fr.write('\n-------------------Bank Me-------------------\n')
    fr.write('---------------Transaction Receipt-----------\n')
    fr.write('*********************************************\n\n')
except IOError as e:
    print('File '+e.filename+' could not be opened or writen to!') 

# Star program
if atm.welcome(): # first method used from the atm object
    error = 0 
else:
    error = 1
    fo.write(asctime()+ ' welcome() error\n')
     
# PIN validation
while True:
    ret = 0
    if atm.pin( input("Please enter your PIN: "), atm.Pin): 
        error = 0 
        fo.write(asctime()+ ' User logged in \n')
        break   
    else:
        error = 1
        fo.write(asctime()+ ' User login error\n')

# Main menu
while  atm.Select != "5":
    ret = 0
    ret = atm.selMainMenue(input("PLEASE SELECT FROM THE ABOVE OTPIONS: ") )
#    print(ret) # debug only
    if (ret[0]):
        error = 0 
        atm.Select = ret[1] 
#        print(ret[1] ) # debug only
    else: # error
        error = 1
        atm.Select = 0
        fo.write(asctime()+ ' User slection error\n')
        print(ret[0])

    if atm.Select == '5': # exit
        while True:
            if not re.match("^[y]$", input('Do you wish to print the receipt, press y or n? ')):
                print("\nThank you for chosing BANK ME!")
                break
            else:
                atm.receipt(atm.ReceiptFile, fr)   
                break
        exit
    elif atm.Select == '4': # change PIN
        while True:
            ret = 0
            ret = atm.newPin(input("ENTER YOUR NEW PIN: "), fr)
#            print(ret) # debug only
            if (ret[0]):
                error = 0 
                atm.Pin = ret[1] 
        #        print(ret[1] ) # debug only
                break
            else: # error
                error = 1
                atm.Select = 0
                fo.write(asctime()+ ' User PIN error\n')
                break

    elif atm.Select == '3': # Deposit
        while True:
            ret = 0
            ret = atm.deposit(input("ENTER YOUR DEPOSIT AMOUNT IN $: ")\
                          , atm.AMOUNT_MIN, atm.AMOUNT_MAX, atm.AccountValue, fr)
#            print(ret) # debug only
            if (ret[0]):
                error = 0 
                atm.AccountValue = ret[1] 
        #        print(ret[1] ) # debug only
                break
            else: # error
                error = 1
                atm.Select = 0
                fo.write(asctime()+ ' Deposit error\n')
 
    elif atm.Select == '2': # Withdraw
        while True:
            ret = 0
            ret = atm.withdraw(input("ENTER YOUR WITHDRAW AMOUNT IN $: ")\
                           , atm.AMOUNT_MIN, atm.AMOUNT_MAX, atm.AccountValue, fr)
#            print(ret) # debug only
            if (ret[0]):
                error = 0 
                atm.AccountValue = ret[1] 
        #        print(ret[1] ) # debug only
                break
            else: # error
                error = 1
                atm.Select = 0
                fo.write(asctime()+ ' Withdraw error\n')            
         
    elif atm.Select == '1': # Balance
        atm.balance(atm.AccountValue, fr)
    else:
        print("\nIncorrect Selecion!")

fo.write(asctime()+ ' Program Closed\n')
fo.close() # to ensure file is closed
fr.close() # to ensure file is closed
atm.delay(3000)
