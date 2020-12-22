#!/usr/bin/python3
# -*- coding: utf-8 -*-
#cornet_emf_parser_full.py
#@Alexandre Buissé - 2020

'''
cornet_emf_parser_full.py is a script to read and parse output from an EMF device USB serial port.
It has been tested with a Cornet ED88Tplus.
'''

#Standard imports
import re
import sys
import datetime
import argparse

#Third party import
try:
    import serial
except ModuleNotFoundError:
    print('You need to install pyserial to run this script !')
    print('Try : pip3 install pyserial')
    sys.exit()

def usage():
    '''
    Help function
    '''
    print()
    print('This script will help you read and parse Cornet EMF detector raw data from pyserial output')
    print('Tested on Cornet ED88Tplus')
    print('----EXAMPLES----')
    print(str(sys.argv[0:][0]) + ' --source=/dev/ttyUSB1')
    print(str(sys.argv[0:][0]) + ' --output=test_output')
    print(str(sys.argv[0:][0]) + ' --alarm=0.352')
    print(str(sys.argv[0:][0]) + ' --target=2400')
    print(str(sys.argv[0:][0]) + ' --fmin=52')
    print(str(sys.argv[0:][0]) + ' --fmax=2800')
    print(str(sys.argv[0:][0]) + ' -a=0.352 -t=2400')
    print(str(sys.argv[0:][0]) + ' -a=0.352 -n=52 -x=2800')
    print(str(sys.argv[0:][0]) + ' -a=0.352 -t=2400 -o=test_output')
    print('----------------\n')

def get_timestamp():
    '''
    Return a formated timestamp
    '''
    return '[' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']'

def transforme_val(freq_val_temp, freq_val_num_after_comma):
    '''
    Add a comma to freq_val_temp to position define by freq_val_num_after_comma
    examples :
        0690E-02
        means 0690 and 2 digits after decimal point
        6.90

        0621E-03
        means 0621 et 3 digits after decimal point
        0.690

        0621E-04
        means 0621 et 4 digits after decimal point
        0.0690
    '''

    before = len(freq_val_temp) - freq_val_num_after_comma
    # print('before ' + str(before))
    after = freq_val_num_after_comma
    # print('after ' + str(after))

    before_comma = freq_val_temp[:before]
    # print('before_comma ' + str(before_comma))
    if before == 0 and not before_comma:
        before_comma = '0'
    after_comma = freq_val_temp[-after:]
    new_val = before_comma + '.' + after_comma

    return new_val

def parse_data(raw_line):
    '''
    Take raw_line in parameter and parse it in a proper data
    Return freq_val, freq from this raw_line
    '''
    # Define regex
    freq_val_regex = '(.*)E'
    freq_val_after_comma_regex = 'E-(.*),'
    freq_regex = r',(\d\d\d\d)'

    # Decode bytes and strip leading and trailing spaces
    line = raw_line.decode().strip()

    # print(line)

    # Obtenir est transformer la valeur de la fréquence (0690E-02 => 6.90)
    freq_val_temp = re.findall(freq_val_regex, line)[0]
    # print('freq_val_temp : ' + str(freq_val_temp))
    freq_val_num_after_comma = re.findall(freq_val_after_comma_regex, line)[0]
    # print('freq_val_num_after_comma : ' + str(freq_val_num_after_comma))
    freq_val = transforme_val(freq_val_temp, int(freq_val_num_after_comma))

    # Obtenir la fréquence
    freq = re.findall(freq_regex, line)[0]

    return freq_val, freq

def save_to_file(csvfile, line):
    '''
    Save parsed line to a file
    '''
    with open(csvfile, mode='a', encoding='utf-8') as newfile:
        newfile.write(line + '\n')

def show_info(source, out, alarm, target, fmin, fmax):
    '''
    Display output with vars in parameter
    '''
    print('**Reading data from your device** (stop with CTRL+Z)')
    print('source : ' + source)
    if out:
        print('output file : ' + out)
    if alarm:
        print('alarm : ' + alarm)

    if target:
        print('target : ' + target)

    if fmin:
        print('fmin : ' + fmin)

    if fmax:
        print('fmax : ' + fmax)

def main(source="/dev/ttyUSB0", out=None, alarm=None, target=None, fmin=None, fmax=None):
    '''
    Main function
    '''
    try:
        port = serial.Serial(source, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=3.0)
    except serial.serialutil.SerialException as serial_exception:
        print(serial_exception)
        if "No such file or directory" in str(serial_exception):
            print('Device could not be opened, is it plug ?')
        elif "Permission denied" in str(serial_exception):
            print('Permission denied : you need to put your username in "tty" and "dialout" groups !')
            print('Try : sudo usermod -a -G tty $USER')
            print('Try : sudo usermod -a -G dialout $USER')
            print('(note : you must logout after this operations)')
        sys.exit()

    with port as port_serie:
        if port_serie.isOpen():
            show_info(source, out, alarm, target, fmin, fmax)
            while True:
                raw_line = port_serie.readline()
                if not raw_line: # if nothing until timeout : break
                    print('No data returned from your device : are you in RF mode ?')
                    break
                # print('raw : ' + str(raw_line))
                timestamp = get_timestamp()
                freq_val, freq = parse_data(raw_line)

                store_line = False
                alarmed = True
                # Display/save only if output aim to params
                if alarm:
                    store_line = False
                    alarmed = False
                    if float(freq_val) >= float(alarm):
                        alarmed = True

                if target and alarmed:
                    store_line = False
                    # print('freq : ' + str(freq))
                    # print('target : ' + str(target))
                    if int(freq) == int(target):
                        store_line = True

                if fmin and not fmax and alarmed:
                    store_line = False
                    if int(freq) >= int(fmin):
                        store_line = True

                if fmax and not fmin and alarmed:
                    store_line = False
                    if int(freq) <= int(fmax):
                        store_line = True

                if fmin and fmax and alarmed:
                    store_line = False
                    if int(freq) >= int(fmin) and int(freq) <= int(fmax):
                        store_line = True

                if not alarm and not target and not fmin and not fmax:
                    store_line = True

                if store_line:
                    tosave = timestamp + ',' + freq_val + ',' + freq
                    print(tosave)

                # Save to file if out is set
                if out and store_line:
                    save_to_file(out, tosave)

DESCRIPTION = '''
This script will help you read and parse Cornet EMF detector raw data RF output from its USB Serial interface with pyserial
Tested on Cornet ED88Tplus
'''

EXAMPLES = '''Examples :
    cornet_emf_parser_full.py --source=/dev/ttyUSB1
    cornet_emf_parser_full.py --output=test_output
    cornet_emf_parser_full.py --alarm=0.352
    cornet_emf_parser_full.py --target=2400
    cornet_emf_parser_full.py --fmin=52
    cornet_emf_parser_full.py --fmax=2800
    cornet_emf_parser_full.py -a=0.352 -t=2400
    cornet_emf_parser_full.py -a=0.352 -n=52 -x=2800
    cornet_emf_parser_full.py -a=0.352 -t=2400 -o=test_output
'''

PARSER = argparse.ArgumentParser(prog='cornet_emf_parser_full.py',
                                 description=DESCRIPTION, epilog=EXAMPLES,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
PARSER.add_argument('-s', '--source', help='Your device source (see dmesg | grep tty) (default is /dev/ttyUSB0)', required=False, default='/dev/ttyUSB0')
PARSER.add_argument('-o', '--output', help='Filename of your output file if you want to save data', required=False, default=None)
PARSER.add_argument('-a', '--alarm', help='Frequency value limit which will enable a data to be keep', required=False, default=None)
PARSER.add_argument('-t', '--target', help='Target frequency (ie : 720)', required=False, default=None)
PARSER.add_argument('-n', '--fmin', help='Minimum frequency to target (ie : 700)', required=False, default=None)
PARSER.add_argument('-x', '--fmax', help='Maximum frequency to target (ie : 2600)', required=False, default=None)

ARGS = PARSER.parse_args()

main(ARGS.source, ARGS.output, ARGS.alarm, ARGS.target, ARGS.fmin, ARGS.fmax)
