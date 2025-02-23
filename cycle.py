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


parser = argparse.ArgumentParser(
    prog="Cycle List",
    description="A script that cycles through items in a list. It takes a list of items as input and prints each "
                "item in the list repeatedly, cycling back to the beginning once it reaches the end. It also "
                "supports a size parameter to limit the number of items to cycle through. Items in the list are "
                "shuffled randomly depending on which priority bucket they belong to."
)
parser.add_argument("-f", "--filename", default="url.json", nargs='?', type=str, const=1)
parser.add_argument("-s", "--size", default=86, nargs='?', type=int, const=1)

args = parser.parse_args()

previous = ["", ""]
start = time.time()


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


def remove_random_elements(arr, percentage):
    num_elements_to_remove = int(len(arr) * percentage / 100)
    indices_to_remove = random.sample(range(len(arr)), num_elements_to_remove)
    for index in sorted(indices_to_remove, reverse=True):
        del arr[index]
    return arr


def cycle(
    url,
    cycle_iteration,
    high_priority_items,
    normal_priority_items,
    low_priority_items,
    extra_items,
    total_iterations
):
    elapsed_time = time.time() - start
    if elapsed_time < 60:
        display_time = f"{elapsed_time:.2f} seconds"
    elif 3600 > elapsed_time > 60:
        display_time = f"{int(elapsed_time // 60)}:{int(elapsed_time % 60):02} minutes"
    else:
        display_time = f"{int(elapsed_time // 3600)}:{int((elapsed_time % 3600) // 60):02}:{int(elapsed_time % 60):02} hours"
    print(
        "\nstart", time.ctime(start), "\n",
        "\n  elapsed:", display_time,
        "\n\n  High:", high_priority_items,
        "   Normal:", normal_priority_items,
        "   Low:", low_priority_items,
        "   Extra:", extra_items,
        "\n\n  cycle:", cycle_iteration,
        "  iterations:", total_iterations,
        "\n\n\t up next: ", url,
        "\n\n\t current: ", previous[-1],
        "\n\n\t    prev: ", previous[-2],
        "\n\n  Press 'q' to quit."
        "\n\n  Press Any Key to Open...",
    )
    a = wait_key()
    previous.append(url)
    if a == "c":
        cls()
        return
    if a == "\x1b" or a == "q":
        exit(0)
    webbrowser.open(url, new=1, autoraise=True)
    time.sleep(1)
    cls()


c, h, n, l, i, e = 0, 0, 0, 0, 0, 0
while True:
    c += 1
    cls()
    with open(str(args.filename)) as json_file:
        data = json.load(json_file)
    priority1 = [[x, 'High'] for x in data["High Priority"]]
    priority2 = [[x, 'Normal'] for x in data["Normal Priority"]]
    priority3 = [[x, 'Low'] for x in data["Low Priority"]]
    random.shuffle(priority1)
    random.shuffle(priority2)
    random.shuffle(priority3)
    priority1 = remove_random_elements(priority1, 60)
    priority2 = remove_random_elements(priority2, 60)
    priority3 = remove_random_elements(priority3, 95)
    loop_list = priority1 + priority2 + priority3
    remove_random_elements(loop_list, args.size)
    loop_list += [[random.choice(data["Extra"]), "Extra"]]
    random.shuffle(loop_list)
    for page in tqdm(loop_list):
        cycle(page[0], c, h, n, l, e, i)
        if page[1] == 'High': h += 1
        if page[1] == 'Normal': n += 1
        if page[1] == 'Low': l += 1
        if page[1] == 'Extra': e += 1
        i += 1
    cls()
    print()
    print("\t\t\aCycle Complete!")
    time.sleep(2)

