# emf_tools
[![License](https://img.shields.io/badge/licence-AGPLv3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0.en.html)

[![Language](https://img.shields.io/badge/language-python3-orange.svg)](https://www.python.org/)

Emf_tools is a repository with tools (currently one) to help with emf meters.  
Tested on a Cornet ED88Tplus.

The goal of the script **cornet_emf_parser_full.py** is to :
- read data from the device USB/serial interface
- decode and parse the data
- display them
- and optionaly
  - save them into a CSV format file
  - chose what to save according various criteria (value alarm, targeted frequency)

Originately I did that with minicom (configured with (speed) 9600, (data) 8bit, (parity) no parity and (stopbits) 1 stop), tee and a bit of parsing with Python :  
```
sudo minicom -D <your device from dmesg | grep tty> | tee myoutput
```

The cons of minicom is we have to put the timestamp option every time back and it is boring to used it along a separated parsing script.

## Getting Started
Download the project on your computer.
```
git clone https://github.com/alevoski/emf_tools.git
```

### Prerequisites

#### Install the required pip modules
```
pip install -r requirements.txt
```

#### Put your username in "tty" and "dialout" groups
```
sudo usermod -a -G tty $USER')
sudo usermod -a -G dialout $USER')
```
You must logout after this operations !

#### Connect and identify your device
```
sudo dmesg | grep tty
```
You shoud see something like
***[  364.321080] usb 2-2: ch341-uart converter now attached to ttyUSB1***
So you know your device is id as /dev/ttyUSB1

## HOW TO USE ?
```
cd emf_tools/
cornet_emf_parser_full.py (source by default is /dev/ttyUSB0)
```
Or, to change default source and save the output
```
cornet_emf_parser_full.py --source=/dev/ttyUSB1 --output=test_output
```

### To show help and some examples
```
python3 cornet_emf_parser_full.py -h
```

## Author
Alexandre Buissé
