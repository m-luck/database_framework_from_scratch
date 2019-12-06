import sys
import timeit

import Arrable as arbl
import QueryCommands as q
import CommandTextParser as p

from QueryCommands import WherePredicates

obj_dict = {} # Stores Arrables with keys as name, e.g. R, S, T. 

def run(file_path, obj_dict):
    
    with open(file_path, "r") as commands:
        for command in commands:
            interpreted_command = p.parse_command(command)
            time_command(interpreted_command, obj_dict)
            
            
def time_command(interpreted_command: str, obj_dict, trials=1, print_out=True):
    exec_string = f"'q.'+{interpreted_command}, globals(), {obj_dict}" # Literally execute the strings
    duration = timeit.timeit(lambda: exec(exec_string))
    if print_out: print(duration)
    
            
