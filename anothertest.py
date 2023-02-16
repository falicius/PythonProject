import asyncio
import curses
from curses import textpad, ascii
import datetime

class Prompt():
    def __init__(self, prompt_string='> '):
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.prompt_string = prompt_string
        self.output_window = None
        self.prompt_window = None
        self._initialize()
        self.rebuild_prompt()
        self.loop = asyncio.get_event_loop()
        # self.data = asyncio.Queue()
        self.task = asyncio.gather(self.get_time())
        self.loop.run_until_complete(self.task)


    def _initialize(self):
        max_y, max_x = self.screen.getmaxyx()
        self.output_window = self.screen.subwin(max_y - 1, max_x, 0, 0)
        self.prompt_window = curses.newwin(1, max_x, max_y - 1, 0)
        self.edit = textpad.Textbox(self.prompt_window, insert_mode=True)
        self.output_window.scrollok(True)
        self.prompt_window.scrollok(True)

    def rebuild_prompt(self, default_text=None):
        self.prompt_window.clear()
        self.prompt_window.addstr(self.prompt_string)
        if default_text:
            self.prompt_window.addstr(default_text)
        self.prompt_window.refresh()

    def _validate_input(self, key):
        if key == ord('\n'):
            return curses.ascii.BEL
        if key == 127:
            key = curses.KEY_BACKSPACE
        if key in (curses.ascii.STX, curses.KEY_LEFT, curses.ascii.BS, curses.KEY_BACKSPACE):
            minx = len(self.prompt_string)
            (y, x) = self.prompt_window.getyx()
            if x == minx:
                return None
        if key == curses.KEY_RESIZE:
            self.resize()
            return None
        return key

    def resize(self):
        max_y, max_x = self.screen.getmaxyx()
        self.output_window.resize(max_y - 1, max_x)
        self.prompt_window.resize(1, max_x)
        self.prompt_window.mvwin(max_y - 1, 0)
        self.output_window.refresh()
        self.prompt_window.refresh()

    def readline(self, handle_interrupt=True):
        self.prompt_window.keypad(1)
        try:
            self.input_string = self.edit.edit(self._validate_input)
            self.input_string = self.input_string[len(self.prompt_string):len(self.input_string) - 1]
        except KeyboardInterrupt:
            if handle_interrupt:
                return False
            else:
                raise KeyboardInterrupt
        self.rebuild_prompt()
        return True

    def addline(self, line):
        self.output_window.addstr(line + '\n')
        self.output_window.refresh()
        self.prompt_window.refresh()

    async def get_time(self):
        while True:
            now = datetime.datetime.now()
            today = now.today()
            today = str(today.strftime("%m-%d-%y"))
            current_time = str(now.strftime("%H-%M-%S"))
            test = "[" + today + " " + current_time + "]:"
            self.output_window.addline(test)
            await asyncio.sleep(1)













# def main(stdscr):
#     console = Prompt(stdscr)



if __name__ == '__main__':
    console = Prompt()