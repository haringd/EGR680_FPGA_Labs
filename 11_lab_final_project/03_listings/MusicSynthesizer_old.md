
## Music Sytheziser

Place description


```python
# Steup the PYNQ board
from pynq.overlays.base import BaseOverlay
base = BaseOverlay("base.bit")
from time import sleep
```


```python
%%microblaze base.PMODA
#include "xparameters.h"
#include "timer.h"
#include "circular_buffer.h"
#include "gpio.h"
#include "pmod_grove.h"

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

    char names[] = { 'c',  'd',  'e',  'f',  'g',  'a',  'b', 'C',  'D',  };
    int tones[] = { 1916, 1700, 1519, 1432, 1275, 1136, 1014, 956, 702 };
    int i;

    // play the tone corresponding to the note name
    for (i = 0; i < 8; i++) {
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
#include "gpio.h"
#include "timer.h"
#include "circular_buffer.h"
#include <pyprintf.h>
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
    //pyprintf(" --> ledbar init done\n");
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

```


```python
def music_synt():
    # initialize GPIO
    #
    buzzer_init()
    ledbar_init()
    # The number of notes
    length = 15
    notes_key = {'c': 99, 'd':100, 'e':101, 'f':102, 'g':103, 'a':97, 'b':98, 'C': 67, 'D': 68 , ' ': 32}

    # A-Team
    notes = [' ','C','C','g','C','f','g','c','e','g','C','g','D','C','b','a','g','f','g', '' ]
    beats = [  8,  3,  1,  2,  18,  2,  8, 10,  1,  1,  2,  2,  2, 18,  3,  1,  1,  3, 16, 8 ]
    if len(notes) != len(beats):
        return print('Error: Notes and beats must be of same length!')
    tempo = 124/1.7
    for index, beat in enumerate(beats):
        if notes[index] == '':
            time.sleep(beat * tempo/1000)
            set_level(10, 1, 1)
        else:
            #print('else: ',chr(notes[index]), int(beat * tempo))
            playNote(notes_key[notes[index]], int(beat * tempo)) 
            set_level(list(notes_key.keys()).index(notes[index])+1, 1, 1)
        # Delay between notes
        time.sleep(tempo / 300);

```


```python
if __name__ == '__main__':
    # synthesice music and visualize with LED Bar
    for i in range(3):
        music_synt()
```


```python

#ledbar_init()
#a = ledbar_read(void)
#set_bits(0b100000001 & 0xFFFF)
#set_level(5,1,1)

```


```python
#playTone(int(1700), int(600)) 
#print(chr(99))
#notes_key = {'a':97, 'b':98, 'c': 99, 'd':100, 'e':101, 'f':102, 'g':103, ' ': 32, 'C': 67, 'D': 68 }
#notes = ['c', 'd', 'e', 'f', 'g', 'a', 'b', 'C', 'D', ' ', ' ', ' ', ' ', ' ' ]
#for note in notes:
#    playNote(notes_key[note], int(600)) 
```
