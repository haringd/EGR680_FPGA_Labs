
# coding: utf-8

# ## Music Sytheziser
# 
# Place description

# In[53]:


# Steup the PYNQ board
from pynq.overlays.base import BaseOverlay
base = BaseOverlay("base.bit")
from time import sleep
import ipywidgets as widgets
from IPython.display import display


# In[54]:


get_ipython().run_cell_magic('microblaze', 'base.PMODA', '#include <pyprintf.h>\n\n#include "xparameters.h"\n#include "timer.h"\n#include "circular_buffer.h"\n#include "gpio.h"\n#include "pmod_grove.h"\n\n// Mailbox commands\n#define CONFIG_IOP_SWITCH       0x1\n#define PLAY_TONE               0x3\n#define PLAY_DEMO               0x5\n\n// Speaker channel\n#define SPEAKER_CHANNEL 1\n\n// The driver instance for GPIO Devices\ngpio pb_speaker;\n\nvoid buzzer_init(){\n    pb_speaker = gpio_open(PMOD_G4_A);\n    gpio_set_direction(pb_speaker, GPIO_OUT);\n}\n\nvoid generateTone(int period_us) {\n    // turn-ON speaker\n    gpio_write(pb_speaker, 1);\n    delay_us(period_us>>1);\n    // turn-OFF speaker\n    gpio_write(pb_speaker, 0);\n    delay_us(period_us>>1);\n}\n\nvoid playTone(int tone, int duration) { \n    // tone is in us delay\n    long i;\n    pyprintf("playTone %d and %d \\n", tone, duration);\n    for (i = 0; i < duration * 1000L; i += tone * 2) {\n        generateTone(tone*2);\n    }\n}\n\nvoid playNote(char note, int duration) {\n\n    char names[] = { \'B\', \'c\',  \'d\',  \'e\',  \'f\',  \'g\',  \'a\',  \'b\', \'C\',  \'D\'  };\n    int tones[] = { 2010, 1916, 1700, 1519, 1432, 1275, 1136, 1014, 956,  702   };\n    int i;\n\n    // play the tone corresponding to the note name\n    for (i = 0; i < 10; i++) { // i < 8\n        if (names[i] == note) {\n          playTone(tones[i], duration);\n        }\n    }\n}\n\nvoid melody_demo(void) {\n    // The number of notes\n    int length = 15;\n    char notes[] = "CCDDCCDDCCDDCC ";\n    int beats[] = { 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 4 };\n    int tempo = 300;\n    int i;\n\n    for(i = 0; i < length; i++) {\n        if(notes[i] == \' \') {\n            delay_ms(beats[i] * tempo);\n        } else {\n            playNote(notes[i], beats[i] * tempo);\n        }\n        // Delay between notes\n        delay_ms(tempo / 2);\n    }\n}\n#include "gpio.h"\n#include "timer.h"\n#include "circular_buffer.h"\n#include <pyprintf.h>\n#include <pmod_grove.h>\n\n\n// Work on 8-bit mode\n#define CONFIG_IOP_SWITCH           0x1\n#define RESET                       0x3\n#define WRITE_LEDS                  0x5\n#define SET_BRIGHTNESS              0x7\n#define SET_LEVEL                   0x9\n#define READ_LEDS                   0xB\n\n/*\n * Green-to-Red direction contains slight transparency to one led distance.\n * i.e. A LED that is OFF will glow slightly if a LED  beside it is ON\n */\n#define GLB_CMDMODE                 0x00\n#define HIGH                        0xFF\n#define LOW                         0x01\n#define MED                         0xAA\n#define OFF                         0x00\n\n/*\n * gpio devices for clock and data\n */\ngpio gpio_clk;\ngpio gpio_data;\n\n/* \n * LED state, Brightness for each LED in\n * {Red, Orange, Green, Green, Green, Green, Green, Green, Green, Green}\n */\nchar ledbar_state[10] = {OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF};\nchar current_state[10] = {OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF};\n\n// Current Level\nint level_holder = 0;\n\n// Current direction: 0 => Red-to-Green, 1 => Green-to-Red\nint prev_inverse = 0;\n\nvoid ledbar_init(){  \n    gpio_clk = gpio_open(PMOD_G1_B);\n    gpio_data = gpio_open(PMOD_G1_A);\n    gpio_set_direction(gpio_clk, GPIO_OUT);\n    gpio_set_direction(gpio_data, GPIO_OUT);\n    //pyprintf(" --> ledbar init done\\n");\n}\n\nvoid send_data(u8 data){\n    int i;\n    u32 data_state, clkval, data_internal;\n\n    data_internal = data;\n\n    clkval = 0;\n    gpio_write(gpio_data, 0);\n    // First toggle the clock 8 times\n    for (i = 0; i < 8; ++i) {\n         clkval ^= 1;\n         gpio_write(gpio_clk, clkval);\n    }\n\n    // Working in 8-bit mode\n    for (i = 0; i < 8; i++){\n        /*\n         * Read each bit of the data to be sent LSB first\n         * Write it to the data_pin\n         */\n        data_state = (data_internal & 0x80) ? 0x00000001 : 0x00000000;\n        gpio_write(gpio_data, data_state);\n        clkval ^= 1;\n        gpio_write(gpio_clk, clkval);\n\n        // Shift Incoming data to fetch next bit\n        data_internal = data_internal << 1;\n    }\n}\n\nvoid latch_data(){\n    int i;\n    gpio_write(gpio_data, 0);\n    delay_ms(10);\n\n    // Generate four pulses on the data pin as per data sheet\n    for (i = 0; i < 4; i++){\n        gpio_write(gpio_data, 1);\n        gpio_write(gpio_data, 0);\n    }\n}\n\nu16 reverse_data(u16 c){\n    /*\n     * Function to reverse incoming data\n     * Allows LEDbar to be lit in reverse order\n     */\n    int shift;\n    u16 result = 0;\n\n    for (shift = 0; shift < 16; shift++){\n        if (c & (0x0001 << shift))\n            result |= (0x8000 >> shift);\n    }\n\n    // 10 LSBs are used as LED Control 6 MSBs are ignored\n    result = result >> 6;\n    return result;\n}\n\nvoid set_bits(u16 data){\n    int h,i;\n    int data_internal = data;\n\n    for(h=0; h<10; h++){\n        ledbar_state[h] = HIGH;\n    }\n\n    send_data(GLB_CMDMODE);\n\n    for (i = 0; i < 10; i++){\n        if ((data_internal & 0x0001) == 1) {\n            send_data(ledbar_state[i]);\n        } else {\n            send_data(0x00);\n            ledbar_state[i] = 0x00;\n        }\n        data_internal = data_internal >> 1;\n    }\n    // Two extra empty bits for padding the command to the correct length\n    send_data(0x00);\n    send_data(0x00);\n\n\n    latch_data();\n    // Store LEBbar state for reading purpose.\n    for(h=0; h<10; h++){\n        current_state[h] = ledbar_state[h];\n    }\n}\n\nvoid set_led_brightness(u16 data, char set_brightness[]){\n    int h,i;\n    int data_internal = data;\n\n    for(h=0; h<10; h++){\n        ledbar_state[h] = set_brightness[h];\n    }\n\n    send_data(GLB_CMDMODE);\n\n    for (i = 0; i < 10; i++){\n        if ((data_internal & 0x0001) == 1) {\n            send_data(ledbar_state[i]);\n        } else {\n            send_data(0x00);\n            ledbar_state[i] = 0x00;\n        }\n        data_internal = data_internal >> 1;\n    }\n    // Two extra empty bits for padding the command to the correct length\n    send_data(0x00);\n    send_data(0x00);\n\n    latch_data();\n    // Store LEBbar state for reading purpose.\n    for(h=0; h<10; h++){\n        current_state[h] = ledbar_state[h];\n    }\n}\n\nvoid set_level(int level, int intensity, int inverse){\n    int h,i;\n    int prev_inv ;\n\n    prev_inv = prev_inverse;\n\n    // Clear LED states from previous writes\n    if (inverse != prev_inv) {\n        for(h=0; h<10; h++){\n            ledbar_state[h] = OFF;\n        }\n    }\n\n    if (inverse == 0) { \n        // Execute when direction is Red-to-Green\n        if (level < level_holder) {\n            for(h=level_holder-1; h>level-1; h--){\n                ledbar_state[h] = OFF;\n            }\n        }\n        for(h=0; h<level; h++)\n        {\n            if (intensity == 1) {\n                ledbar_state[h] = LOW;\n            } else if (intensity == 2) {\n                ledbar_state[h] = MED;\n            } else if (intensity == 3) {\n                ledbar_state[h] = HIGH;\n            } else {\n                ledbar_state[h] = OFF;\n            }\n        }\n        for(h=level; h>10; h++){\n            ledbar_state[h] = OFF;\n        }\n    } else if(inverse == 1) { // Execute when direction is Red-to-Green\n        if (level < level_holder) {\n            for(h=0; h>=10-level; h++)\n            {\n                ledbar_state[h] = OFF;\n            }\n        }\n        for(h=9; h>=10-level; h--)\n        {\n            if (intensity == 1) {\n                ledbar_state[h] = LOW;\n            } else if (intensity == 2) {\n                ledbar_state[h] = MED;\n            } else if (intensity == 3) {\n                ledbar_state[h] = HIGH;\n            } else {\n                ledbar_state[h] = OFF;\n            }\n        }\n        if (level != 10) {\n            for(h=10-level-1; h>=0; h--)\n            {\n                ledbar_state[h] = OFF;\n            }\n        }\n    } else { // Execute when direction is Invalid Integer\n        for(h=0; h<10; h++){\n            ledbar_state[h] = OFF;\n        }\n    }\n\n    send_data(GLB_CMDMODE);\n\n    for (i = 0; i < 10; i++){\n        send_data(ledbar_state[i]);\n    }\n    // Two extra empty bits for padding the command to the correct length\n    send_data(0x00);\n    send_data(0x00);\n\n    // Two extra empty bits for padding the command to the correct length\n    latch_data();\n    // Store LEBbar Indication level for resetting level\n    level_holder= level;\n    // Store LEBbar direction for resetting direction\n    prev_inverse = inverse;\n    // Store LEBbar state for reading purpose.\n    for(h=0; h<10; h++){\n        current_state[h] = ledbar_state[h];\n    }\n}\n\nu16 ledbar_read(){\n    int h;\n    u16 bits;\n\n    bits = 0x0000;\n    for(h=0; h<10; h++){\n        if (current_state[h] != 0x00) {\n            bits |= 0x0001 << h;\n        }\n    }\n    bits = bits & 0x03FF;\n    return bits;\n}')


# In[55]:


def initGPIO():
    # initialize GPIO
    buzzer_init()
    ledbar_init()   
    
def show_of(notes_key):
    # A-Team
    notes = ['B','D',' ' ]
    beats = [  8,  3,  1]
    if len(notes) != len(beats):
        return print('Error: Notes and beats must be of same length!')
    tempo = 124/1.7
    for index, beat in enumerate(beats):
        if notes[index] == '':
            sleep(beat * tempo/1000)
            set_level(0, 3, 1)
        else:
            set_level(list(notes_key.keys()).index(notes[index]), 3, 1)
            playNote(notes_key[notes[index]], int(beat * tempo))           
        # Delay between notes
        sleep(tempo / 300);   
        
def play_note(note, beats ):
    global notes_key
    #notes_key = note_key
    # A-Team
    notes = [note ]
    beats = [ beats]
    if len(notes) != len(beats):
        return print('Error: Notes and beats must be of same length!')
    tempo = 124/1.7
    for index, beat in enumerate(beats):
        if notes[index] == '':
            #print('test pause', index, notes[index])
            sleep(beat * tempo/1000)
            set_level(0, 3, 1)
        else:
            #print('else: ',chr(notes[index]), int(beat * tempo))
            #print('test', index, notes[index])
            set_level(list(notes_key.keys()).index(notes[index]), 3, 1)
            playNote(notes_key[notes[index]], int(beat * tempo)) 
            
        # Delay between notes
        sleep(tempo / 300);    
    #set_level(0, 1, 1)
    
def music_synt(notes_key):
    # A-Team
    notes = [' ','C','C','g','C','f','g','c','e','g','C','g','D','C','b','a','g','f','g', ' ' ]
    beats = [  8,  3,  1,  2,  18,  2,  8, 10,  1,  1,  2,  2,  2, 18,  3,  1,  1,  3, 16, 1 ]
    if len(notes) != len(beats):
        return print('Error: Notes and beats must be of same length!')
    tempo = 124/1.7
    for index, beat in enumerate(beats):
        #print('music_synt', notes[index])
        if notes[index] == '':
            sleep(beat * tempo/1000)
            set_level(0, 3, 1)
        else:
            #print('else: ',chr(notes[index]), int(beat * tempo))
            set_level(list(notes_key.keys()).index(notes[index]), 3, 1)
            playNote(notes_key[notes[index]], int(beat * tempo))            
        # Delay between notes
        sleep(tempo / 300);
        
def on_button0_clicked(b):
    global note_key
    for i in range(3):
        music_synt(note_key)
def on_buttonB_clicked(b):
    play_note('B',4)        
def on_buttonc_clicked(b):
    play_note('c',4)
def on_buttond_clicked(b):
    play_note('d',4)
def on_buttone_clicked(b):
    play_note('e',4)
def on_buttonf_clicked(b):
    play_note('f',4)
def on_buttong_clicked(b):
    play_note('g',4)
def on_buttona_clicked(b):
    play_note('a',4)
def on_buttonb_clicked(b):
    play_note('b',4)
def on_buttonC_clicked(b):
    play_note('C',4)
def on_buttonD_clicked(b):
    play_note('D',4)

def gui():
    button0 = widgets.Button(description="A-Team", button_style='primary')
    buttonB = widgets.Button(description="B", button_style='primary')
    buttonc = widgets.Button(description="c", button_style='primary')
    buttond = widgets.Button(description="d", button_style='primary')
    buttone = widgets.Button(description="e", button_style='primary')
    buttonf = widgets.Button(description="f", button_style='primary')
    buttong = widgets.Button(description="g", button_style='primary')
    buttona = widgets.Button(description="a", button_style='primary')
    buttonb = widgets.Button(description="b", button_style='primary')
    buttonC = widgets.Button(description="C", button_style='primary')
    buttonD = widgets.Button(description="D", button_style='primary')

    button0.on_click(on_button0_clicked)
    buttonB.on_click(on_buttonB_clicked)
    buttonc.on_click(on_buttonc_clicked)
    buttond.on_click(on_buttond_clicked)
    buttone.on_click(on_buttone_clicked)
    buttonf.on_click(on_buttonf_clicked)
    buttong.on_click(on_buttong_clicked)
    buttona.on_click(on_buttona_clicked)
    buttonb.on_click(on_buttonb_clicked)
    buttonC.on_click(on_buttonC_clicked)
    buttonD.on_click(on_buttonD_clicked)
    
    display(button0)
    display(buttonB)
    display(buttonc)
    display(buttond)
    display(buttone)
    display(buttonf)
    display(buttong)
    display(buttona)
    display(buttonb)
    display(buttonC)
    display(buttonD)


# In[56]:


if __name__ == '__main__':
    # define vraiables
    notes_key = { ' ': 32, 'B':66, 'c': 99, 'd':100, 'e':101, 'f':102, 'g':103, 'a':97, 'b':98, 'C': 67, 'D': 68 }
    #init PMODA GPIOs for Groove G1 and G4
    initGPIO()
    show_of(notes_key)
    gui()
    # synthesice music and visualize with LED Bar
    #for i in range(3):
    #    music_synt(note_key)


# In[49]:



#ledbar_init()
#a = ledbar_read(void)
#set_bits(0b100000001 & 0xFFFF)
#set_level(5,1,1)


# In[50]:


#playTone(int(1700), int(600)) 
#print(chr(99))
#notes_key = {'a':97, 'b':98, 'c': 99, 'd':100, 'e':101, 'f':102, 'g':103, ' ': 32, 'C': 67, 'D': 68 }
#notes = ['c', 'd', 'e', 'f', 'g', 'a', 'b', 'C', 'D', ' ', ' ', ' ', ' ', ' ' ]
#for note in notes:
#    playNote(notes_key[note], int(600)) 


# In[51]:


#playNote(68, int(300)) 
#playNote(99, int(300)) 
#


# In[52]:


#melody_demo()

