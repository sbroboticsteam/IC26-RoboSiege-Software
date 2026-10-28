import json
import os
import socket
import time
import pygame
import keyboard

# keep reading the controller even when the terminal isn't the focused window
os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

#Pico IP address (from Thonny output)
SERVER_IP = "" # you might be able to use hostname, but its unreliable
SERVER_PORT = 5005
POLL_INTERVAL = 0.02  # how often the controller is read (50 Hz)


# axis + button constants

# return somekind of Python Dict as a command given a joystick
def get_inputs(joy):
    
    pass



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
    next_send = time.monotonic()
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

        # send commands
        #CALL get_inputs() HERE AND WRITE SEND THE DATA OVER THE SOCKET HERE

        time.sleep(POLL_INTERVAL)
except KeyboardInterrupt:
    pass
finally:
    client_sock.close()
    pygame.quit()
