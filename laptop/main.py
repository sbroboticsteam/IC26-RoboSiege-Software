import json
import os
import socket
import time
import pygame

# keep reading the controller even when the terminal isn't the focused window
os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

#Pico IP address (from Thonny output)
SERVER_IP = "" # you might be able to use hostname, but its unreliable
SERVER_PORT = 5005
SEND_INTERVAL = 0.05  # seconds between sends
POLL_INTERVAL = 0.02  # how often the controller is read (50 Hz)

DEADZONE = 0.1  # stick values smaller than this count as 0 (sticks drift)

# axis + button constants for pygame Xbox controller
LEFT_X_AXIS = 0
LEFT_Y_AXIS = 1
RIGHT_X_AXIS = 2
RIGHT_Y_AXIS = 3
SHOW_RAW_AXES = False

A_BUTTON = 0
B_BUTTON = 1
X_BUTTON = 2
Y_BUTTON = 3

def apply_deadzone(value):
    if abs(value) < DEADZONE:
        return 0.0
    sign = 1.0 if value > 0 else -1.0
    scaled = (abs(value) - DEADZONE) / (1.0 - DEADZONE)
    return round(sign * min(scaled, 1.0), 3)


def get_inputs(joy):
    if joy is None:
        return {"x": 0.0, "y": 0.0, "rot": 0.0, "j1": 0.0, "j2": 0.0}
    return {
        "x": apply_deadzone(joy.get_axis(LEFT_X_AXIS)), # left stick right/left
        "y": apply_deadzone(-joy.get_axis(LEFT_Y_AXIS)), # left stick forward/back, flip upsided down 
        "rot": apply_deadzone(joy.get_axis(RIGHT_X_AXIS)), # left stick forward/back
        # joint 1: b = forward a = backward
        "j1": float(
            joy.get_button(B_BUTTON) -
            joy.get_button(A_BUTTON)
        ),

        # joint 2: y = forward x = backward
        "j2": float(
            joy.get_button(Y_BUTTON) -
            joy.get_button(X_BUTTON)
        )
    }


pygame.init()
pygame.joystick.init()

# SOCKET INIT
client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_sock.settimeout(0.5)
server_addr = (SERVER_IP, SERVER_PORT)

joy = None
print("waiting for Xbox controller")

# main loop - constantly send controller data
try:
    while True:
        for event in pygame.event.get():
            # connected/disconnected message
            if event.type == pygame.JOYDEVICEADDED and joy is None:
                joy = pygame.joystick.Joystick(event.device_index)
                print(f"connected: {joy.get_name()} ({joy.get_numaxes()} axes)")

            elif event.type == pygame.JOYDEVICEREMOVED and joy is not None:
                if event.instance_id == joy.get_instance_id():
                    print("Controller disconnected, sending zeros")
                    joy = None

        message = json.dumps(get_inputs(joy))
        client_sock.sendto(message.encode(), server_addr)
        print("Sent:", message)

        time.sleep(POLL_INTERVAL)
except KeyboardInterrupt:
    pass
finally:
    client_sock.close()
    pygame.quit()
