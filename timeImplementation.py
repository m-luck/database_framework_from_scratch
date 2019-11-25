import argparse
import timeit
from typing import List

from BasicDatabase import BasicDatabase
from HashStructureImplementation import HashStructureImplementation
from BTreeImplementation import BTreeImplementation

db = None
trials = 10**5

def load_db(implementation: BasicDatabase):
    """
    Preload the database.
    """

    truth = {}
    global db
    db = implementation()
    with open("myindex.txt", "r") as f:
        for line in f:
            key, val = line.split("|")
            if key[0].isdigit():
                truth[int(key)] = int(val)
                db.insert(int(key), int(val))
    return db

def command_suite(db: BasicDatabase, commands: List):
    """
    Run all the dynamic commands.
    """
    ldict = {'db':db} # For use in exec (local variables)
    for command in commands:
        exec('db.'+command, globals(), ldict) # Literally execute the strings

def command_suite_out(db: BasicDatabase, commands: List, output_file: str):
    """
    Run all the dynamic commands.
    """
    ldict = {'db':db}
    with open(output_file, "w+") as f:
        f.write("Original:\n")
        f.write(str(db.records)+"\n\n")
        for command in commands:
            exec('db.'+command, globals(), ldict) 
            f.write("After "+command+":\n")
            f.write(str(db.records)+"\n\n")

def time_run(implStructure: str, commands_path: str):
    """
    Times the commands.
    """

    global db # Global for use in timeit setup imports

    # Take in the commands from the file.
    global commands
    with open(commands_path, "r") as f:
        commands = [line.strip('\n') for line in f] 
    print('Commands to run:', commands)

    if implStructure == "hash":
        db = load_db(HashStructureImplementation)
        duration = timeit.timeit(stmt="command_suite(db, commands)", setup="from timeImplementation import command_suite, db, commands", number=trials)

        db = load_db(HashStructureImplementation)
        command_suite_out(db, commands, 'logs_hash.txt')

    elif implStructure == "btree":
        db = load_db(BTreeImplementation)
        duration = timeit.timeit(stmt="command_suite(db, commands)", setup="from timeImplementation import command_suite, db, commands", number=trials)

        db = load_db(BTreeImplementation)
        command_suite_out(db, commands, 'logs_btree.txt')

    else:
        print("Please supply a valid implementation flag (e.g. hash or btree).")
        exit()

    print('Average total time taken for all commands:',"{0:.4f} ms".format(1000 * duration / trials))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("implementation")
    p.add_argument("commands_file_path")

    args = p.parse_args()

    implStructure = args.implementation 
    commands_path = args.commands_file_path
    time_run(implStructure, commands_path)