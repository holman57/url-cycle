import random
import webbrowser
import os
import time
import sys
from tqdm import tqdm
import json
import argparse
if os.name == "nt":
    import msvcrt
else:
    import termios


parser = argparse.ArgumentParser(prog="Cycle List", description="!", epilog="_")
parser.add_argument("-f", "--filename", default="full.json", nargs='?', type=str, const=1)
parser.add_argument("-p", "--priority", default=0, nargs='?', type=int, const=1)
args = parser.parse_args()


def cls():
    os.system("cls" if os.name == "nt" else "clear")


def wait_key():
    result = None
    if os.name == "nt":
        result = msvcrt.getwch()
    else:
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
    if args.priority == 0:
        print(
            "\n\n\t\t\t     High Priority Items:",
            high_priority_items
        )
    print(
        "\n\tcycle:",
        cycle_iteration,
        "\t\tTotal Iterations:",
        total_iterations,
        "\n\n\t",
        url,
        "\n\n\n\t\tPress Any Key...",
    )
    a = wait_key()
    if a == "c":
        cls()
        return
    if a == "\x1b" or a == "q":
        exit(0)
    webbrowser.open(url, new=1, autoraise=True)
    cls()


c, h, i = 0, 0, 0
while True:
    c += 1
    cls()
    with open(str(args.filename)) as json_file:
        data = json.load(json_file)
    priority1 = [x for x in data["High Priority"]]
    priority2 = [x for x in data["Normal Priority"]]
    priority3 = [x for x in data["Low Priority"]]
    random.shuffle(priority1)
    random.shuffle(priority2)
    random.shuffle(priority3)
    loop_list = []
    if args.priority == 1:
        loop_list = priority1
    elif args.priority == 2:
        loop_list = priority2
    elif args.priority == 3:
        loop_list = priority3
    else:
        loop_list = priority1 + priority2 + priority3
    for page in tqdm(loop_list):
        if args.priority == 0:
            if i < len(priority1) - 1:
                h += 1
            else:
                if i % 4 == 0:
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



