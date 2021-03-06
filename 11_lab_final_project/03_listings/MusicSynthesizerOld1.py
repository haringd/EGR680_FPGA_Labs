
# coding: utf-8

# ## Music Sytheziser
# 
# The music synthesizer plays the A-Team theme with the Groove Buzzer and visualizes the played note on the Groove LED Bar. Tu generate the tone or turn on a LED Bar Level the microblaze is used to run C code on it which is used to run the drivers for both external components.
# 
# To run the program scroll down to the music_gamut cell no. 8 and execute in menulist Cell -> Run All Above
# 
# To just here and see the playable tones execute cell no. 8 with the music_gamut() function.

# In[11]:


# Steup the PYNQ board
from pynq.overlays.base import BaseOverlay
base = BaseOverlay("base.bit")
import time


# In[12]:


get_ipython().run_cell_magic('microblaze', 'base.PMODA', '\n/*\n* Code imported from pmod_groove_ledbar.c file\n*/\n#include "xparameters.h"\n#include "timer.h"\n#include "circular_buffer.h"\n#include "gpio.h"\n#include "pmod_grove.h" // file added to have correct\n\n// Mailbox commands\n#define CONFIG_IOP_SWITCH       0x1\n#define PLAY_TONE               0x3\n#define PLAY_DEMO               0x5\n\n// Speaker channel\n#define SPEAKER_CHANNEL 1\n\n// The driver instance for GPIO Devices\ngpio pb_speaker;\n\nvoid buzzer_init(){\n    pb_speaker = gpio_open(PMOD_G4_A);\n    gpio_set_direction(pb_speaker, GPIO_OUT);\n}\n\nvoid generateTone(int period_us) {\n    // turn-ON speaker\n    gpio_write(pb_speaker, 1);\n    delay_us(period_us>>1);\n    // turn-OFF speaker\n    gpio_write(pb_speaker, 0);\n    delay_us(period_us>>1);\n}\n\nvoid playTone(int tone, int duration) { \n    // tone is in us delay\n    long i;\n    for (i = 0; i < duration * 1000L; i += tone * 2) {\n        generateTone(tone*2);\n    }\n}\n\nvoid playNote(char note, int duration) {\n\n    char names[] = { \'B\', \'c\',  \'d\',  \'e\',  \'f\',  \'g\',  \'a\',  \'b\', \'C\',  \'D\'  };\n    int tones[] = {  2010, 1916, 1700, 1519, 1432, 1275, 1136, 1014, 956, 836 };\n    int i;\n\n    // play the tone corresponding to the note name\n    for (i = 0; i < 10; i++) { // haringd changed to 9\n        if (names[i] == note) {\n          playTone(tones[i], duration);\n        }\n    }\n}\n\nvoid melody_demo(void) {\n    // The number of notes\n    int length = 15;\n    char notes[] = "ccggaagffeeddc ";\n    int beats[] = { 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 4 };\n    int tempo = 300;\n    int i;\n\n    for(i = 0; i < length; i++) {\n        if(notes[i] == \' \') {\n            delay_ms(beats[i] * tempo);\n        } else {\n            playNote(notes[i], beats[i] * tempo);\n        }\n        // Delay between notes\n        delay_ms(tempo / 2);\n    }\n}\n\n/*\n* Code imported from pmod_groove_ledbar.c file\n*/\n#include "gpio.h"\n#include "timer.h"\n#include "circular_buffer.h"\n#include <pmod_grove.h>\n\n\n// Work on 8-bit mode\n#define CONFIG_IOP_SWITCH           0x1\n#define RESET                       0x3\n#define WRITE_LEDS                  0x5\n#define SET_BRIGHTNESS              0x7\n#define SET_LEVEL                   0x9\n#define READ_LEDS                   0xB\n\n/*\n * Green-to-Red direction contains slight transparency to one led distance.\n * i.e. A LED that is OFF will glow slightly if a LED  beside it is ON\n */\n#define GLB_CMDMODE                 0x00\n#define HIGH                        0xFF\n#define LOW                         0x01\n#define MED                         0xAA\n#define OFF                         0x00\n\n/*\n * gpio devices for clock and data\n */\ngpio gpio_clk;\ngpio gpio_data;\n\n/* \n * LED state, Brightness for each LED in\n * {Red, Orange, Green, Green, Green, Green, Green, Green, Green, Green}\n */\nchar ledbar_state[10] = {OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF};\nchar current_state[10] = {OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF};\n\n// Current Level\nint level_holder = 0;\n\n// Current direction: 0 => Red-to-Green, 1 => Green-to-Red\nint prev_inverse = 0;\n\nvoid ledbar_init(){  \n    gpio_clk = gpio_open(PMOD_G1_B);\n    gpio_data = gpio_open(PMOD_G1_A);\n    gpio_set_direction(gpio_clk, GPIO_OUT);\n    gpio_set_direction(gpio_data, GPIO_OUT);\n}\n\nvoid send_data(u8 data){\n    int i;\n    u32 data_state, clkval, data_internal;\n\n    data_internal = data;\n\n    clkval = 0;\n    gpio_write(gpio_data, 0);\n    // First toggle the clock 8 times\n    for (i = 0; i < 8; ++i) {\n         clkval ^= 1;\n         gpio_write(gpio_clk, clkval);\n    }\n\n    // Working in 8-bit mode\n    for (i = 0; i < 8; i++){\n        /*\n         * Read each bit of the data to be sent LSB first\n         * Write it to the data_pin\n         */\n        data_state = (data_internal & 0x80) ? 0x00000001 : 0x00000000;\n        gpio_write(gpio_data, data_state);\n        clkval ^= 1;\n        gpio_write(gpio_clk, clkval);\n\n        // Shift Incoming data to fetch next bit\n        data_internal = data_internal << 1;\n    }\n}\n\nvoid latch_data(){\n    int i;\n    gpio_write(gpio_data, 0);\n    delay_ms(10);\n\n    // Generate four pulses on the data pin as per data sheet\n    for (i = 0; i < 4; i++){\n        gpio_write(gpio_data, 1);\n        gpio_write(gpio_data, 0);\n    }\n}\n\nu16 reverse_data(u16 c){\n    /*\n     * Function to reverse incoming data\n     * Allows LEDbar to be lit in reverse order\n     */\n    int shift;\n    u16 result = 0;\n\n    for (shift = 0; shift < 16; shift++){\n        if (c & (0x0001 << shift))\n            result |= (0x8000 >> shift);\n    }\n\n    // 10 LSBs are used as LED Control 6 MSBs are ignored\n    result = result >> 6;\n    return result;\n}\n\nvoid set_bits(u16 data){\n    int h,i;\n    int data_internal = data;\n\n    for(h=0; h<10; h++){\n        ledbar_state[h] = HIGH;\n    }\n\n    send_data(GLB_CMDMODE);\n\n    for (i = 0; i < 10; i++){\n        if ((data_internal & 0x0001) == 1) {\n            send_data(ledbar_state[i]);\n        } else {\n            send_data(0x00);\n            ledbar_state[i] = 0x00;\n        }\n        data_internal = data_internal >> 1;\n    }\n    // Two extra empty bits for padding the command to the correct length\n    send_data(0x00);\n    send_data(0x00);\n\n\n    latch_data();\n    // Store LEBbar state for reading purpose.\n    for(h=0; h<10; h++){\n        current_state[h] = ledbar_state[h];\n    }\n}\n\nvoid set_led_brightness(u16 data, char set_brightness[]){\n    int h,i;\n    int data_internal = data;\n\n    for(h=0; h<10; h++){\n        ledbar_state[h] = set_brightness[h];\n    }\n\n    send_data(GLB_CMDMODE);\n\n    for (i = 0; i < 10; i++){\n        if ((data_internal & 0x0001) == 1) {\n            send_data(ledbar_state[i]);\n        } else {\n            send_data(0x00);\n            ledbar_state[i] = 0x00;\n        }\n        data_internal = data_internal >> 1;\n    }\n    // Two extra empty bits for padding the command to the correct length\n    send_data(0x00);\n    send_data(0x00);\n\n    latch_data();\n    // Store LEBbar state for reading purpose.\n    for(h=0; h<10; h++){\n        current_state[h] = ledbar_state[h];\n    }\n}\n\nvoid set_level(int level, int intensity, int inverse){\n    int h,i;\n    int prev_inv ;\n\n    prev_inv = prev_inverse;\n\n    // Clear LED states from previous writes\n    if (inverse != prev_inv) {\n        for(h=0; h<10; h++){\n            ledbar_state[h] = OFF;\n        }\n    }\n\n    if (inverse == 0) { \n        // Execute when direction is Red-to-Green\n        if (level < level_holder) {\n            for(h=level_holder-1; h>level-1; h--){\n                ledbar_state[h] = OFF;\n            }\n        }\n        for(h=0; h<level; h++)\n        {\n            if (intensity == 1) {\n                ledbar_state[h] = LOW;\n            } else if (intensity == 2) {\n                ledbar_state[h] = MED;\n            } else if (intensity == 3) {\n                ledbar_state[h] = HIGH;\n            } else {\n                ledbar_state[h] = OFF;\n            }\n        }\n        for(h=level; h>10; h++){\n            ledbar_state[h] = OFF;\n        }\n    } else if(inverse == 1) { // Execute when direction is Red-to-Green\n        if (level < level_holder) {\n            for(h=0; h>=10-level; h++)\n            {\n                ledbar_state[h] = OFF;\n            }\n        }\n        for(h=9; h>=10-level; h--)\n        {\n            if (intensity == 1) {\n                ledbar_state[h] = LOW;\n            } else if (intensity == 2) {\n                ledbar_state[h] = MED;\n            } else if (intensity == 3) {\n                ledbar_state[h] = HIGH;\n            } else {\n                ledbar_state[h] = OFF;\n            }\n        }\n        if (level != 10) {\n            for(h=10-level-1; h>=0; h--)\n            {\n                ledbar_state[h] = OFF;\n            }\n        }\n    } else { // Execute when direction is Invalid Integer\n        for(h=0; h<10; h++){\n            ledbar_state[h] = OFF;\n        }\n    }\n\n    send_data(GLB_CMDMODE);\n\n    for (i = 0; i < 10; i++){\n        send_data(ledbar_state[i]);\n    }\n    // Two extra empty bits for padding the command to the correct length\n    send_data(0x00);\n    send_data(0x00);\n\n    // Two extra empty bits for padding the command to the correct length\n    latch_data();\n    // Store LEBbar Indication level for resetting level\n    level_holder= level;\n    // Store LEBbar direction for resetting direction\n    prev_inverse = inverse;\n    // Store LEBbar state for reading purpose.\n    for(h=0; h<10; h++){\n        current_state[h] = ledbar_state[h];\n    }\n}\n\nu16 ledbar_read(){\n    int h;\n    u16 bits;\n\n    bits = 0x0000;\n    for(h=0; h<10; h++){\n        if (current_state[h] != 0x00) {\n            bits |= 0x0001 << h;\n        }\n    }\n    bits = bits & 0x03FF;\n    return bits;\n}\n\nvoid my_func(u16 led){\n    set_bits(led);\n}')


# NOTICE: The advantage of seberating the code at this spot is that aftre the python libarays are load and the microblaze is flashed the python code followed can be executed and debug indepandently. This saves a lot of time and in case there is an buzzer involved it saves your ears as well.

# In[18]:


def play_melody(notes, beats, notes_key, tempo):
    if len(notes) != len(beats):
        return print('Error: Notes and beats must be of same length!')
    #tempo = 124/1.7
    for index, beat in enumerate(beats):
        if notes[index] == '':
            time.sleep(beat * tempo/1000)
            set_level(0, 3, 1)
        else:
            set_level(list(notes_key.keys()).index(notes[index]), 3, 1) 
            #my_func( list(notes_key.keys()).index(notes[index]) )
            playNote(notes_key[notes[index]], int(beat * tempo))  
            #print( list(notes_key.keys()).index(notes[index]), notes_key[notes[index]],  notes[index])
        # Delay between notes
        time.sleep(tempo / 300);
        
def music_synt(tempo, notes_key):
    # initialize GPIO, just to enusers GPIO init
    buzzer_init()
    ledbar_init()

    # A-Team part 1, main
    notes = [' ','C','C','g','C','f','g','c','e','g','C','g','D','C','b','a','g','f','g', ' ']
    beats = [  8,  3,  1,  2, 18,  2,  8, 10,  1,  1,  2,  2,  2, 18,  3,  1,  1,  3, 16,  1 ]
    play_melody(notes, beats, notes_key, tempo)

def music_synt2(tempo, notes_key):
    # A-Team part 2
    notes = ['C','C','g','C','e','f','d','g','c','e','f','a','b','b','a',' ','f','c','a' ]
    beats = [ 3 , 1 , 2 , 18, 2 , 2 , 2 , 2 , 16, 3 , 1 , 2 , 50, 2 , 2 , 2 , 2 , 8 , 8  ]
    play_melody(notes, beats, notes_key, tempo)
    
def music_synt3(tempo, notes_key):
    # A-Team part 3
    notes = [' ','d','f','g','C','g','f',' ','g','f','f','e','c','B','c',' ' ]
    beats = [ 8 , 3 , 1 , 2 , 18, 2 , 2 , 2 , 8 , 8 , 2 , 2,  2,  2,  16, 2 ]
    play_melody(notes, beats, notes_key, tempo)

def music_synt4(tempo, notes_key):
    # A-Team part 4
    notes = ['e','e','d','e',' ','d',' ','e',' ','d',' ','d','a','g' ]
    beats = [ 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2,  8,  8]
    play_melody(notes, beats, notes_key, tempo)

def music_synt5(tempo, notes_key):
    # A-Team part 5
    notes = ['e','e','d','e',' ','d',' ','c',' ','c',' ','c','d', ' ' ]
    beats = [ 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2,  16,  1]  
    play_melody(notes, beats, notes_key, tempo)

def A_Team(tempo, notes_key):
    for i in range(1):
        music_synt(tempo, notes_key)
        music_synt2(tempo, notes_key)
        music_synt3(tempo, notes_key)
        music_synt4(tempo, notes_key)
        music_synt5(tempo, notes_key)
    music_synt(tempo, notes_key)
    
def music_gamut(notes_key):
    # initialize GPIO, to be able to run it independently
    buzzer_init()
    ledbar_init()

    # A-Team
    notes = [' ', 'B', 'c', 'd', 'e', 'f', 'g', 'a', 'b', 'C', 'D', ' ']
    beats = [  4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4]
    if len(notes) != len(beats):
        return print('Error: Notes and beats must be of same length!')
    tempo = 124/0.5
    for index, beat in enumerate(beats):
        if notes[index] == '':
            time.sleep(beat * tempo/1000)
            set_level(0, 3, 1)
        else:
            set_level(list(notes_key.keys()).index(notes[index]), 3, 1) 
            playNote(notes_key[notes[index]], int(beat * tempo))            
            print( 'led level, tune, ascii dec value:',
                  list(notes_key.keys()).index(notes[index]),  
                  notes[index], 
                  notes_key[notes[index]] 
                )
        # Delay between notes
        time.sleep(tempo / 200);


# In[19]:


if __name__ == '__main__':
    # synthesice music and visualize with LED Bar
    tempo = 124/1.7
    notes_key = { ' ': 32, 'B':66, 'c': 99, 'd':100, 'e':101, 'f':102, 'g':103, 'a':97, 'b':98, 'C': 67, 'D': 68 }
    
    # play A-Team theme
    A_Team(tempo, notes_key)
    


# In[ ]:


# play the gamut of the buzzer
music_gamut(notes_key)


# In[ ]:


# test celll

#playTone(int(1700), int(600)) 
#print(chr(99))
#notes_key = {'a':97, 'b':98, 'c': 99, 'd':100, 'e':101, 'f':102, 'g':103, ' ': 32, 'C': 67, 'D': 68 }
#notes = ['c', 'd', 'e', 'f', 'g', 'a', 'b', 'C', 'D', ' ', ' ', ' ', ' ', ' ' ]
#for note in notes:
#    playNote(notes_key[note], int(600)) 
#playNote(notes_key['b'], int(600)) 
#playNote(notes_key['C'], int(600)) 
#playNote(notes_key['D'], int(600)) 


# In[15]:



my_func


# In[16]:


set_bits


# In[17]:


set_level

