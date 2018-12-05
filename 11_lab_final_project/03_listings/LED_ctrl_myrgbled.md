
## LED Ctrl RGB

Use buttons and sliders to control the LEDs on the board.

The program is started by select Menubar -> Cell -> Run All

Cell -> Current Outputs -> Toggle Scrolling
   


```python
import time
from pynq.overlays.base import BaseOverlay

import ipywidgets as widgets
from IPython.display import display
from multiprocessing import Process
from multiprocessing.sharedctypes import Value

base = BaseOverlay("base.bit")
```



### Define functions here
Function decision() provides the computaion of the win and loss with average and a consol ouput accordingly.
#### Colors RGB LED No 4 and 5
    off = 0    blue = 1    green = 2    türkies = 3    red = 4    purple = 5    yellow = 6
    white = 7



```python
def all_led_off():
    # turn all led's off
    for led in base.leds:
        led.off()    
    base.rgbleds[4].off()
    base.rgbleds[5].off()
    
def on_button0_clicked(b):
    if bt_led_state0.value == 0:
        bt_led_state0.value = 1
        base.leds[0].on()
    else:
        bt_led_state0.value = 0     
        base.leds[0].off()
    ldStatus0.value = '' + ('False' if base.leds.read() & int('0001',2) == 0 else 'True')
    
def on_button1_clicked(b):
    if bt_led_state1.value == 0:
        base.leds[1].on()
        bt_led_state1.value = 1   
    else:
        bt_led_state1.value = 0  
        base.leds[1].off()
    ldStatus1.value = '' + ('False' if base.leds.read() & int('0010',2) == 0 else 'True')
    
def on_button2_clicked(b):
    if bt_led_state2.value == 0:
        base.leds[2].on()
        bt_led_state2.value = 1
    else:
        bt_led_state2.value = 0  
        base.leds[2].off()
    ldStatus2.value = '' + ('False' if base.leds.read() & int('0100',2) == 0 else 'True')
    
def on_button3_clicked(b):
    if bt_led_state3.value == 0:
        base.leds[3].on()
        bt_led_state3.value = 1
    else:
        bt_led_state3.value = 0  
        base.leds[3].off()
    ldStatus3.value = '' + ('False' if base.leds.read() & int('1000',2) == 0 else 'True')
    
def on_button4_clicked(b):
    exit.value = 1
    
def handle_slider0_change(change):
    green_duty.value = change.new
    
def handle_slider1_change(change):
    blue_duty.value = change.new
    
def handle_slider2_change(change):
    red_duty.value = change.new
    
def handle_slider3_change(change):
    frequency.value = change.new
    
def handle_slider4_change(change):
    led_freq.value = change.new
    
def handle_check0_change(LED0):
    led0_check.value = int(LED0)
    
def handle_check1_change(LED1):
    led1_check.value = int(LED1)
    
def handle_check2_change(LED2):
    led2_check.value = int(LED2)
    
def handle_check3_change(LED3):
    led3_check.value = int(LED3)
    
def led_control(which_led, bt_status, check_status):
    if check_status and bt_status != 0:
        base.leds[which_led].toggle()
    else:
        if bt_status:
            base.leds[which_led].on()
        else:
            base.leds[which_led].off()    

def run_leds():
    # function to run LED output with flash function in process
    while( 1 ):      
        # LED control
        led_control(0, bt_led_state0.value, led0_check.value)
        led_control(1, bt_led_state1.value, led1_check.value)
        led_control(2, bt_led_state2.value, led2_check.value)
        led_control(3, bt_led_state3.value, led3_check.value)

        # update LED status
        ldStatus0.value = '' + ('False' if base.leds.read() & int('0001',2) == 0 else 'True')
        ldStatus1.value = '' + ('False' if base.leds.read() & int('0010',2) == 0 else 'True')
        ldStatus2.value = '' + ('False' if base.leds.read() & int('0100',2) == 0 else 'True')
        ldStatus3.value = '' + ('False' if base.leds.read() & int('1000',2) == 0 else 'True') 
        
        # defines interval time
        time.sleep(led_freq.value/100)
        
        # terminate process
        if exit.value:
            break
        
def run_pwm2():  
    # prvides PWM for RGB LED        
    try:           
        while( 1 ):
            if red_duty.value != 0:
                base.rgbleds[4].pwmd(red.value, red_duty.value, frequency.value)
            if green_duty.value != 0:
                base.rgbleds[4].pwmd(green.value, green_duty.value, frequency.value)
            if blue_duty.value != 0:
                base.rgbleds[4].pwmd(blue.value, blue_duty.value, frequency.value)
            # terminate process
            if exit.value:
                break
    except KeyboardInterrupt:
        raise
        
def run_gui():
    # setup GUI and displays it       

    button0.on_click(on_button0_clicked)
    button1.on_click(on_button1_clicked)
    button2.on_click(on_button2_clicked)
    button3.on_click(on_button3_clicked)
    button4.on_click(on_button4_clicked)

    slider0.observe(handle_slider0_change, names='value')
    slider1.observe(handle_slider1_change, names='value')
    slider2.observe(handle_slider2_change, names='value')
    slider3.observe(handle_slider3_change, names='value')
    slider4.observe(handle_slider4_change, names='value')
    
    check0.observe(handle_check0_change)
    check1.observe(handle_check1_change)
    check2.observe(handle_check2_change)
    check3.observe(handle_check3_change)

    # display LED toggle controls 
    left_box = widgets.VBox([button0, ldStatus0])
    right_box = widgets.VBox([button1, ldStatus1])
    left1_box = widgets.VBox([button2, ldStatus2])
    right1_box = widgets.VBox([button3, ldStatus3])
    box = widgets.HBox([left_box, right_box, left1_box, right1_box])
    box.layout.border='solid 2px lightgray'
    box.layout.padding='10px 10px 10px 10px'
    display(box)
    
    # display LED flash controls 
    left3_box = widgets.VBox([slider4])
    right3_box = widgets.VBox([check0, check1, check2, check3])
    box3 = widgets.HBox([left3_box, right3_box])
    box3.layout.border='solid 2px lightgreen'
    box3.layout.padding='10px 10px 10px 10px'
    display(box3)
    
    # display RGB controls 
    left2_box = widgets.VBox([slider0, slider1, slider2])
    right2_box = widgets.VBox([slider3])
    box1 = widgets.HBox([left2_box, right2_box])
    box1.layout.border='solid 2px lightblue'
    box1.layout.padding='10px 10px 10px 10px'
    display(box1)
    
    # Exit Button
    display(button4)
    
```

### Start progarm


```python
if __name__ == '__main__':
    # Gui variables
    button0 = widgets.Button(description="LD0", button_style='primary')
    button1 = widgets.Button(description="LD1", button_style='success')
    button2 = widgets.Button(description="LD2", button_style='danger')
    button3 = widgets.Button(description="LD3", button_style='warning')
    button4 = widgets.Button(description="Exit", button_style='danger')

    ldStatus0 = widgets.Label(value='False')
    ldStatus1 = widgets.Label(value='False')
    ldStatus2 = widgets.Label(value='False')
    ldStatus3 = widgets.Label(value='False')

    check0 = widgets.interactive(handle_check0_change, LED0=False)
    check1 = widgets.interactive(handle_check1_change, LED1=False)
    check2 = widgets.interactive(handle_check2_change, LED2=False)
    check3 = widgets.interactive(handle_check3_change, LED3=False)
    
    slider0 = widgets.IntSlider(min=0, max=100, value=0, description='Green')
    slider1 = widgets.IntSlider(min=0, max=100, value=0, description='Blue')
    slider2 = widgets.IntSlider(min=0, max=100, value=0, description='Red')
    slider3 = widgets.IntSlider(min=30, max=20000, value=20000, description='Frequency')
    slider4 = widgets.IntSlider(min=10, max=100, value=75, description='LED Flash')

    # LED variables
    led_freq = Value('i', 75)
    led0_check = Value('i', 0)
    led1_check = Value('i', 0)
    led2_check = Value('i', 0)
    led3_check = Value('i', 0)
    bt_led_state0 = Value('i', 0)
    bt_led_state1 = Value('i', 0)
    bt_led_state2 = Value('i', 0)
    bt_led_state3 = Value('i', 0)
    
    # RGB gloabal variables
    blue = Value('i', 1)
    green = Value('i', 2)
    red = Value('i', 4)
    blue_duty = Value('i', 0)
    green_duty = Value('i', 0)
    red_duty = Value('i', 0)
    frequency = Value('i', 20000)
    
    # terminate process
    exit = Value('i', 0)
    
    # turn all led's off
    all_led_off()
    
    # LED show of
    for x in range(3):
        base.leds[x].on()
        base.leds[x+1].on()
        base.rgbleds[4].rgb_on(2**x);
        base.rgbleds[5].rgb_on(2**x);
        time.sleep(1)
        all_led_off()
    
    # start GUI
    run_gui()
    
    # running pwm in seperate process
    try:           
        p_pwm = Process(target=run_pwm2, args=(), name='pwm2')
        p_pwm.start()
    except:
           raise
            
    # running led flash in seperate process
    try:           
        p_led_flash = Process(target=run_leds, args=(), name='led_flash')
        p_led_flash.start()
    except:
           raise

    #print('Am I blocked?') # debug only

```


<p>Failed to display Jupyter Widget of type <code>HBox</code>.</p>
<p>
  If you're reading this message in the Jupyter Notebook or JupyterLab Notebook, it may mean
  that the widgets JavaScript is still loading. If this message persists, it
  likely means that the widgets JavaScript library is either not installed or
  not enabled. See the <a href="https://ipywidgets.readthedocs.io/en/stable/user_install.html">Jupyter
  Widgets Documentation</a> for setup instructions.
</p>
<p>
  If you're reading this message in another frontend (for example, a static
  rendering on GitHub or <a href="https://nbviewer.jupyter.org/">NBViewer</a>),
  it may mean that your frontend doesn't currently support widgets.
</p>




<p>Failed to display Jupyter Widget of type <code>HBox</code>.</p>
<p>
  If you're reading this message in the Jupyter Notebook or JupyterLab Notebook, it may mean
  that the widgets JavaScript is still loading. If this message persists, it
  likely means that the widgets JavaScript library is either not installed or
  not enabled. See the <a href="https://ipywidgets.readthedocs.io/en/stable/user_install.html">Jupyter
  Widgets Documentation</a> for setup instructions.
</p>
<p>
  If you're reading this message in another frontend (for example, a static
  rendering on GitHub or <a href="https://nbviewer.jupyter.org/">NBViewer</a>),
  it may mean that your frontend doesn't currently support widgets.
</p>




<p>Failed to display Jupyter Widget of type <code>HBox</code>.</p>
<p>
  If you're reading this message in the Jupyter Notebook or JupyterLab Notebook, it may mean
  that the widgets JavaScript is still loading. If this message persists, it
  likely means that the widgets JavaScript library is either not installed or
  not enabled. See the <a href="https://ipywidgets.readthedocs.io/en/stable/user_install.html">Jupyter
  Widgets Documentation</a> for setup instructions.
</p>
<p>
  If you're reading this message in another frontend (for example, a static
  rendering on GitHub or <a href="https://nbviewer.jupyter.org/">NBViewer</a>),
  it may mean that your frontend doesn't currently support widgets.
</p>




<p>Failed to display Jupyter Widget of type <code>Button</code>.</p>
<p>
  If you're reading this message in the Jupyter Notebook or JupyterLab Notebook, it may mean
  that the widgets JavaScript is still loading. If this message persists, it
  likely means that the widgets JavaScript library is either not installed or
  not enabled. See the <a href="https://ipywidgets.readthedocs.io/en/stable/user_install.html">Jupyter
  Widgets Documentation</a> for setup instructions.
</p>
<p>
  If you're reading this message in another frontend (for example, a static
  rendering on GitHub or <a href="https://nbviewer.jupyter.org/">NBViewer</a>),
  it may mean that your frontend doesn't currently support widgets.
</p>


