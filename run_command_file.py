import sys
import timeit

from Arrable import Arrable as arbl
import QueryCommands as q
from CommandTextParser import parse

from QueryCommands import WherePredicates

obj_dict = {} # Stores Arrables with keys as name, e.g. R, S, T. 

def run(file_path, obj_dict, commands):
    
    while commands:
        command = commands.pop()
        interpreted_command = parse(command)
        time_command(interpreted_command, obj_dict)
            
            
def time_command(interpreted_command: str, obj_dict, trials=1, print_out=True):
    exec_string = f"'q.'+{interpreted_command}, globals(), {obj_dict}" # Literally execute the strings
    duration = timeit.timeit(lambda: exec(exec_string))
    if print_out: print(duration)

def garbage_collect_through_lookahead(obj_dict, future_commands):
    """
    Side effect of removing keys that are no longer in the future commands
    """
    
    obj_set = set(obj_dict.keys())
    still_to_use = set()
    
    for command in future_commands: 
        assigned_variable = command[0]
        still_to_use.add(assigned_variable)
    not_needed = obj_set - still_to_use
    needed = obj_set - not_needed
    for key in needed: 
        obj_dict.remove(key)

