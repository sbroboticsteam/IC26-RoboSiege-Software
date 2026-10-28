# IC27-RoboSiege-Software

Officially distributed software for SBRT's internal competition for the 2027 season — RoboSiege.

## Requirements

In order to run the software in this repository, you should have VSCode (or a code editor of your choice), Python, and Thonny installed.

### VSCode Installation

Download and install Visual Studio Code from [https://code.visualstudio.com/](https://code.visualstudio.com/).

Once installed, open VSCode and install the **Python** extension by Microsoft from the Extensions tab.

### Python Installation

Download Python from [https://www.python.org/downloads/](https://www.python.org/downloads/).

**Windows:**

- Run the Python installer.
- If the installer offers an **Add Python to PATH** option, enable it. This allows you to run Python from any terminal.
- If using the Python Install Manager, follow its prompts to make Python commands available.
- Verify installation by opening a new terminal and running `python --version` or `py --version`.

**Mac:**

- Download and run the Python installer.
- Open Terminal and verify installation with `python3 --version`.
- Python is generally accessible through `python3` rather than `python`. If the command is not found, ensure the Python installation's executable directory is included in your shell's `PATH`.

### Thonny Installation

Download Thonny from [https://thonny.org/](https://thonny.org/) and install the appropriate version for your operating system.

Thonny will be used to upload and run MicroPython code on the Raspberry Pi Pico.

To configure your Pico:

1. Connect your Raspberry Pi Pico to your computer via USB.
2. Open Thonny and go to **Run → Configure interpreter**.
3. Select **MicroPython (Raspberry Pi Pico)** as the interpreter.
4. Select the appropriate device/port and install MicroPython firmware if prompted.

### Python Packages

For the laptop end of things, we'll need `pygame` and/or `keyboard`.

`pygame` is typically used for game development, but makes creating a user interface and handling external controllers relatively straightforward. `keyboard` is useful if you want to control your robot using only keyboard inputs.

**Optional:** It may help to create a virtual environment if you already have Python installed and don't want packages to conflict:

```bash
python -m venv .venv
```

On Mac, use `python3 -m venv .venv` if `python` is unavailable.

Activate the virtual environment with:

**Windows**

```cmd
.venv\Scripts\activate
```

**Mac:**

```bash
source .venv/bin/activate
```

To install the necessary Python packages, open a terminal in the repository's root directory, then run:

```bash
cd laptop
python -m pip install -r requirements.txt
```

On Mac, use `python3 -m pip` if you aren't using a virtual environment.

## Directories

- `/laptop` — Contains the Python code that runs on your laptop, including controller input and UDP communication.
- `/pico` — Contains the MicroPython code that runs on the Raspberry Pi Pico, including motor control and receiving UDP commands.

The laptop and Pico must be connected to the same network for UDP communication to work.
