import random
import webbrowser
import os
import time
import sys
from tqdm import tqdm
import json
import argparse


def cls():
    os.system("cls" if os.name == "nt" else "clear")


def wait_key():
    result = None
    if os.name == "nt":
        import msvcrt

        result = msvcrt.getwch()
    else:
        import termios

        fd = sys.stdin.fileno()
        old_term = termios.tcgetattr(fd)
        new_attr = termios.tcgetattr(fd)
        new_attr[3] = new_attr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, new_attr)
        try:
            result = sys.stdin.read(1)
        except IOError:
            pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)
    return result


def cycle(url, cycle_iteration, high_priority_items, total_iterations):
    print(
        "\n\n\t\t\t     High Priority Items:",
        high_priority_items,
        "\n\tcycle:",
        cycle_iteration,
        "\t\tTotal Iterations:",
        total_iterations,
        "\n\n\t",
        url,
        "\n\n\n\t\tPress Any Key...",
    )
    a = wait_key()
    if a == "\x1b" or a == "q":
        exit(0)
    webbrowser.open(url, new=1, autoraise=True)
    cls()


c = 0
while True:
    c += 1
    cls()
    parser = argparse.ArgumentParser(prog="Cycle List", description="!", epilog="_")
    parser.add_argument("filename")
    args = parser.parse_args()
    print(args.filename)
    with open(str(args.filename)) as json_file:
        data = json.load(json_file)
    priority1 = [x for x in data["High Priority"]]
    priority2 = [x for x in data["Normal Priority"]]
    priority3 = [x for x in data["Low Priority"]]
    random.shuffle(priority1)
    random.shuffle(priority2)
    random.shuffle(priority3)
    loop_list = priority2 + priority3
    h, i = 0, 0
    for page in tqdm(loop_list):
        if i % 2 == 0:
            if len(priority1) == 0:
                priority1 = [x for x in data["High Priority"]]
                random.shuffle(priority1)
            h += 1
            random_priority1 = priority1.pop(0)
            cycle(random_priority1, c, h, i)
        i += 1
        cycle(page, c, h, i)
    cls()
    print()
    print("\t\t\aCycle Complete!")
    time.sleep(2)
