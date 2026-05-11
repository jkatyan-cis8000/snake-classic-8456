#!/usr/bin/env python3
"""
Classic Snake Game - Main Entry Point

This module orchestrates all game components and runs the main game loop.
It provides difficulty selection, game initialization, and game restart capability.
"""

import sys
import time
from typing import Optional

from game_engine import GameEngine, Direction
from game_state import GameState, Difficulty
from input_handler import InputHandler
from renderer import Renderer


class SnakeGame:
    """Main game class that orchestrates all components."""

    def __init__(self):
        self.game_state: Optional[GameState] = None
        self.game_engine: Optional[GameEngine] = None
        self.input_handler = InputHandler()
        self.renderer = Renderer()
        self.difficulty: Optional[Difficulty] = None
        self.running = True

    def select_difficulty(self) -> bool:
        """Display difficulty menu and return True if a valid selection was made."""
        self.renderer.clear_screen()
        self.renderer.render_difficulty_menu()

        key = self.input_handler.get_key()

        difficulty_map = {
            '1': Difficulty.EASY,
            '2': Difficulty.MEDIUM,
            '3': Difficulty.HARD,
            '4': Difficulty.EXPERT,
            '\x1b[A': None,  # Arrow up - no action
            '\x1b[B': None,  # Arrow down - no action
            '\x1b[C': None,  # Arrow right - no action
            '\x1b[D': None,  # Arrow left - no action
        }

        selected = difficulty_map.get(key)
        if selected is not None:
            self.difficulty = selected
            return True
        elif key in ('q', 'Q', '\x1b'):  # ESC or Q to quit
            return False

        # Invalid selection, wait briefly and show menu again
        time.sleep(0.2)
        return self.select_difficulty()

    def initialize_game(self) -> bool:
        """Initialize game state and engine with selected difficulty."""
        if self.difficulty is None:
            return False

        self.game_state = GameState(difficulty=self.difficulty)
        self.game_engine = GameEngine(self.game_state, board_size=(20, 20))
        self.game_engine.start_game()
        return True

    def process_input(self, key: str) -> None:
        """Process keyboard input and update game direction."""
        direction_map = {
            'w': Direction.UP,
            's': Direction.DOWN,
            'a': Direction.LEFT,
            'd': Direction.RIGHT,
            '\x1b[A': Direction.UP,    # Arrow up
            '\x1b[B': Direction.DOWN,  # Arrow down
            '\x1b[C': Direction.RIGHT, # Arrow right
            '\x1b[D': Direction.LEFT,  # Arrow left
        }

        direction = direction_map.get(key)
        if direction:
            self.game_engine.change_direction(direction)

    def run_game_loop(self) -> bool:
        """
        Run the main game loop.
        Returns True if game should restart, False otherwise.
        """
        speed = self.game_state.speed

        while self.running:
            # Clear screen
            self.renderer.clear_screen()

            # Render current state
            self.renderer.render_board(
                self.game_engine.get_snake_positions(),
                self.game_engine.get_food_position(),
                (20, 20)
            )
            self.renderer.render_score(self.game_engine.get_score())

            # Check if game over
            if self.game_engine.is_game_over():
                self.renderer.render_game_over(self.game_engine.get_score())
                key = self.input_handler.get_key()

                if key == '\x1b':  # ESC to quit
                    return False
                else:  # Any other key to restart
                    return True

            # Input handling with non-blocking read
            import select
            if select.select([sys.stdin], [], [], 0)[0]:
                key = self.input_handler.get_key()
                self.process_input(key)

            # Game update
            self.game_engine.update()

            # Wait for next frame (difficulty-based speed)
            time.sleep(speed / 1000.0)

        return False

    def restart_game(self) -> None:
        """Reset game state for a new game."""
        self.running = True

    def run(self) -> None:
        """Main entry point - runs the complete game."""
        while True:
            # Difficulty selection
            if not self.select_difficulty():
                break

            # Initialize game
            if not self.initialize_game():
                break

            # Run game loop
            should_restart = self.run_game_loop()

            if not should_restart:
                break

            # Reset for next game
            self.restart_game()
            self.game_engine = None
            self.game_state = None

        self.renderer.clear_screen()
        print("Thanks for playing Snake!")


def main():
    """Entry point for the game."""
    try:
        game = SnakeGame()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
