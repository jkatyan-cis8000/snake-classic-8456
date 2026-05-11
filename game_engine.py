"""Core game engine module for the Snake game.

This module provides the fundamental game logic including:
- Direction enum for snake movement
- Snake class for managing snake position, direction, and growth
- GameEngine class for handling game loop, collision detection, and food consumption
"""

from enum import Enum
from typing import List, Tuple, Optional


class Direction(Enum):
    """Direction enum representing the four possible movement directions."""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def __init__(self, dx: int, dy: int):
        self.dx = dx
        self.dy = dy

    def opposite(self) -> 'Direction':
        """Return the opposite direction."""
        opposite_map = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        return opposite_map[self]


class Snake:
    """Snake class managing snake position, direction, and growth.

    The snake is represented as a list of coordinates [(x, y), ...]
    where the head is at index 0.
    """

    def __init__(self, initial_position: Tuple[int, int]):
        """Initialize the snake with a starting position.

        Args:
            initial_position: The (x, y) coordinate for the snake's head.
        """
        self._body: List[Tuple[int, int]] = [initial_position]
        self._direction: Direction = Direction.RIGHT
        self._next_direction: Direction = Direction.RIGHT
        self._grow_pending: bool = False

    @property
    def body(self) -> List[Tuple[int, int]]:
        """Return a copy of the snake's body coordinates."""
        return self._body.copy()

    @property
    def head(self) -> Tuple[int, int]:
        """Return the snake's head position."""
        return self._body[0]

    @property
    def direction(self) -> Direction:
        """Return the current movement direction."""
        return self._direction

    def change_direction(self, new_direction: Direction) -> bool:
        """Change the snake's direction.

        Prevents 180-degree turns (reversing direction).

        Args:
            new_direction: The desired direction to move.

        Returns:
            True if direction was changed, False if ignored.
        """
        if new_direction != self._direction.opposite():
            self._next_direction = new_direction
            return True
        return False

    def move(self) -> bool:
        """Move the snake one step in the current direction.

        Returns:
            True if move was successful, False if collision detected.
        """
        self._direction = self._next_direction
        dx, dy = self._direction.dx, self._direction.dy
        head_x, head_y = self._body[0]
        new_head = (head_x + dx, head_y + dy)

        if self._check_collision_with_self(new_head):
            return False

        self._body.insert(0, new_head)

        if not self._grow_pending:
            self._body.pop()
        else:
            self._grow_pending = False

        return True

    def grow(self) -> None:
        """Mark the snake to grow on the next move."""
        self._grow_pending = True

    def _check_collision_with_self(self, position: Tuple[int, int]) -> bool:
        """Check if a position collides with the snake's body.

        Args:
            position: The (x, y) position to check.

        Returns:
            True if position collides with body, False otherwise.
        """
        return position in self._body[1:]


class GameEngine:
    """Game engine class handling game loop, collision detection, and food consumption."""

    def __init__(self, board_width: int = 20, board_height: int = 20):
        """Initialize the game engine.

        Args:
            board_width: Width of the game board.
            board_height: Height of the game board.
        """
        self._board_width = board_width
        self._board_height = board_height
        self._snake = Snake((board_width // 2, board_height // 2))
        self._food: Optional[Tuple[int, int]] = None
        self._game_over: bool = False
        self._score: int = 0
        self._food_spawned: bool = False

    @property
    def snake(self) -> Snake:
        """Return the snake instance."""
        return self._snake

    @property
    def food(self) -> Optional[Tuple[int, int]]:
        """Return the current food position."""
        return self._food

    @property
    def score(self) -> int:
        """Return the current score."""
        return self._score

    @property
    def game_over(self) -> bool:
        """Return True if the game has ended."""
        return self._game_over

    @property
    def board_width(self) -> int:
        """Return the board width."""
        return self._board_width

    @property
    def board_height(self) -> int:
        """Return the board height."""
        return self._board_height

    def start_game(self) -> None:
        """Start a new game."""
        self._snake = Snake((self._board_width // 2, self._board_height // 2))
        self._food = None
        self._game_over = False
        self._score = 0
        self._food_spawned = False
        self._spawn_food()

    def update(self) -> bool:
        """Update the game state.

        Moves the snake, checks for collisions, and handles food consumption.

        Returns:
            True if game continues, False if game over.
        """
        if self._game_over:
            return False

        if not self._snake.move():
            self._game_over = True
            return False

        if self._check_collision_with_wall(self._snake.head):
            self._game_over = True
            return False

        if self._snake.head == self._food:
            self._snake.grow()
            self._score += 1
            self._spawn_food()

        return True

    def change_direction(self, direction: Direction) -> bool:
        """Change the snake's direction.

        Args:
            direction: The new direction to move.

        Returns:
            True if direction was changed, False otherwise.
        """
        return self._snake.change_direction(direction)

    def _check_collision_with_wall(self, position: Tuple[int, int]) -> bool:
        """Check if a position collides with the board walls.

        Args:
            position: The (x, y) position to check.

        Returns:
            True if position is outside board bounds, False otherwise.
        """
        x, y = position
        return x < 0 or x >= self._board_width or y < 0 or y >= self._board_height

    def _spawn_food(self) -> None:
        """Spawn food at a random position not occupied by the snake."""
        while True:
            import random
            x = random.randint(0, self._board_width - 1)
            y = random.randint(0, self._board_height - 1)
            position = (x, y)

            if position not in self._snake.body:
                self._food = position
                break
