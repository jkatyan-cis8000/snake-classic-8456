from enum import Enum
from typing import Callable, Optional


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class InputHandler:
    def __init__(self):
        self._current_direction: Direction = Direction.RIGHT
        self._next_direction: Direction = Direction.RIGHT
        self._callback: Optional[Callable[[Direction], None]] = None

    def handle_input(self, key: str) -> None:
        key_lower = key.lower()
        key_map = {
            'w': Direction.UP,
            'a': Direction.LEFT,
            's': Direction.DOWN,
            'd': Direction.RIGHT,
            '\x1b[A': Direction.UP,
            '\x1b[B': Direction.DOWN,
            '\x1b[D': Direction.LEFT,
            '\x1b[C': Direction.RIGHT,
        }

        if key_lower in key_map:
            new_direction = key_map[key_lower]
        elif key in key_map:
            new_direction = key_map[key]
        else:
            return

        if self._validate_direction(new_direction):
            self._next_direction = new_direction
            if self._callback:
                self._callback(self._next_direction)

    def _validate_direction(self, new_direction: Direction) -> bool:
        opposite_directions = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }
        return opposite_directions.get(self._current_direction) != new_direction

    def listen_for_input(self, callback: Callable[[Direction], None]) -> None:
        self._callback = callback

    def update_direction(self) -> None:
        self._current_direction = self._next_direction

    def get_current_direction(self) -> Direction:
        return self._current_direction
