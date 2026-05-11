import sys
import termios
import tty
from typing import Callable


class InputHandler:
    def __init__(self):
        self._fd = sys.stdin.fileno()
        self._old_settings = None

    def _init_terminal(self) -> None:
        self._old_settings = termios.tcgetattr(self._fd)
        tty.setcbreak(self._fd)

    def _restore_terminal(self) -> None:
        if self._old_settings:
            termios.tcsetattr(self._fd, termios.TCSADRAIN, self._old_settings)

    def get_key(self) -> str:
        self._init_terminal()
        try:
            ch = sys.stdin.read(1)
            if ch == "\x1b":
                ch += sys.stdin.read(2)
                return ch
            return ch
        finally:
            self._restore_terminal()

    def listen_for_input(self, callback: Callable[[str], None]) -> None:
        key = self.get_key()
        callback(key)
