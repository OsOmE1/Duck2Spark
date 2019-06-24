import sys
import math
import time

args = sys.argv
if "-i" in args:
    r_file = args[args.index('-i') + 1]
    try:
        open(r_file, 'r')
    except IndexError:
        raise Exception("NoInputFileSpecified")
    except FileNotFoundError:
        raise Exception("NoInputFileSpecified")
else:
    raise Exception("NoInputFileSpecified")
if "-o":
    try:
        w_file = args[args.index('-o') + 1]
    except:
        raise Exception("NoOutputFileSpecified")
    open(w_file, 'w')
else:
    raise Exception("NoOutputFileSpecified")

if "-f":
    try:
        f_delay = args[args.index('-f') + 1]
    except:
        f_delay = None
else:
    f_delay = None
banner = """
  _____             _    ___   _____                  _    
 |  __ \           | |  |__ \ / ____|                | |   
 | |  | |_   _  ___| | __  ) | (___  _ __   __ _ _ __| | __
 | |  | | | | |/ __| |/ / / / \___ \| '_ \ / _` | '__| |/ /
 | |__| | |_| | (__|   < / /_ ____) | |_) | (_| | |  |   < 
 |_____/ \__,_|\___|_|\_\____|_____/| .__/ \__,_|_|  |_|\_
                                    | |                    
                                    |_|      
Written by OsOmE1              
"""
print(banner + '\n')
print(f'Input file: {r_file} \n')
print(f'Output File: {w_file}')
print(f'Generating script..')
time.sleep(1.5)

final_script = """
#include "DigiKeyboard.h"
#include <avr/pgmspace.h>
#define KEY_UP_ARROW 0x52
#define KEY_DOWN_ARROW 0x51
#define KEY_LEFT_ARROW 0x50
#define KEY_RIGHT_ARROW 0x4F
#define KEY_TAB     43

"""
void_loop = """
void loop() {

"""
max_bytes = 6012
strings = []
lines = []
with open(r_file, 'r') as read:
    raw_lines = read.read().splitlines()
    for line in raw_lines:
        opt = line.split(' ', 1)[0]
        try:
            command = line.split(' ', 1)[1]
        except:
            if opt == "ENTER":
                lines.append('DigiKeyboard.sendKeyStroke(KEY_ENTER);')
                continue
            elif opt == "CONTROL" or opt == "CTRL":
                lines.append('DigiKeyboard.sendKeyStroke(MOD_CONTROL_LEFT);')
                continue
            elif opt == "DOWNARROW" or "DOWN":
                lines.append('DigiKeyboard.sendKeyStroke(KEY_DOWN_ARROW);')
                continue
            elif opt == "UPARROW" or "UP":
                lines.append('DigiKeyboard.sendKeyStroke(KEY_UP_ARROW);')
                continue
            elif opt == "LEFTARROW" or "LEFT":
                lines.append('DigiKeyboard.sendKeyStroke(KEY_LEFT_ARROW);')
                continue
            elif opt == "RIGHTARROW" or "RIGHT":
                lines.append('DigiKeyboard.sendKeyStroke(KEY_LEFT_ARROW);')
                continue
            elif opt == "TAB":
                lines.append('DigiKeyboard.sendKeyStroke(KEY_TAB);')
                continue
            elif opt == "TAB":
                lines.append('DigiKeyboard.sendKeyStroke(KEY_TAB);')
                continue
            
        if opt == "REM":
            pass
        elif opt == "STRING":
            if len(command) > 65:
                current_char = 0
                divved_up = []
                for _ in range(1, math.ceil(len(command) / 65) + 1):
                    try:
                        string = command[current_char: current_char + 65]
                        divved_up.append(string)
                    except:
                        string = command.replace(''.join(divved_up), '')
                        divved_up.append(string)
                    current_char += 65
                for part in divved_up:
                    part = part.replace('"', "'")
                    strings.append(f'const char line{str(len(strings) + 1)}[] PROGMEM = "{part}";')
                    lines.append(f'DigiKeyboard.print( GetPsz (line{str(len(strings))}) );')
            else:
                command = command.replace('"', "'")
                strings.append(f'const char line{str(len(strings) + 1)}[] PROGMEM = "{command}";')
                lines.append(f'DigiKeyboard.print( GetPsz (line{str(len(strings))}) );')
        elif opt == "GUI":
            lines.append(f"DigiKeyboard.sendKeyStroke(KEY_{command.upper().strip()}, MOD_GUI_LEFT);")
        elif opt == "DELAY":
            lines.append(f'DigiKeyboard.delay({command.strip()});')
        elif opt == "ALT":
            lines.append(f'DigiKeyboard.sendKeyStroke(KEY_{command.upper().strip()}, MOD_ALT_LEFT);')
        elif opt == "CONTROL" or opt == "CTRL":
            lines.append(f'DigiKeyboard.sendKeyStroke(KEY_{command.upper().strip()}, MOD_CONTROL_LEFT);')

if f_delay:
    void_loop = void_loop + f'   DigiKeyboard.delay({f_delay});\n'         
for i, line in enumerate(lines):
    if i == len(lines) - 1:
        void_loop = void_loop + '   ' + line + '\n'
        void_loop = void_loop + '   for(;;){}\n'
        void_loop = void_loop + '}'
    else:
        void_loop = void_loop + '   ' + line + '\n'
for i, string in enumerate(strings):
    if i == len(strings) - 1:
        final_script = final_script + string + '\n'
        final_script = final_script + 'char buffer[66];\n' + '#define GetPsz( x ) (strcpy_P(buffer, (char*)x))\n\nvoid setup(){}\n' + void_loop
    else:
        final_script = final_script + string + '\n'
with open(w_file, 'w') as w_file:
    w_file.write(final_script)
print(f'{w_file.name} generated! \n')
print(f'The original script was: {str(len(open(r_file, "r").read()))} bytes.\n')
print(f'The generated script is: {str(len(final_script))} bytes.')