
## Music Sytheziser

The music synthesizer plays the A-Team theme with the Groove Buzzer and visualizes the played note on the Groove LED Bar. Tu generate the tone or turn on a LED Bar Level the microblaze is used to run C code on it which is used to run the drivers for both external components.

To run the program scroll down to the music_gamut cell no. 8 and execute in menulist Cell -> Run All Above

To just here and see the playable tones execute cell no. 8 with the music_gamut() function.


```
# Steup the PYNQ board
from pynq.overlays.base import BaseOverlay
base = BaseOverlay("base.bit")
import time
```


```
%%microblaze base.PMODA

/*
* Code imported from pmod_groove_ledbar.c file
*/
#include "xparameters.h"
#include "timer.h"
#include "circular_buffer.h"
#include "gpio.h"
#include "pmod_grove.h" // file added to have correct

// Mailbox commands
#define CONFIG_IOP_SWITCH       0x1
#define PLAY_TONE               0x3
#define PLAY_DEMO               0x5

// Speaker channel
#define SPEAKER_CHANNEL 1

// The driver instance for GPIO Devices
gpio pb_speaker;

void buzzer_init(){
    pb_speaker = gpio_open(PMOD_G4_A);
    gpio_set_direction(pb_speaker, GPIO_OUT);
}

void generateTone(int period_us) {
    // turn-ON speaker
    gpio_write(pb_speaker, 1);
    delay_us(period_us>>1);
    // turn-OFF speaker
    gpio_write(pb_speaker, 0);
    delay_us(period_us>>1);
}

void playTone(int tone, int duration) { 
    // tone is in us delay
    long i;
    for (i = 0; i < duration * 1000L; i += tone * 2) {
        generateTone(tone*2);
    }
}

void playNote(char note, int duration) {

    char names[] = { 'B', 'c',  'd',  'e',  'f',  'g',  'a',  'b', 'C',  'D'  };
    int tones[] = {  2010, 1916, 1700, 1519, 1432, 1275, 1136, 1014, 956, 836 };
    int i;

    // play the tone corresponding to the note name
    for (i = 0; i < 10; i++) { // haringd changed to 9
        if (names[i] == note) {
          playTone(tones[i], duration);
        }
    }
}

void melody_demo(void) {
    // The number of notes
    int length = 15;
    char notes[] = "ccggaagffeeddc ";
    int beats[] = { 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 4 };
    int tempo = 300;
    int i;

    for(i = 0; i < length; i++) {
        if(notes[i] == ' ') {
            delay_ms(beats[i] * tempo);
        } else {
            playNote(notes[i], beats[i] * tempo);
        }
        // Delay between notes
        delay_ms(tempo / 2);
    }
}

/*
* Code imported from pmod_groove_ledbar.c file
*/
#include "gpio.h"
#include "timer.h"
#include "circular_buffer.h"
#include <pmod_grove.h>


// Work on 8-bit mode
#define CONFIG_IOP_SWITCH           0x1
#define RESET                       0x3
#define WRITE_LEDS                  0x5
#define SET_BRIGHTNESS              0x7
#define SET_LEVEL                   0x9
#define READ_LEDS                   0xB

/*
 * Green-to-Red direction contains slight transparency to one led distance.
 * i.e. A LED that is OFF will glow slightly if a LED  beside it is ON
 */
#define GLB_CMDMODE                 0x00
#define HIGH                        0xFF
#define LOW                         0x01
#define MED                         0xAA
#define OFF                         0x00

/*
 * gpio devices for clock and data
 */
gpio gpio_clk;
gpio gpio_data;

/* 
 * LED state, Brightness for each LED in
 * {Red, Orange, Green, Green, Green, Green, Green, Green, Green, Green}
 */
char ledbar_state[10] = {OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF};
char current_state[10] = {OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF, OFF};

// Current Level
int level_holder = 0;

// Current direction: 0 => Red-to-Green, 1 => Green-to-Red
int prev_inverse = 0;

void ledbar_init(){  
    gpio_clk = gpio_open(PMOD_G1_B);
    gpio_data = gpio_open(PMOD_G1_A);
    gpio_set_direction(gpio_clk, GPIO_OUT);
    gpio_set_direction(gpio_data, GPIO_OUT);
}

void send_data(u8 data){
    int i;
    u32 data_state, clkval, data_internal;

    data_internal = data;

    clkval = 0;
    gpio_write(gpio_data, 0);
    // First toggle the clock 8 times
    for (i = 0; i < 8; ++i) {
         clkval ^= 1;
         gpio_write(gpio_clk, clkval);
    }

    // Working in 8-bit mode
    for (i = 0; i < 8; i++){
        /*
         * Read each bit of the data to be sent LSB first
         * Write it to the data_pin
         */
        data_state = (data_internal & 0x80) ? 0x00000001 : 0x00000000;
        gpio_write(gpio_data, data_state);
        clkval ^= 1;
        gpio_write(gpio_clk, clkval);

        // Shift Incoming data to fetch next bit
        data_internal = data_internal << 1;
    }
}

void latch_data(){
    int i;
    gpio_write(gpio_data, 0);
    delay_ms(10);

    // Generate four pulses on the data pin as per data sheet
    for (i = 0; i < 4; i++){
        gpio_write(gpio_data, 1);
        gpio_write(gpio_data, 0);
    }
}

u16 reverse_data(u16 c){
    /*
     * Function to reverse incoming data
     * Allows LEDbar to be lit in reverse order
     */
    int shift;
    u16 result = 0;

    for (shift = 0; shift < 16; shift++){
        if (c & (0x0001 << shift))
            result |= (0x8000 >> shift);
    }

    // 10 LSBs are used as LED Control 6 MSBs are ignored
    result = result >> 6;
    return result;
}

void set_bits(u16 data){
    int h,i;
    int data_internal = data;

    for(h=0; h<10; h++){
        ledbar_state[h] = HIGH;
    }

    send_data(GLB_CMDMODE);

    for (i = 0; i < 10; i++){
        if ((data_internal & 0x0001) == 1) {
            send_data(ledbar_state[i]);
        } else {
            send_data(0x00);
            ledbar_state[i] = 0x00;
        }
        data_internal = data_internal >> 1;
    }
    // Two extra empty bits for padding the command to the correct length
    send_data(0x00);
    send_data(0x00);


    latch_data();
    // Store LEBbar state for reading purpose.
    for(h=0; h<10; h++){
        current_state[h] = ledbar_state[h];
    }
}

void set_led_brightness(u16 data, char set_brightness[]){
    int h,i;
    int data_internal = data;

    for(h=0; h<10; h++){
        ledbar_state[h] = set_brightness[h];
    }

    send_data(GLB_CMDMODE);

    for (i = 0; i < 10; i++){
        if ((data_internal & 0x0001) == 1) {
            send_data(ledbar_state[i]);
        } else {
            send_data(0x00);
            ledbar_state[i] = 0x00;
        }
        data_internal = data_internal >> 1;
    }
    // Two extra empty bits for padding the command to the correct length
    send_data(0x00);
    send_data(0x00);

    latch_data();
    // Store LEBbar state for reading purpose.
    for(h=0; h<10; h++){
        current_state[h] = ledbar_state[h];
    }
}

void set_level(int level, int intensity, int inverse){
    int h,i;
    int prev_inv ;

    prev_inv = prev_inverse;

    // Clear LED states from previous writes
    if (inverse != prev_inv) {
        for(h=0; h<10; h++){
            ledbar_state[h] = OFF;
        }
    }

    if (inverse == 0) { 
        // Execute when direction is Red-to-Green
        if (level < level_holder) {
            for(h=level_holder-1; h>level-1; h--){
                ledbar_state[h] = OFF;
            }
        }
        for(h=0; h<level; h++)
        {
            if (intensity == 1) {
                ledbar_state[h] = LOW;
            } else if (intensity == 2) {
                ledbar_state[h] = MED;
            } else if (intensity == 3) {
                ledbar_state[h] = HIGH;
            } else {
                ledbar_state[h] = OFF;
            }
        }
        for(h=level; h>10; h++){
            ledbar_state[h] = OFF;
        }
    } else if(inverse == 1) { // Execute when direction is Red-to-Green
        if (level < level_holder) {
            for(h=0; h>=10-level; h++)
            {
                ledbar_state[h] = OFF;
            }
        }
        for(h=9; h>=10-level; h--)
        {
            if (intensity == 1) {
                ledbar_state[h] = LOW;
            } else if (intensity == 2) {
                ledbar_state[h] = MED;
            } else if (intensity == 3) {
                ledbar_state[h] = HIGH;
            } else {
                ledbar_state[h] = OFF;
            }
        }
        if (level != 10) {
            for(h=10-level-1; h>=0; h--)
            {
                ledbar_state[h] = OFF;
            }
        }
    } else { // Execute when direction is Invalid Integer
        for(h=0; h<10; h++){
            ledbar_state[h] = OFF;
        }
    }

    send_data(GLB_CMDMODE);

    for (i = 0; i < 10; i++){
        send_data(ledbar_state[i]);
    }
    // Two extra empty bits for padding the command to the correct length
    send_data(0x00);
    send_data(0x00);

    // Two extra empty bits for padding the command to the correct length
    latch_data();
    // Store LEBbar Indication level for resetting level
    level_holder= level;
    // Store LEBbar direction for resetting direction
    prev_inverse = inverse;
    // Store LEBbar state for reading purpose.
    for(h=0; h<10; h++){
        current_state[h] = ledbar_state[h];
    }
}

u16 ledbar_read(){
    int h;
    u16 bits;

    bits = 0x0000;
    for(h=0; h<10; h++){
        if (current_state[h] != 0x00) {
            bits |= 0x0001 << h;
        }
    }
    bits = bits & 0x03FF;
    return bits;
}

void my_func(u16 led){
    set_bits(led);
}
```

NOTICE: The advantage of seberating the code at this spot is that aftre the python libarays are load and the microblaze is flashed the python code followed can be executed and debug indepandently. This saves a lot of time and in case there is an buzzer involved it saves your ears as well.


```
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
```


```
if __name__ == '__main__':
    # synthesice music and visualize with LED Bar
    tempo = 124/1.7
    notes_key = { ' ': 32, 'B':66, 'c': 99, 'd':100, 'e':101, 'f':102, 'g':103, 'a':97, 'b':98, 'C': 67, 'D': 68 }
    
    # play A-Team theme
    A_Team(tempo, notes_key)
    
```


```
# play the gamut of the buzzer
music_gamut(notes_key)
```


```
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
```


```

my_func
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-15-990f10c9b52d> in <module>()
          1 set_level
    ----> 2 my_func
    

    NameError: name 'my_func' is not defined



```
set_bits
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-16-b52bb9aab296> in <module>()
    ----> 1 set_bits
    

    NameError: name 'set_bits' is not defined



```
set_level
```




    <pynq.lib.pynqmicroblaze.magic._FunctionWrapper at 0x2f099530>


