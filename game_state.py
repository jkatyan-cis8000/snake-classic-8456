from enum import Enum
from typing import Tuple, Set
import random


class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class GameState:
    def __init__(self, difficulty: Difficulty = Difficulty.MEDIUM):
        self.difficulty = difficulty
        self.score = 0
        self.food_position: Tuple[int, int] = (0, 0)
        self._speed_map = {
            Difficulty.EASY: 150,
            Difficulty.MEDIUM: 100,
            Difficulty.HARD: 75,
            Difficulty.EXPERT: 50,
        }

    @property
    def speed(self) -> int:
        return self._speed_map[self.difficulty]

    def spawn_food(self, snake_positions: Set[Tuple[int, int]], board_size: Tuple[int, int] = (20, 20)) -> None:
        while True:
            x = random.randint(0, board_size[0] - 1)
            y = random.randint(0, board_size[1] - 1)
            position = (x, y)
            if position not in snake_positions:
                self.food_position = position
                break

    def update_score(self, points: int = 1) -> None:
        self.score += points

    def set_difficulty(self, difficulty: Difficulty) -> None:
        self.difficulty = difficulty
