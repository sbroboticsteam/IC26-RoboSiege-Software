import machine 
import time

import network
import socket
import json
import asyncio

import errno

# PIN INIT (editing required)
led = machine.Pin("LED", _)
led.on()  

#base these on your board
stby1 = machine.Pin(_, _)

in1 = machine.Pin(_, _)                 
in2 = machine.Pin(_, _)                
m1en = machine.PWM(machine.Pin(_))
m1en.freq(1000) 

in3 = machine.Pin(_, _) 
in4 = machine.Pin(_, _)
m2en = machine.PWM(machine.Pin(_))
m2en.freq(1000)

stby2 = machine.Pin(_, _)

in5 = machine.Pin(_, _) 
in6 = machine.Pin(_, _)
m3en = machine.PWM(machine.Pin(_))
m3en.freq(1000)

in7 = machine.Pin(_, _) 
in8 = machine.Pin(_, _)
m4en = machine.PWM(machine.Pin(_))
m4en.freq(1000)

servo1 = machine.PWM(machine.Pin(_))
servo1.freq(50)
servo2 = machine.PWM(machine.Pin(_))
servo2.freq(50)

def set_motor(speed, pin1, pin2, pwm):
    pass

def set_left(speed):
    pass
    
def set_right(speed):
    pass

def set_servo(servo, value):
    pass

def mecanum_drive(x, y, rot):
    pass

#set stby1 pins high
stby1.on()
stby2.on()

# WLAN INIT (no editing required)
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
wlan.config(hostname=config["HOSTNAME"]) # change HOSTNAME in config.json to your robots name - itll show on WiFi
print(f"hostname: {wlan.config("hostname")}")

# SOCKET INIT (editing optional)
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
                # interpret command json entries
                #WRITE YOUR CALLS TO YOUR FUNCTIONS HERE
                print(command)
            await asyncio.sleep_ms(10)
    finally:
        sock.close()

async def async_loop():
    #producer/consumer pattern loop
    asyncio.create_task(listen_command())
    asyncio.create_task(perform_command())
    
    while True:
        await asyncio.sleep(1)

#run the loop
asyncio.run(async_loop())