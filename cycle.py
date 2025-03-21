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

DEFAULT_FILENAME = "url.json"
DEFAULT_SIZE = 93

parser = argparse.ArgumentParser(
    prog="Cycle List",
    description="A script that cycles through items in a list. It takes a list of items as input and prints each "
                "item in the list repeatedly, cycling back to the beginning once it reaches the end. It also "
                "supports a size parameter to limit the number of items to cycle through. Items in the list are "
                "shuffled randomly depending on which priority bucket they belong to."
)
parser.add_argument("filename", nargs="?", default=DEFAULT_FILENAME, type=str,
                    help="Name of the file to read")
parser.add_argument("size", nargs="?", default=DEFAULT_SIZE, type=int,
                    help="Number of items to cycle through")
parser.add_argument("-f", "--file", action="store_true", help="Name of the JSON file for the list")
parser.add_argument("-s", "--size", action="store_true", help="Size of the probability distribution")

args = parser.parse_args()


def display_progress_bar(stdscr, state, width):
    bar_length = int((width + 1) / state['total']) if state['total'] > 0 else 0
    bar = "█" * bar_length * state['position']
    stdscr.addstr(0, 0, bar)


def display_state(stdscr, state):
    stdscr.erase()
    if state['timer'] == 1:
        elapsed_time = time.time() - state['start_time'] - state['paused_time_total']
    else:
        elapsed_time = state['elapsed_time']
    display_time = f"{elapsed_time:.2f} s" if elapsed_time < 60 else \
        f"{int(elapsed_time / 60)}:{int(elapsed_time % 60):02} m" if elapsed_time < 3600 else \
            f"{int(elapsed_time / 3600) :02}:{int((elapsed_time % 3600) / 60):02}:{int(elapsed_time % 60):02} h"
    height, width = stdscr.getmaxyx()
    display_progress_bar(stdscr, state, width)
    stdscr.addstr(1, 2, f"start: {time.ctime(state['start_time'])}")
    stdscr.addstr(3, 0, f" ┌─────────────┐\n │ {display_time}\n └─────────────┘")
    stdscr.addstr(4, 15, "│" + ("" if state['timer'] == 1 else " * Paused"))
    stdscr.addstr(7, 3, f"High: {state['high']}")
    stdscr.addstr(7, 15, f"Normal: {state['normal']}")
    stdscr.addstr(7, 30, f"Low: {state['low']}")
    stdscr.addstr(7, 41, f"Extra: {state['extra']}")
    stdscr.addstr(9, 3, f"cycle: {state['cycle']}")
    stdscr.addstr(9, 15, f"iterations: {state['iterations']}")
    stdscr.addstr(11, 11, f"up next: {state['history'][state['history_index']] if state['history_index'] > -1 and len(state['history']) > 0 else ' '}")
    stdscr.addstr(13, 11, f"current: {state['history'][-2] if state['history_index'] > 0 and len(state['history']) > 1 else ' '}")
    stdscr.addstr(15, 14, f"prev: {state['history'][-3] if state['history_index'] > 1 and len(state['history']) > 2 else ' '}")
    stdscr.addstr(17, 5, "'q' to Quit")
    stdscr.addstr(18, 5, "'p' to Pause")
    stdscr.addstr(19, 5, "Any Key to Open...")
    # stdscr.addstr(23, 3, f"history len: {len(state['history'])}")
    # stdscr.addstr(24, 3, f"position: {(state['cycle'] - 1) * state['total'] + state['position']}")
    # stdscr.addstr(25, 3, f"history index: {state['history_index']}")
    if state['timer'] == 1:
        state['elapsed_time'] = elapsed_time
    else:
        state['paused_time'] = time.time() - state['paused_start_time']
    stdscr.refresh()


def background_update(stdscr, state):
    state['start_time'] = time.time()
    while True:
        display_state(stdscr, state)
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
    loop_list += [[random.choice(data["Low Priority"]), "Low"]]
    random.shuffle(loop_list)
    return data, loop_list


def resume_timer(state):
    if state['timer'] == 0:
        state['paused_time_total'] += state['paused_time']
    state['timer'] = 1


def update_state(state, page):
    state['position'] = state.get('position', 0) + 1
    state['remaining'] = (state['total'] - state['position']) / state['total'] * 100 if state['total'] > 0 else 0
    state['history'].append(page[0])
    state[page[1].lower()] = state.get(page[1].lower(), 0) + 1
    state['iterations'] += 1


def update_history(state, page):
    if len(state['history']) == (state['cycle'] - 1) * state['total'] + state['position']:
        webbrowser.open(page[0], new=1, autoraise=True)
        state['history_index'] += 1
    else:
        webbrowser.open(state['history'][state['history_index']], new=1, autoraise=True)
        state['history'] = state['history'][:state['history_index']]
    resume_timer(state)


def main(stdscr):
    state = {
        'cycle': 0,
        'high': 0,
        'normal': 0,
        'low': 0,
        'extra': 0,
        'iterations': 0,
        'history': [],
        'remaining': 0.0,
        'total': 0,
        'position': 0,
        'history_index': 0,
        'timer': 1,
        'elapsed_time': 0.0,
        'start_time': 0.0,
        'paused_time': 0.0,
        'paused_start_time': 0.0,
        'paused_time_total': 0.0,
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
            state['position'] = 0
            for i, page in enumerate(loop_list):
                update_state(state, page)
                while True:
                    key = stdscr.getch()
                    if key == ord('q'):
                        os._exit(0)
                    elif key == ord('p'):
                        if state['timer'] == 1:
                            state['timer'] = 0
                            state['paused_start_time'] = time.time()
                        elif state['timer'] == 0:
                            resume_timer(state)
                        continue
                    elif key == curses.KEY_RESIZE:
                        continue
                    elif key == curses.KEY_DOWN:
                        if len(state['history']) != state['history_index']:
                            state['history_index'] += 1
                        else:
                            resume_timer(state)
                            break
                    elif key == curses.KEY_UP:
                        if state['history_index'] > 0:
                            state['history_index'] -= 1
                    elif key != curses.KEY_RESIZE:
                        update_history(state, page)
                        break
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    curses.wrapper(main)
