import machine, time
from machine import Pin

class MakerPi():
    def __init__(self, adc = 28, pwm = 15):
        self.photo_pin = machine.ADC(adc)  # port 7
        
        period = 20 #msec
        frequency = int(1000/period)
        self.min = int(65536/period * 1.0)
        self.mid = int(1.5 * period)
        self.max = int(2.0 * period)

        self.pwm = machine.PWM(machine.Pin(pwm))
        self.pwm.freq(frequency)
        
    def brightness(self):
        return self.photo_pin.read_u16()
    
    def servo(self, angle=0):
        dutycycle = int(((self.max - self.min)/180)*angle)+self.min
        self.pwm.duty_u16(dutycycle)
        
    def beep(self, frequency = 440, pin = 22):
        self.buzzer = machine.PWM(machine.Pin(pin))
        self.freq(frequency)
        self.duty_u16(int(65536/2))
        time.sleep(0.5)
        self.duty_u16(0)

    def light(self, adc = 28):
        self.photo_pin = machine.ADC(adc)  # port 7
        fred = MakerPi(pwm = 15)
        done = False;

        while not done:
            val = self.photo_pin.read_u16()
            print(val)
            time.sleep(.2)
            
            if(val <= 40000):
                fred.servo(-90)
                
            else:
                fred.servo(90)

fred = MakerPi(pwm = 15)
print(fred.brightness())
fred.light()
