# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 18:34:49 2018

@author: schwa
"""
import re
class Atm:
    AMOUNT_MIN = 0
    AMOUNT_MAX = 1000

    Pin  = "1234"
    Select = 0
    AccountValue = 0
    ReceiptFile = "atm_receipt.txt"
    
    def __init__(self, AccountValue, Pin):
        self.AccountValue = AccountValue
        self.Pin = Pin
        
    # Print Receipt
    def receipt(self, filename, file):
        file.write('THANK YOU FOR CHOOSING BANK ME!')
        file.close()
        file = open(filename, "r")
        for line in file:
            print(line, end='')
        file.close()
        return 1
    # Balance 
    def balance(self, account_value , file):
        print("\nYOUR BALANCE IS $%.2f \n \n\r" % account_value)
        file.write('Your checking account balance is----> $'\
                   +str(account_value)+'\n\n')
        self.delay(3000)
        self.mainMenue( )
        return 1
    # Withdraw money
    def withdraw(self,  inVal, AMOUNT_MIN, AMOUNT_MAX, account_value, file ):
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
                self.delay(3000)
                self.mainMenue( )
                ret=[1, account_value]
            else:
                ret=[0, inVal]
                print("\nWITHDRAW AMOUNT $%.2f TOO BIG OR TOO SMALL\n" % amount) 
        return ret
    # Deposit money
    def deposit( self, inVal, AMOUNT_MIN, AMOUNT_MAX, account_value, file ):
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
                self.delay(3000)
                self.mainMenue( )
                ret=[1, account_value]
            else:
                ret=[0, inVal]
                print("\nDEPOSIT AMOUNT $%.2f TOO BIG OR TOO SMALL\n" % amount) 
        return ret
    # set new pin
    def newPin( self, inVal, file ):
        ret = [0, 0]; # no error 1, error 0
        if not re.match("^[0-9]{4}$", inVal):
            print ("Error! Make sure you only use numbers from 0-9 in PIN")
            self.delay(3000)
            self.mainMenue( )
            inVal = 'Z'      
            ret=[0, inVal]
        else:
            ret =[1, inVal]  
    #        print(ret) # debug only
            print("\nYOUR NEW PIN IS", inVal, "\n")   
            file.write('You have changed your PIN number\n\n')
            self.delay(3000)
            self.mainMenue()
        return ret
    # selection main menue
    def selMainMenue(self, inVal ):
        ret = 0; # no error 1, error 0
        if not re.match("^[1-5]*$", inVal):
            print ("Error! Make sure you only use numbers from 1-5 in selecion")
            ret=[0, inVal]
        else:
            ret =[1, inVal]
        return ret
    # PIN validation
    def pin( self, inVal, PIN ):
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
                self.mainMenue()
                inVal = 'Z'  
                ret = 1
    #                break             
            else:        
                print("\nInvalid PIN!")
                inVal = 'Z'  
                ret = 0
        return ret
    
    def delay(self, msec ):
        cnt = 0
        while cnt < msec:
            cnt += 0.0001
        return 1  # no error 1, error 0
    
    def mainMenue(self):
        print(" Main Menu")
        print("----------------------- \n")
        print(" 1. CHECK BALANCE")
        print(" 2. WITHDRAW CASH")
        print(" 3. DEPOSIT CASH")
        print(" 4. CHANGE PIN")
        print(" 5. EXIT ")
        return 1  # no error 1, error 0
    
    def welcome(self):
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