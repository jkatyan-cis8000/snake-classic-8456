import sys
import time
import threading
from game_engine import GameEngine, Direction, Snake
from game_state import GameState, Difficulty
from input_handler import InputHandler
from renderer import Renderer


class Game:
    def __init__(self):
        self.renderer = Renderer()
        self.input_handler = InputHandler()
        self.game_state = None
        self.game_engine = None
        self.running = False
        self.difficulty = Difficulty.MEDIUM
        self._input_thread = None

    def initialize_game(self, difficulty: Difficulty = None) -> None:
        if difficulty:
            self.difficulty = difficulty
        self.game_state = GameState(self.difficulty)
        self.game_engine = GameEngine(self.game_state)
        self.game_engine.start_game()
        self.running = True

    def _handle_input(self) -> None:
        while self.running and not self.game_engine.is_game_over():
            key = self.input_handler.get_key()
            if key == "\x1b[A":
                self.game_engine.change_direction(Direction.UP)
            elif key == "\x1b[B":
                self.game_engine.change_direction(Direction.DOWN)
            elif key == "\x1b[C":
                self.game_engine.change_direction(Direction.RIGHT)
            elif key == "\x1b[D":
                self.game_engine.change_direction(Direction.LEFT)
            elif key == "\x1b":
                self.running = False

    def game_loop(self) -> None:
        self._input_thread = threading.Thread(target=self._handle_input, daemon=True)
        self._input_thread.start()

        speed = self.game_state.speed / 1000.0

        while self.running and not self.game_engine.is_game_over():
            self.renderer.clear_screen()
            self.renderer.render_score(self.game_engine.get_score())
            self.renderer.render_board(
                self.game_engine.get_snake_positions(),
                self.game_engine.get_food_position()
            )
            self.game_engine.update()
            time.sleep(speed)

        self.renderer.clear_screen()
        self.renderer.render_game_over(self.game_engine.get_score())

    def restart_game(self) -> None:
        self.initialize_game(self.difficulty)
        self.game_loop()

    def run(self) -> None:
        while True:
            self.renderer.clear_screen()
            self.renderer.render_difficulty_menu()
            key = self.input_handler.get_key()

            if key == "1":
                difficulty = Difficulty.EASY
                break
            elif key == "2":
                difficulty = Difficulty.MEDIUM
                break
            elif key == "3":
                difficulty = Difficulty.HARD
                break
            elif key == "4":
                difficulty = Difficulty.EXPERT
                break
            elif key in ("\x1b", "\x03"):
                print("Goodbye!")
                return

        self.initialize_game(difficulty)
        self.game_loop()

        while True:
            key = self.input_handler.get_key()
            if key == "\x1b":
                break
            else:
                self.restart_game()
                break


def main() -> None:
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
