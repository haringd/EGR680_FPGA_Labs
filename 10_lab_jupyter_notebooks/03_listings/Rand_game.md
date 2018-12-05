
## Let's Make a Deal

Is a game where a player can choose between four different doors. The computer decides behinde which door win is placed.

The game is started by select Menubar -> Cell -> Run All

You can do the following to control the game:
    
    Button 0 pressed:        Door 1
    Button 1 pressed:        Door 2
    Button 2 pressed:        Door 3
    Button 3 pressed:        Door 4
    
    Switch 0 on:             Exit program
    Switch 1 on:             Exit program 
   
    *************************************************************
    * FSM State machine from C program                         **
    *************************************************************
                       000
    +---------------------+
    | Idle                |
    | Display user input  |<--------+
    |                     |         |
    +---------------------+         |
        |                           |
        |                           |
        |              001          |
    +---------------------+         |
    |                     |         |
    | Wait for button     |         |
    | coin_val on Pmod A  |         |
    +---------------------+         |
        |                           |
        |                           |
        |              002          |
    +---------------------+         |
    | user output         |         |
    | if (rnd == door)    |---------+
    | Display output      |
    +---------------------+
 


```python
import time
from pynq.overlays.base import BaseOverlay
import random
```

### Load overlay bitstream file generated by Vivado


```python
base = BaseOverlay("base.bit")
```

### Seed random number generator


```python
random.seed(time.localtime)
```

### Variables


```python
Delay1 = 0.3
Delay2 = 0.1
color = 0
rgbled_position = [4,5]
randomNo = random.randint(1,4)
winCnt = 0
lossCnt = 0
avgMedium = 0
```

### Define functions here
Function decision() provides the computaion of the win and loss with average and a consol ouput accordingly.
#### Colors RGB LED No 4 and 5
    off = 0
    blue = 1
    green = 2
    türkies = 3
    red = 4
    purple = 5
    yellow = 6
    white = 7



```python
def decision(rnd, door, win, loss, avg):
    #print("\r\nComputer chose %d" % rnd)
    # print("---------------------\r\n")
    if (rnd == door):
        color = 2
        print("WIN!")
        win = win + 1
    else:
        color = 4
        print("LOSS!")
        loss = loss + 1
        # print("---------------------\r\n")
    avg = win/ (win + loss)
    print("Win: %d - Loss: %d - Win Average: %f" % (win, loss, avg))
    
    for led in rgbled_position:
        base.rgbleds[led].write(color)
        base.rgbleds[led].write(color)
            
    return [win, loss, avg]
```

### Start progarm


```python
print("\r\n\r\n***********************************")
print("---Welcome to Let's Make a Deal!---")
print("***********************************")
# print("Select between 1 and 4 to seed the Random Number Generator: ")
print("Choose a button in a range of 1 and 4 to select a door: ")


for led in base.leds:
    led.on()    
while (base.switches.read() == 0):
#while (base.buttons[3].read()==0):
    if (base.buttons[0].read()==1):
    #    color = (color+1) % 8
        for led in base.leds:
            led.off()
        time.sleep(Delay2)
        
        for led in base.leds:
            led.toggle()
            time.sleep(Delay2)
            
     #  for led in rgbled_position:
     #      base.rgbleds[led].write(color)
     #      base.rgbleds[led].write(color)
     #   time.sleep(Delay1)
        
        ret = decision(random.randint(1,4), 1, winCnt, lossCnt, avgMedium)
        winCnt = ret[0]
        lossCnt = ret[1]
        avgMedium = ret[2]
        
        
    elif (base.buttons[1].read()==1):
        for led in base.leds:
            led.off()
        time.sleep(Delay2)
        for led in base.leds:
            led.toggle()
            time.sleep(Delay2)
        ret = decision(random.randint(1,4), 2, winCnt, lossCnt, avgMedium)
        winCnt = ret[0]
        lossCnt = ret[1]
        avgMedium = ret[2]
            
    elif (base.buttons[2].read()==1):
        for led in reversed(base.leds):
            led.off()
        time.sleep(Delay2)
        for led in reversed(base.leds):
            led.toggle()
            time.sleep(Delay2)        
        ret = decision(random.randint(1,4), 3, winCnt, lossCnt, avgMedium)
        winCnt = ret[0]
        lossCnt = ret[1]
        avgMedium = ret[2]
            
    elif (base.buttons[3].read()==1):
        for led in reversed(base.leds):
            led.off()
        time.sleep(Delay2)
        for led in reversed(base.leds):
            led.toggle()
            time.sleep(Delay2)  
        ret = decision(random.randint(1,4), 4, winCnt, lossCnt, avgMedium)
        winCnt = ret[0]
        lossCnt = ret[1]
        avgMedium = ret[2]
        
print('Live long and prosper!')
for led in base.leds:
    led.off()
for led in rgbled_position:
    base.rgbleds[led].off()
    
```

    
    
    ***********************************
    ---Welcome to Let's Make a Deal!---
    ***********************************
    Choose a button in a range of 1 and 4 to select a door: 
    LOSS!
    Win: 0 - Loss: 1 - Win Average: -0.000000
    LOSS!
    Win: 0 - Loss: 2 - Win Average: -0.000000
    WIN!
    Win: 1 - Loss: 2 - Win Average: 0.333333
    LOSS!
    Win: 1 - Loss: 3 - Win Average: 0.250000
    LOSS!
    Win: 1 - Loss: 4 - Win Average: 0.200000
    Live long and prosper!


### End Program