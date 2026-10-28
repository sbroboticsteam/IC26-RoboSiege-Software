import machine 
import time

import network
import socket
import json
import asyncio

import errno

# PIN INIT 
led = machine.Pin("LED", machine.Pin.OUT)
led.on()  

#based on vincents board
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

def set_motor(speed, pin1, pin2, pwm):
    if speed > 0:
        pin1.high()
        pin2.low()
    elif speed < 0:
        pin1.low()
        pin2.high()
    else:
        pin1.low()
        pin2.low()

    pwm.duty_u16(int(abs(speed) * 65535))

def set_left(speed):
    set_motor(speed, in1, in2, m1en)
    set_motor(speed, in3, in4, m2en)
    
def set_right(speed):
    set_motor(speed, in5, in6, m3en)
    set_motor(speed, in7, in8, m4en)

def set_servo(servo, value):
    clamp_val = min(max(value, -1.0),1.0)
    norm_val = (clamp_val + 1) / 2
    #min and max servo pulse values in microseconds
    a = 600
    b = 2400
    #interpolated servo value
    lerp = a * (1-norm_val) + b * norm_val
    
    #multiply by 1000 for nanoseconds
    servo.duty_ns(int(lerp * 1000))
    
def mecanum_drive(x, y, rot):
    # Clamp joystick inputs
    x = min(max(x, -1.0), 1.0)
    y = min(max(y, -1.0), 1.0)

    # calculat individual motor speeds
    front_left  = y + x + rot
    rear_left   = y - x + rot
    front_right = y - x - rot
    rear_right  = y + x - rot

    #normalize
    max_speed = max(
        abs(front_left),
        abs(rear_left),
        abs(front_right),
        abs(rear_right),
        1.0
    )

    front_left /= max_speed
    rear_left /= max_speed
    front_right /= max_speed
    rear_right /= max_speed

    set_motor(front_left, in1, in2, m1en)
    set_motor(rear_left, in3, in4, m2en)
    set_motor(rear_right, in5, in6, m3en)
    set_motor(front_right, in7, in8, m4en)

#set stby1 pins high
stby1.on()
stby2.on()

# WLAN INIT

with open("config.json", "r") as f:
    config = json.load(f)

network.hostname(config["HOSTNAME"])

wlan = network.WLAN(network.STA_IF) 
wlan.active(True)           
wlan.scan()    
wlan.isconnected()
wlan.connect(config["SSID"], config["PASSWORD"]) 
while not wlan.isconnected():
    machine.idle()
print("WIFI CONNECTED")
print(f"IP:{wlan.ipconfig('addr4')}")
wlan.config(hostname=config["HOSTNAME"])
print(f"hostname: {wlan.config("hostname")}")

# SOCKET INIT
PORT = 5005
command_queue = []
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", PORT))
sock.setblocking(False)

print("UDP server listening on", PORT)

async def listen_command():
    try:
        while True:
            try:
                data, _ = sock.recvfrom(1024)
            except OSError as e:
                if e.args[0] != errno.EAGAIN:
                    raise
            else:
                str_packet = data.decode()
                json_packet = json.loads(str_packet)             
                command_queue.insert(0, json_packet)

            await asyncio.sleep_ms(10)
    finally:
        sock.close()

async def perform_command():
    try:
        while True:
            if len(command_queue) > 0:
                command = command_queue.pop()
                x = command["x"]
                y = command["y"]
                rot = command["rot"]
                j1 = command["j1"]
                j2 = command["j2"]
                print(command)
                
                mecanum_drive(x, y, rot)
                set_servo(servo1, j1)
                set_servo(servo2, j2)
            await asyncio.sleep_ms(10)
    finally:
        sock.close()

async def async_loop():
    asyncio.create_task(listen_command())
    asyncio.create_task(perform_command())
    
    while True:
        await asyncio.sleep(1)

#run the loop
asyncio.run(async_loop())