# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
print("Hello World")

user = 0

print("Hello Human")

while user != "Hello Computer":

    user = input()
    
    if user == 'Hello Computer' :
    
        print("\nGoodby Human")
        
    else:
        
        print("\nIncorrect Greeting!")
        
while  user != "Goodby Computer":
    
    user = input()
    
    if user == 'Goodbye Computer':
        exit
    else:
        print("\nIncorrect Greeting!")