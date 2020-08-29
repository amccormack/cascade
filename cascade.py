#!/usr/bin/env python3

import argparse
import subprocess
from typing import List 

def get_window_ids() -> List[int]:
    command = 'xdotool search --onlyvisible --classname .'
    unparsed = subprocess.check_output(command, shell=True).decode('utf-8')
    return [int(line) for line in unparsed.split('\n') if line]

def get_display_shape() -> (int, int):
    '''Get width, height.'''
    command = 'xwininfo -root -shape'
    unparsed = subprocess.check_output(command, shell=True).decode('utf-8')
    width_line = [
        line for line in unparsed.split('\n') if line and 'width: ' in line.lower()
    ][0].strip().split(' ')[-1]
    height_line = [
        line for line in unparsed.split('\n') if line and 'height: ' in line.lower()
    ][0].strip().split(' ')[-1]
    return int(width_line), int(height_line)

def move_window(window_id, x, y, sync=False):
    command = 'xdotool windowmove {sync:s} {window_id:d} {x:d} {y:d}'.format(
        window_id=window_id, x=x, y=y, sync='--sync' if sync else '')
    subprocess.check_output(command, shell=True)
    

def cascade_left(x_advance=10, y_advance=40):
    window_ids = get_window_ids()
    x = 0 
    y = 0 
    for wid in window_ids:
        move_window(wid, x, y, True)
        x += x_advance
        y += y_advance

def cascade_right(x_advance=10, y_advance=10):
    window_ids = get_window_ids()
    width, _ = get_display_shape()
    x = width // 2
    y = 0 
    for wid in window_ids:
        move_window(wid, x, y, True)
        x += x_advance
        y += y_advance

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--right', help='Cascade on "right" side of screen', action='store_true')
    args = parser.parse_args()
    if args.right:
        cascade_right()
    else:
        cascade_left()

