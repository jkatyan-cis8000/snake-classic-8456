from enum import Enum
from typing import List, Tuple, Set
from game_state import GameState


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class Snake:
    def __init__(self, start_position: Tuple[int, int] = (10, 10)):
        self.positions: List[Tuple[int, int]] = [start_position]
        self.direction = Direction.RIGHT
        self.grow_pending = False

    @property
    def head(self) -> Tuple[int, int]:
        return self.positions[0]

    def move(self) -> None:
        head = self.head
        dx, dy = self.direction.value
        new_head = (head[0] + dx, head[1] + dy)
        self.positions.insert(0, new_head)
        if not self.grow_pending:
            self.positions.pop()
        self.grow_pending = False

    def change_direction(self, new_direction: Direction) -> None:
        opposite = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
        }
        if new_direction != opposite.get(self.direction):
            self.direction = new_direction

    def grow(self) -> None:
        self.grow_pending = True

    def check_self_collision(self) -> bool:
        return self.head in self.positions[1:]

    def get_positions(self) -> Set[Tuple[int, int]]:
        return set(self.positions)


class GameEngine:
    def __init__(self, game_state: GameState, board_size: Tuple[int, int] = (20, 20)):
        self.game_state = game_state
        self.board_size = board_size
        self.snake = Snake((board_size[0] // 2, board_size[1] // 2))
        self.game_over = False
        self.score = 0
        self.game_started = False

    def start_game(self) -> None:
        self.game_state.spawn_food(self.snake.get_positions(), self.board_size)
        self.game_started = True
        self.game_over = False

    def update(self) -> None:
        if not self.game_started or self.game_over:
            return
        self.snake.move()
        self._check_collisions()
        self._check_food()

    def _check_collisions(self) -> None:
        head = self.snake.head
        x, y = head
        if x < 0 or x >= self.board_size[0] or y < 0 or y >= self.board_size[1]:
            self.game_over = True
        elif self.snake.check_self_collision():
            self.game_over = True

    def _check_food(self) -> None:
        if self.snake.head == self.game_state.food_position:
            self.snake.grow()
            self.game_state.update_score(10)
            self.game_state.spawn_food(self.snake.get_positions(), self.board_size)

    def is_game_over(self) -> bool:
        return self.game_over

    def get_score(self) -> int:
        return self.game_state.score

    def get_snake_positions(self) -> List[Tuple[int, int]]:
        return self.snake.positions

    def get_food_position(self) -> Tuple[int, int]:
        return self.game_state.food_position

    def change_direction(self, direction: Direction) -> None:
        if self.game_started and not self.game_over:
            self.snake.change_direction(direction)
