import time
import threading
import webbrowser
import argparse
import random
import json
import os
# The standard `curses` module in Python is designed primarily for Unix-like systems
# and doesn't directly support Windows.
import curses

# pip install windows-curses

parser = argparse.ArgumentParser(
    prog="Cycle List",
    description="A script that cycles through items in a list. It takes a list of items as input and prints each "
                "item in the list repeatedly, cycling back to the beginning once it reaches the end. It also "
                "supports a size parameter to limit the number of items to cycle through. Items in the list are "
                "shuffled randomly depending on which priority bucket they belong to."
)
parser.add_argument("-f", "--filename", default="url.json", nargs='?', type=str, const=1)
parser.add_argument("-s", "--size", default=92, nargs='?', type=int, const=1)
args = parser.parse_args()


def background_update(stdscr, state):
    start_time = time.time()
    while True:
        stdscr.erase()
        elapsed_time = time.time() - start_time
        if elapsed_time < 60:
            display_time = f"{elapsed_time:.2f} s"
        elif elapsed_time < 3600:
            display_time = f"{int(elapsed_time / 60)}:{int(elapsed_time % 60):02} m"
        else:
            display_time = f"{elapsed_time / 3600:.2f} h"

        height, width = stdscr.getmaxyx()
        stdscr.addstr(height - 5, 1, f"Remaining: {state['remaining']:.2f}%")

        total = state['total']
        remaining = state['remaining']
        done = total - remaining
        bar_width = int(width * 0.8) - 2
        percent = int(done / (total if total != 0 else 1) * bar_width)
        bar = "█" * percent
        stdscr.addstr(0, 0, bar)

        stdscr.addstr(1, 2, f"start: {time.ctime(start_time)}")
        stdscr.addstr(3, 0,
          f" ┌─────────────┐\n"
          f" │ {display_time}\n"
          f" └─────────────┘"
        )
        stdscr.addstr(4, 15, "│")

        stdscr.addstr(7, 3, f"High: {state['high']}")
        stdscr.addstr(7, 15, f"Normal: {state['normal']}")
        stdscr.addstr(7, 30, f"Low: {state['low']}")
        stdscr.addstr(7, 41, f"Extra: {state['extra']}")

        stdscr.addstr(9, 3, f"cycle: {state['cycle']}")
        stdscr.addstr(9, 15, f"iterations: {state['iterations']}")

        stdscr.addstr(11, 11, f"up next: {state['history'][-1]}")
        stdscr.addstr(13, 11, f"current: {state['history'][-2]}")
        stdscr.addstr(15, 14, f"prev: {state['history'][-3]}")

        stdscr.addstr(17, 3, "Press 'q' to quit.")
        stdscr.addstr(19, 3, "Press Any Key to Open...")

        stdscr.refresh()
        time.sleep(0.01)


def remove_random_elements(arr, percentage):
    num_elements_to_remove = int(len(arr) * percentage / 100)
    indices_to_remove = random.sample(range(len(arr)), num_elements_to_remove)
    for index in sorted(indices_to_remove, reverse=True):
        del arr[index]
    return arr


def load_and_shuffle_data(filename, size):
    with open(filename) as json_file:
        data = json.load(json_file)
    priority1 = [[x, 'High'] for x in data["High Priority"]]
    priority2 = [[x, 'Normal'] for x in data["Normal Priority"]]
    priority3 = [[x, 'Low'] for x in data["Low Priority"]]
    random.shuffle(priority1)
    random.shuffle(priority2)
    random.shuffle(priority3)
    priority1 = remove_random_elements(priority1, 50)
    priority2 = remove_random_elements(priority2, 50)
    priority3 = remove_random_elements(priority3, 90)
    loop_list = priority1 + priority2 + priority3
    remove_random_elements(loop_list, size)
    loop_list += [[random.choice(data["Extra"]), "Extra"]]
    random.shuffle(loop_list)
    return data, loop_list


def main(stdscr):
    state = {
        'cycle': 0,
        'high': 0,
        'normal': 0,
        'low': 0,
        'extra': 0,
        'iterations': 0,
        'history': [" ", " ", " "],
        'remaining': 0.0,
        'total': 0
    }
    update_thread = threading.Thread(
        target=background_update,
        args=(stdscr, state),
        daemon=True
    )
    update_thread.start()
    try:
        while True:
            stdscr.clear()
            curses.curs_set(0)
            state['cycle'] += 1
            data, loop_list = load_and_shuffle_data(str(args.filename), args.size)
            state['total'] = len(loop_list)
            for i, page in enumerate(loop_list):
                remaining = state['total'] - (i + 1)
                state['remaining'] = (remaining / state['total']) * 100 if state['total'] > 0 else 0
                state['history'].append(page[0])
                if page[1] == 'High': state['high'] += 1
                if page[1] == 'Normal': state['normal'] += 1
                if page[1] == 'Low': state['low'] += 1
                if page[1] == 'Extra': state['extra'] += 1
                state['iterations'] += 1
                key = stdscr.getch()
                if key == ord('q'):
                    os._exit(0)
                elif key == curses.KEY_RESIZE:
                    height, width = stdscr.getmaxyx()
                    stdscr.addstr(height - 5, 1, f"Screen width: {width}, height: {height}")
                elif key == curses.KEY_DOWN:
                    state['history'].append(page[0])
                else:
                    webbrowser.open(page[0], new=1, autoraise=True)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    curses.wrapper(main)
