import argparse
from timeImplementation import time_run

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("command_file")

    args = p.parse_args()

    file_path = args.command_file

    time_run("hash", file_path)
    time_run("btree", file_path)
