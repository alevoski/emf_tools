# emf_tools
[![License](https://img.shields.io/badge/licence-AGPLv3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0.en.html)
[![Platform](https://img.shields.io/badge/platform-linux-lightgrey.svg)](https://www.linux.com/)
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

The drawback of minicom is we have to put back the timestamp option every time and it is boring to use it along a separated parsing script.

## Getting Started
Download the project on your computer.
```
git clone https://github.com/alevoski/emf_tools.git
```

### Prerequisites

#### Install the required pip module
```
pip install -r requirements.txt
```

#### Put your username in "tty" and "dialout" groups
```
sudo usermod -a -G tty $USER
sudo usermod -a -G dialout $USER
```
You must logout after this operations !

#### Connect and identify your device
```
sudo dmesg | grep tty
```
You shoud see something like
***[  364.321080] usb 2-2: ch341-uart converter now attached to ttyUSB1***  
So you know your device id is ***/dev/ttyUSB1***.

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

## License
emf_tools.
Copyright (C) 2020 Alexandre Buissé alevoski@pm.me

This program is free software: you can redistribute it and/or modify  
it under the terms of the GNU Affero General Public License as published  
by the Free Software Foundation, either version 3 of the License, or  
(at your option) any later version.  

This program is distributed in the hope that it will be useful,  
but WITHOUT ANY WARRANTY; without even the implied warranty of  
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the  
GNU Affero General Public License for more details.  

You should have received a copy of the GNU Affero General Public License  
along with this program.  If not, see <https://www.gnu.org/licenses/>.
