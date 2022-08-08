import time
import threading
import argparse
from pynput import keyboard
from pynput.mouse import Button, Controller, Listener

class MouseClickerThread(threading.Thread):
    def __init__(self, button, delay):
        super(MouseClickerThread, self).__init__()
        self.name = f'MouseClicker({button}) thread'
        self.delay = delay
        self.button = button
        self.clicking = False
        self.thread_running = True
        self.click_count = 0
        self.thread_sleep = 0.1
        self.mouse_controller = Controller()

    def toggle_clicking(self):
        self.clicking = not self.clicking

    def exit(self):
        if self.click_count > 0: print('')
        print(f'Stopping {self.name}...')
        self.clicking = False
        self.thread_running = False
        raise Listener.StopException

    def run(self):
        print(f'Starting {self.name}...')
        while self.thread_running:
            while self.clicking:
                self.mouse_controller.click(self.button)
                self.click_count = self.click_count + 1
                print(f'\rClicks: {self.click_count}', end='')
                time.sleep(self.delay)
            time.sleep(self.thread_sleep)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-tk", "--toggle-key", default='<alt>+s',  metavar='TEXT', help="Key combination used to toggle clicking (default: %(default)s)")
    parser.add_argument("-ek", "--exit-key", default='<alt>+e',  metavar='TEXT', help="Key combination used to terminate program (default: %(default)s)")
    parser.add_argument("-d", "--delay", type=float, default=0.03,  metavar='NUMBER', help="Delay between key presses in seconds (default: %(default)s)")
    args = parser.parse_args()

    clicker_thread = MouseClickerThread(Button.left, args.delay)
    clicker_thread.start()
    with keyboard.GlobalHotKeys({
        args.toggle_key: clicker_thread.toggle_clicking, 
        args.exit_key: clicker_thread.exit
    }) as h:
        print(f'Start/Stop key: {args.toggle_key}')
        print(f'Terminate key: {args.exit_key}')
        h.join()
    print('Stopped successfully')
