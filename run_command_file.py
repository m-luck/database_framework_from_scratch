import sys
import timeit

from Arrable import Arrable as arbl
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
            time_command(f"obj_dict['{variable}'] = {value}", obj_dict)
            # garbage_collect_through_lookahead(obj_dict, commands)
        else: 
            singular = pair[0]
            variable, value = interpret(singular)
            time_command(f"obj_dict['{variable}'] = {value}", obj_dict)
                
            
def time_command(interpreted_command: str, obj_dict, trials=1, print_out=True):
    print(interpreted_command)
    exec_string = f"\"{interpreted_command}\", globals(), {obj_dict}" # Literally execute the strings
    duration = timeit.timeit(lambda: exec(exec_string), number=trials)
    if print_out: print(duration)

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