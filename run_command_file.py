import sys
import time

from Arrable import Arrable
import QueryCommands as q
from CommandTextParser import parse, interpret

from QueryCommands import WherePredicates

obj_dict = {} # Stores Arrables with keys as name, e.g. R, S, T. 

def run(commands, obj_dict):
    commands.reverse()
    while commands:
        pair = commands.pop()
        if len(pair) == 2:
            variable, value = pair
            value = interpret(value)
            to_run = f"obj_dict['{variable}'] = {value}"
            time_command(to_run)
            # garbage_collect_through_lookahead(obj_dict, commands)
        else: 
            singular = pair[0]
            variable, value = interpret(singular)
            to_run = f"obj_dict['{variable}'] = {value}"
            time_command(to_run)
            
def time_command(interpreted_command: str, trials=1, print_out=True, with_command=True):
    start = time.time()
    execcode(interpreted_command)
    end = time.time()
    if print_out:
        if with_command: print("{0:.4f}: {1}".format(end-start, interpreted_command))
        else: print("{0:.4f}".format(end-start))

def execcode(code_str: str):
    global obj_dict
    # print(code_str)
    glob_dict = {"obj_dict": obj_dict, "q": q, "Arrable": Arrable}
    exec(code_str, glob_dict)
    # print(glob_dict)

# def garbage_collect_through_lookahead(obj_dict, future_commands):
#     """
#     Has side effect of removing keys that are no longer in the future commands
#     """
#     obj_set = set(obj_dict.keys())
#     still_to_use = set()
#     for command in future_commands: 
#         assigned_variable = command[0]
#         still_to_use.add(assigned_variable)
#     not_needed = obj_set - still_to_use
#     for key in not_needed: 
#         obj_dict.remove(key)


if __name__ == "__main__":
    command_list = parse("test_commands1")
    run(command_list, obj_dict)