
## Music Sytheziser

The music synthesizer plays the A-Team theme with the Groove Buzzer and visualizes the played note on the Groove LED Bar. Tu generate the tone or turn on a LED Bar Level the microblaze is used to run C code on it which is used to run the drivers for both external components.

To run the program scroll down to the music_gamut cell no. 8 and execute in menulist Cell -> Run All Above

To just here and see the playable tones execute cell no. 8 with the music_gamut() function.


```python
# Steup the PYNQ board
from pynq.overlays.base import BaseOverlay
base = BaseOverlay("base.bit")
import time
import ipywidgets as widgets
from IPython.display import display
```

## MicroBlaze Softcore for PMODA
The following cell compiles, flashes, and executes C code on the MicroBlaze softcore. Each perihareal outlet as they are PMODA, PMODB, and ARDUINO has there own MicroBlaze.

The following cell uses the PMODA MicroBlaze to execute driver code which allows the pogrammer to invoke C functions directly in python code. This works of because of cell magic where the microblaze cell wrappes the C funtion to make it accessable for python.

Due to the fact that there is only one microblace per outlet a notebook can only have one cell per each microblaze. if there more the first code will be compiled, flashed, and executed. As the the second microplace cell with the same outlet is run the C code of that cell is compiled, flashed, and executed on the microblaze. 


```python
%%microblaze base.PMODA

/*
* Code imported from pmod_groove_ledbar.c file
*/
#include "xparameters.h"
#include "timer.h"
#include "circular_buffer.h"
#include "gpio.h"
#include "pmod_grove.h" // file added to have correct

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
 * gpio devices ledbar for clock and data
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

void playNote(char note, int duration) {

    char names[] = { 'B', 'c',  'd',  'e',  'f',  'g',  'a',  'b', 'C',  'D'  };
    int tones[] = {  2010, 1916, 1700, 1519, 1432, 1275, 1136, 1014, 956, 836 };
    int i;

    // play the tone corresponding to the note name
    for (i = 0; i < 10; i++) { // haringd changed to 9
        if (names[i] == note) {
          set_bits(reverse_data(0b00000000001 << i));
          playTone(tones[i], duration);
            
        }
    }
}

void melody_demo(void) {
    // The number of notes to play
    int length = 20;
    
    /* Melody demo */
//  char notes[] = "ccggaagffeeddc ";
//  int beats[] = { 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 4 };
    
    /*  A-Team theme */
    char notes[] = {' ','C','C','g','C','f','g','c','e','g','C','g','D','C','b','a','g','f','g', ' ',\
                    'C','C','g','C','e','f','d','g','c','e','f','a','b','b','a',' ','f','c','a',\
                    ' ','d','f','g','C','g','f',' ','g','f','f','e','c','B','c',' ',\
                    'e','e','d','e',' ','d',' ','e',' ','d',' ','d','a','g',
                    'e','e','d','e',' ','d',' ','c',' ','c',' ','c','d', ' '};
    int beats[] = {  8,  3,  1,  2, 18,  2,  8, 10,  1,  1,  2,  2,  2, 18,  3,  1,  1,  3, 16,  1, \ 
                     3 , 1 , 2 , 18, 2 , 2 , 2 , 2 , 16, 3 , 1 , 2 , 50, 2 , 2 , 2 , 2 , 8 , 8, \
                     8 , 3 , 1 , 2 , 18, 2 , 2 , 2 , 8 , 8 , 2 , 2,  2,  2,  16, 2, \
                     2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2,  8,  8, \
                     2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2 , 2,  16,  1 };

    /* gamut */
//  char notes [] = {' ', 'B', 'c', 'd', 'e', 'f', 'g', 'a', 'b', 'C', 'D', ' '};
//  int beats [] = {  4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4};
    
    length = sizeof(notes);
    int tempo = 73;
    int i;

    for(i = 0; i < length; i++) {
        if(notes[i] == ' ') {
            set_bits((0b00000000000));
            delay_ms(beats[i] * tempo);
        } else {
            playNote(notes[i], beats[i] * tempo);
        }
        // Delay between notes
        delay_ms(tempo / 2);
    }
}
void c_music_play(){
    buzzer_init();
    ledbar_init();
    set_bits(0b1111100000);
    delay_ms(1000);
    melody_demo();
}


```

## C Implemented Play
The function c_music_play() calls the C implemented melody with note visualitation on the led bar.


```python
c_music_play()
```

## Python Implemented Play
The cells below using C functions written from the MicroBlaze cell to implemented melody with note visualitation on the led bar.

NOTICE: The advantage of seberating the code at this spot is that aftre the python libarays are load and the microblaze is flashed the python code followed can be executed and debug indepandently. This saves a lot of time and in case there is an buzzer involved it saves your ears as well.


```python
def play_melody(notes, beats, notes_key, tempo):
    if len(notes) != len(beats):
        return print('Error: Notes and beats must be of same length!')
    #tempo = 124/1.7
    for index, beat in enumerate(beats):
        if notes[index] == ' ':
            time.sleep(beat * tempo/1000)
            set_level(0, 3, 1)
        else:
      #      set_level(list(notes_key.keys()).index(notes[index]), 3, 1) # not needed due to C implementation
            # my_func( list(notes_key.keys()).index(notes[index]) ) # not working because not wrapped
            playNote(notes_key[notes[index]], int(beat * tempo))  
            # print( list(notes_key.keys()).index(notes[index]), notes_key[notes[index]],  notes[index])
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
        if notes[index] == ' ':
            time.sleep(beat * tempo/1000)
            set_level(0, 3, 1)
        else:
       #     set_level(list(notes_key.keys()).index(notes[index]), 3, 1)  # not needed due to C implementation
            playNote(notes_key[notes[index]], int(beat * tempo))            
            print( 'led level, tune, ascii dec value:',
                  list(notes_key.keys()).index(notes[index]),  
                  notes[index], 
                  notes_key[notes[index]] 
                )
        # Delay between notes
        time.sleep(tempo / 200);
```


```python
if __name__ == '__main__':
    # synthesice music and visualize with LED Bar
    tempo = 124/1.7
    notes_key = { ' ': 32, 'B':66, 'c': 99, 'd':100, 'e':101, 'f':102, 'g':103, 'a':97, 'b':98, 'C': 67, 'D': 68 }
    play = [      ' ', 'B'  ]
    play_beats = [  4,   4 ]
    beat_slide = 4

    # play A-Team theme
    A_Team(tempo, notes_key)
```


```python
# play the gamut of the buzzer
music_gamut(notes_key)
```


```python
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

## Python GUI 
Make your own instend custom music. Us the beat slider to set a beat for a tone and add atone by pressing the coresponding button. It will print your beat and play. Beat log, comming soon! Donations are welcome :)


```python
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
        if notes[index] == ' ':
            time.sleep(beat * tempo/1000)
            set_level(0, 3, 1)
        else:
            #set_level(list(notes_key.keys()).index(notes[index]), 3, 1)
            playNote(notes_key[notes[index]], int(beat * tempo)) 
            
        # Delay between notes
        time.sleep(tempo / 300);    


def on_buttonB_clicked(b):
    play_note('B',4)      
    play.append('B')
    play_beats.append(beat_slide)
def on_buttonc_clicked(b):
    play_note('c',4)
    play.append('c')
    play_beats.append(beat_slide)
def on_buttond_clicked(b):
    play_note('d',4)
    play.append('d')
    play_beats.append(beat_slide)
def on_buttone_clicked(b):
    play_note('e',4)
    play.append('e')
    play_beats.append(beat_slide)
def on_buttonf_clicked(b):
    play_note('f',4)
    play.append('f')
    play_beats.append(beat_slide)
def on_buttong_clicked(b):
    play_note('g',4)
    play.append('g')
    play_beats.append(beat_slide)
def on_buttona_clicked(b):
    play_note('a',4)
    play.append('a')
    play_beats.append(beat_slide)
def on_buttonb_clicked(b):
    play_note('b',4)
    play.append('b')
    play_beats.append(beat_slide)
def on_buttonC_clicked(b):
    play_note('C',4)
    play.append('C')
    play_beats.append(beat_slide)
def on_buttonD_clicked(b):
    play_note('D',4)
    play.append('D')
    play_beats.append(beat_slide)
def on_buttonPause_clicked(b):
    play_note(' ',4)      
    play.append(' ')
    play_beats.append(beat_slide)
def on_buttonRun_clicked(b):
    global play, play_beats, notes_key, tempo
    print('play', play)
    print('play_beats', play_beats)
    play_melody(play, play_beats, notes_key, tempo)
def handle_slider_change(change):
    global beat_slide
    beat_slide = change.new
#def handle_sliderTempo_change(change):
#    global tempo
#    tempo = change.new
#def gui():
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
buttonPause = widgets.Button(description="Pause", button_style='success')
buttonRun = widgets.Button(description="Play Awesome", button_style='danger')
slider = widgets.IntSlider(min=1, max=16, value=4, description='Beat') 
#sliderTempo = widgets.IntSlider(min=40, max=150, value=70, description='Tempo')

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
buttonPause.on_click(on_buttonPause_clicked)
buttonRun.on_click(on_buttonRun_clicked)
slider.observe(handle_slider_change, names='value')
#slider.observe(handle_sliderTempo_change, names='value')

buttonPause.layout.margin = "0  0  0 500px"
buttonD.layout.margin = "0  0  0 450px"
buttonC.layout.margin = "0  0  0 400px"
buttonb.layout.margin = "0  0  0 350px"
buttona.layout.margin = "0  0  0 300px"
buttong.layout.margin = "0  0  0 250px"
buttonf.layout.margin = "0  0  0 200px"
buttone.layout.margin = "0  0  0 150px"
buttond.layout.margin = "0  0  0 100px"
buttonc.layout.margin = "0  0  0 50px"
buttonB.layout.margin = "0  0  0 0"
buttonRun.layout.margin = "0  0  0 550px"

display(buttonPause)
display(buttonD)
display(buttonC)
display(buttonb)
display(buttona)
display(buttong)
display(buttonf)
display(buttone)
display(buttond)
display(buttonc)
display(buttonB)
display(buttonRun)
display(slider)
#display(sliderTempo)
```

## MicroBlaze Wrapper

Next cell function set_level() is wrapped by MicroBlaze.


```python
set_level
```

Next cell function ledbar_init() is wrapped by MicroBlaze.


```python
ledbar_init
```

It is uncleare why the MicroBlaze wrapes one function but not another.

Next cell function set_bits() is not wrapped by MicroBlaze.


```python
set_bits(5)
```
