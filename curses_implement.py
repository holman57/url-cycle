import time
import threading

# The standard `curses` module in Python is designed primarily for Unix-like systems
# and doesn't directly support Windows.
import curses
# pip install windows-curses


def background_update(stdscr):
    start_time = time.time()
    while True:
        # stdscr.clear()
        stdscr.erase()
        elapsed_time = time.time() - start_time
        if elapsed_time < 60:
            display_time = f"{elapsed_time:.2f} s"
        elif elapsed_time < 3600:
            display_time = f"{int(elapsed_time / 60)}:{int(elapsed_time % 60):02} m"
        else:
            display_time = f"{elapsed_time / 3600:.2f} h"

        stdscr.addstr(0, 0, "████ ██")
        stdscr.addstr(1, 2, f"start: {time.ctime(start_time)}")
        stdscr.addstr(3, 0,
            f" ┌─────────────┐\n"
            f" │ {display_time}\n"
            f" └─────────────┘"
        )
        stdscr.addstr(4, 15, "│")
        stdscr.addstr(7, 2, f"High:")
        stdscr.addstr(9, 2, f"cycle:")

        height, width = stdscr.getmaxyx()
        stdscr.addstr(15, 1, f"Screen width: {width}, height: {height}")

        stdscr.refresh()
        time.sleep(0.01)


def main(stdscr):
    stdscr.clear()
    curses.curs_set(0)  # Hide the cursor
    update_thread = threading.Thread(target=background_update, args=(stdscr,), daemon=True)
    update_thread.start()
    # Keep the main thread alive so the background thread can run
    try:
        while True:
            time.sleep(1)  # or curses.getch() to respond to key presses
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    curses.wrapper(main)
