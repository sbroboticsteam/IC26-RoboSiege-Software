from microdot import Microdot
from microdot.websocket import with_websocket
from microdot.cors import CORS
from machine import Pin, PWM
import machine
import asyncio 
import network
import time

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('WIFI_NAME', 'PASSWORD')
time.sleep(5)

# Wait for connection
max_attempts = 10
attempt = 0

while not wlan.isconnected() and attempt < max_attempts:
    print(f"Trying to connect (Attempt {attempt + 1}/{max_attempts})...")
    time.sleep(10)
    attempt += 1

# Connection is successful when LED blinks on the Pi
if wlan.isconnected():
    print("Connected to IP:", wlan.ifconfig()[0])
    led = Pin("LED", Pin.OUT)
    for i in range(5):
        print(i)
        led.on()
        time.sleep(1)
        led.off()
        time.sleep(1)
else:
    print("Failed to connect to Wi-Fi. Please check your SSID and password.")
    
# Initialize PWM and direction pins 
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
    speed = min(max(speed, -1.0), 1.0)
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

    m1en.duty_u16(int(abs(speed * 65535)))
    m2en.duty_u16(int(abs(speed * 65535)))
    
def set_right(speed):
    speed = min(max(speed, -1.0), 1.0)

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

    m3en.duty_u16(int(abs(speed * 65535)))
    m4en.duty_u16(int(abs(speed * 65535)))
                                                # Set PWM duty cycle to 0 (stop)
 

def drive(left, right):
    set_left(left)
    set_right(right)

stby1.on()
stby2.on()


app = Microdot()
CORS(app, allowed_origins = '*', allow_credentials = True)


@app.route('/hello_world', methods=['GET'])
async def get_invoices(request):
    return 'Hello World!'

@app.get('/')
@with_websocket
async def index(request, ws):
    try: 
        while True:
            data = await ws.receive()
            if not data:
                break
            await ws.send('hello world')
            
    except OSError as msg:
        print(msg)

@app.get('/motion')
@with_websocket
async def index(request, ws):
    # Main movement function
    def move(x, y):
        print("moving\n")
        abs_x, abs_y = abs(x), abs(y)

        if x >= 0 and y >= 0:  # Forward and turn right
            # drive(y, abs(abs_y - abs_x))
            drive(y, y-x)

        elif x <= 0 and y <= 0:  # Backward and turn left
            # print("backward and turn left")
            # set_wheel_direction((1, 0), (1, 0))  # Both wheels backward
            drive(y-x, y)

        elif x >= 0 and y <= 0:  # Backward and turn right
            # print("backward and turn right")
            # set_wheel_direction((1, 0), (1, 0))  # Both wheels backward
            drive(y, y-x)

        elif x <= 0 and y >= 0:  # Forward and turn left
            # print("forward and turn left")
            # set_wheel_direction((0, 1), (0, 1))  # Both wheels forward
            drive(y-x, y)
            
    while True:
        data = await ws.receive()
        if not data:
            break
        direction = data.split(",")
        x = direction[0]
        y = direction[1]        
        move(int(float(x)), int(float(y)))
        
        await ws.send('good bye')
app.run(port=80)