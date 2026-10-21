import machine 
import time

led = machine.Pin("LED", machine.Pin.OUT)
led.on()  


stby1 = machine.Pin(5, machine.Pin.OUT)

in1 = machine.Pin(4, machine.Pin.OUT)                 
in2 = machine.Pin(3, machine.Pin.OUT)                
m1en = machine.PWM(machine.Pin(2))
m1en.freq(1000)

in3 = machine.Pin(6, machine.Pin.OUT) 
in4 = machine.Pin(7, machine.Pin.OUT)
m2en = machine.PWM(machine.Pin(8))
m2en.freq(1000)

stby2 = machine.Pin(21, machine.Pin.OUT);

in5 = machine.Pin(20, machine.Pin.OUT) 
in6 = machine.Pin(19, machine.Pin.OUT)
m3en = machine.PWM(machine.Pin(15))
m3en.freq(1000)

in7 = machine.Pin(22, machine.Pin.OUT) 
in8 = machine.Pin(26, machine.Pin.OUT)
m4en = machine.PWM(machine.Pin(27))
m4en.freq(1000)

servo1 = machine.PWM(machine.Pin(28))
servo1.freq(50)
servo2 = machine.PWM(machine.Pin(0))
servo2.freq(50)

def set_left(speed):
    if speed > 0:
        in1.high()
        in2.low()

        in3.high()
        in4.low()
    else:
        in1.low()
        in2.high()
        
        in3.low()
        in4.high()

    m1en.duty_u16(int(abs(speed * 65535 / 100)))
    m2en.duty_u16(int(abs(speed * 65535 / 100)))
    
def set_right(speed):
    if speed > 0:
        in5.high()
        in6.low()

        in7.high()
        in8.low()
    else:
        in5.low()
        in6.high()
        
        in7.low()
        in8.high()

    m3en.duty_u16(int(abs(speed * 65535 / 100)))
    m4en.duty_u16(int(abs(speed * 65535 / 100)))
                                                # Set PWM duty cycle to 0 (stop)
 
stby1.on()
stby2.on()

def set_servo1(value):
    clamp_val = min(max(value, -1.0),1.0)
    norm_val = 2 * clamp_val - 1
    #min and max servo pulse values in microseconds
    a = 1100
    b = 1900
    #interpolated servo value
    lerp = a * (1-norm_val) + b * norm_val
    
    #multiply by 1000 for nanoseconds
    servo1.duty_ns(int(lerp * 1000))

def set_servo2(value):
    clamp_val = min(max(value, -1.0),1.0)
    norm_val = (clamp_val+1)/2
    #min and max servo pulse values in microseconds
    a = 1100
    b = 1900
    #interpolated servo value
    lerp = a * (1-norm_val) + b * norm_val
    
    #multiply by 1000 for nanoseconds
    servo2.duty_ns(int(lerp * 1000))
 
while True:
    set_servo1(1)
    set_servo2(0)
    time.sleep(1)
    
    set_servo1(0)
    set_servo2(-1)
    time.sleep(1)
    
    set_servo1(-1)
    set_servo2(0)
    time.sleep(1)
    
    set_servo1(0)
    set_servo2(1)
    time.sleep(1)

