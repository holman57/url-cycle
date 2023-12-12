import random
import webbrowser
import os
import time
import sys
from tqdm import tqdm


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def wait_key():
    result = None
    if os.name == 'nt':
        import msvcrt
        result = msvcrt.getwch()
    else:
        import termios
        fd = sys.stdin.fileno()
        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)
        try:
            result = sys.stdin.read(1)
        except IOError: pass
        finally: termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    return result


while True:
    cls()
    data = [line.strip() for line in open(r"C:\Users\LukeH\Desktop\url.list", 'r')]
    for line in data: 
        print(line)
        time.sleep(random.randint(9, 9999) * 0.000001)
    time.sleep(random.randint(0, 1))
    cls()
    random.shuffle(data)
    
    for line in data: 
        print(line)
        time.sleep(random.randint(9, 9999) * 0.000001)
    time.sleep(random.randint(1, 3))
    cls()
    for page in tqdm(data):
        print()
        print()
        print("\t", page)
        print()
        print()
        print()
        print("\t\tPress Any Key...")
        a = wait_key()
        if a == '\x1b': exit(0)
        if a == 'q': exit(0)
        webbrowser.open(page)
        cls()
        continue
    cls()
    print()
    print("\t\tCycle Complete!")
    time.sleep(2)


