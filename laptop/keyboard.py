import json
import socket
import threading
import time

from pynput import keyboard  # pip install pynput

# Pico IP address (from Thonny output)
SERVER_IP = ""  # you might be able to use hostname, but its unreliable
SERVER_PORT = 5005
SEND_INTERVAL = 0.02  # how often a command is sent (50 Hz, same as the controller)

# Each field: (key for +1, key for -1). Neither or both held -> 0.
# Matches the controller script's fields and directions.
INPUTS = {
    "x": ("d", "a"),          # strafe right / left   (left stick x)
    "y": ("w", "s"),          # forward / back        (left stick y)
    "rot": ("right", "left"), # turn right / left     (right stick x)
    "j1": ("o", "k"),         # joint 1 fwd / back    (B / A)
    "j2": ("p", "l"),         # joint 2 fwd / back    (Y / X)
}
KEYS = {k for pair in INPUTS.values() for k in pair}

# Keys currently held down (updated by the keyboard listener thread)
pressed = set()
lock = threading.Lock()


def key_name(key):
    """Return 'left'/'right' for the arrow keys, the lowercase letter for
    character keys, or None for anything else."""
    if key == keyboard.Key.left:
        return "left"
    if key == keyboard.Key.right:
        return "right"
    try:
        return key.char.lower() if key.char else None
    except AttributeError:
        return None


def on_press(key):
    if key == keyboard.Key.esc:
        return False  # stops the listener, which ends the main loop
    name = key_name(key)
    if name in KEYS:
        with lock:
            pressed.add(name)


def on_release(key):
    name = key_name(key)
    if name in KEYS:
        with lock:
            pressed.discard(name)


def get_inputs():
    """Return {"x", "y", "rot", "j1", "j2"}, each -1.0, 0.0 or 1.0."""
    with lock:
        return {
            name: float((pos in pressed) - (neg in pressed))
            for name, (pos, neg) in INPUTS.items()
        }


# SOCKET INIT
client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_addr = (SERVER_IP, SERVER_PORT)

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
print("WASD = move, Left/Right arrows = turn, O/K = j1, P/L = j2. Esc to quit.")

# main loop - constantly send keyboard data
try:
    while listener.running:
        message = json.dumps(get_inputs())
        client_sock.sendto(message.encode(), server_addr)
        print("Sent:", message)

        time.sleep(SEND_INTERVAL)
except KeyboardInterrupt:
    pass
finally:
    listener.stop()
    client_sock.close()
    print("Stopped.")