# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from time import asctime
import re
from atm_func_partII import welcome, pin, \
selMainMenue, newPin, deposit, withdraw, balance, receipt, delay

AMOUNT_MIN = 0
AMOUNT_MAX = 1000

gPin  = "1234"
gSelect = 0
gAccountValue = 0
gReceiptFile = "atm_receipt.txt"

# Open a file
try:
    fo = open("07_lab_error_log.txt", "a")
    fr = open(gReceiptFile, "w")
    fo.write(asctime()+ 'ATM program starts '+ '\n')
    fr.write('\n-------------------Bank Me-------------------\n')
    fr.write('---------------Transaction Receipt-----------\n')
    fr.write('*********************************************\n\n')
except IOError as e:
    print('File '+e.filename+' could not be opened!') 

# Star program
if welcome(): 
    error = 0 
else:
    error = 1
    fo.write(asctime()+ ' welcome() error\n')
     
# PIN validation
while True:
    ret = 0
    if pin( input("Please enter your PIN: "), gPin): 
        error = 0 
        fo.write(asctime()+ ' User logged in \n')
        break   
    else:
        error = 1
        fo.write(asctime()+ ' User login error\n')

# Main menu
while  gSelect != "5":
    ret = 0
    ret = selMainMenue(input("PLEASE SELECT FROM THE ABOVE OTPIONS: ") )
#    print(ret) # debug only
    if (ret[0]):
        error = 0 
        gSelect = ret[1] 
#        print(ret[1] ) # debug only
    else: # error
        error = 1
        gSelect = 0
        fo.write(asctime()+ ' User slection error\n')
        print(ret[0])

    if gSelect == '5': # exit
        while True:
            if not re.match("^[y]$", input('Do you wish to print the receipt, press y or n? ')):
                print("\nThank you for chosing BANK ME!")
                break
            else:
                receipt(gReceiptFile, fr)   
                break
        exit
    elif gSelect == '4': # change PIN
        while True:
            ret = 0
            ret = newPin(input("ENTER YOUR NEW PIN: "), fr)
#            print(ret) # debug only
            if (ret[0]):
                error = 0 
                gPin = ret[1] 
        #        print(ret[1] ) # debug only
                break
            else: # error
                error = 1
                gSelect = 0
                fo.write(asctime()+ ' User PIN error\n')
                break

    elif gSelect == '3': # Deposit
        while True:
            ret = 0
            ret = deposit(input("ENTER YOUR DEPOSIT AMOUNT IN $: ")\
                          , AMOUNT_MIN, AMOUNT_MAX, gAccountValue, fr)
#            print(ret) # debug only
            if (ret[0]):
                error = 0 
                gAccountValue = ret[1] 
        #        print(ret[1] ) # debug only
                break
            else: # error
                error = 1
                gSelect = 0
                fo.write(asctime()+ ' Deposit error\n')
 
    elif gSelect == '2': # Withdraw
        while True:
            ret = 0
            ret = withdraw(input("ENTER YOUR WITHDRAW AMOUNT IN $: ")\
                           , AMOUNT_MIN, AMOUNT_MAX, gAccountValue, fr)
#            print(ret) # debug only
            if (ret[0]):
                error = 0 
                gAccountValue = ret[1] 
        #        print(ret[1] ) # debug only
                break
            else: # error
                error = 1
                gSelect = 0
                fo.write(asctime()+ ' Withdraw error\n')            
         
    elif gSelect == '1': # Balance
        balance(gAccountValue, fr)
    else:
        print("\nIncorrect Selecion!")

fo.write(asctime()+ ' Program Closed\n')
fo.close() # to ensure file is closed
fr.close() # to ensure file is closed
delay(3000)
