import time
import threading
from pynput import keyboard
from pynput.mouse import Button, Controller, Listener

delay = 0.03
button = Button.left
start_stop_key = '<alt>+s'
exit_key = '<alt>+e'

def line_print(msg):
    print(f'\r{msg}', end='')

class ClickMouse(threading.Thread):
    def __init__(self, delay, button):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True
        self.click_count = 0

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        print('Running auto-click service...')
        while self.program_running:
            while self.running:
                mouse.click(self.button)
                self.click_count = self.click_count + 1
                line_print(f'Clicks: {self.click_count}')
                time.sleep(self.delay)
            time.sleep(0.1)

mouse = Controller()
click_thread = ClickMouse(delay, button)
click_thread.start()

def start_stop():
    if click_thread.running:
        click_thread.stop_clicking()
    else:
        click_thread.start_clicking()

def stop_threads():
    click_thread.exit()
    raise Listener.StopException

with keyboard.GlobalHotKeys({start_stop_key:start_stop, exit_key: stop_threads}) as h:
    h.join()