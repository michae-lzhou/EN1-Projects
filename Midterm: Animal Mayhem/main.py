from machine import Pin, PWM
import time

POWER_LEVEL = 65025
# lower right pins with USB on top
RIGHT_FORWARD_PIN = 8
RIGHT_REVERSE_PIN = 9

right_forward = PWM(Pin(RIGHT_FORWARD_PIN))
right_reverse = PWM(Pin(RIGHT_REVERSE_PIN))

def spin_wheel(pwm):
    pwm.duty_u16(POWER_LEVEL)
    time.sleep(0.1)
    pwm.duty_u16(0)
    time.sleep(0)
    
def beep(frequency = 440):
    buzzer = machine.PWM(machine.Pin(22))
    buzzer.freq(frequency)
    buzzer.duty_u16(int(65536/2))
    time.sleep(0.2)
    buzzer.duty_u16(0)
        
def light(adc = 28):
    photo_pin = machine.ADC(adc)  # port 1
    done = False;

    while not done:
        val = photo_pin.read_u16()
        print(val)
        time.sleep(.2)
        if(val <= 40000):
            print('wagging')
            spin_wheel(right_forward)
            time.sleep(0.2)
            spin_wheel(right_reverse)
            
        else:
            
            
    
light()

#print('right forward')
#spin_wheel(right_forward)

#print('right reverse')
#spin_wheel(right_reverse)
