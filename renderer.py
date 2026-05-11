import os
from typing import List, Tuple


class Renderer:
    def __init__(self):
        self._clear_cmd = "cls" if os.name == "nt" else "clear"

    def clear_screen(self) -> None:
        os.system(self._clear_cmd)

    def render_board(self, snake_positions: List[Tuple[int, int]], food_position: Tuple[int, int], board_size: Tuple[int, int] = (20, 20)) -> None:
        snake_set = set(snake_positions)
        for y in range(board_size[1]):
            row = ""
            for x in range(board_size[0]):
                position = (x, y)
                if position == food_position:
                    row += "F"
                elif position in snake_set:
                    row += "O"
                else:
                    row += "."
            print(row)

    def render_score(self, score: int) -> None:
        print(f"Score: {score}")

    def render_game_over(self, final_score: int) -> None:
        print("\n" + "=" * 40)
        print("GAME OVER")
        print(f"Final Score: {final_score}")
        print("=" * 40)
        print("Press any key to restart or ESC to quit...")

    def render_difficulty_menu(self) -> None:
        print("\n" + "=" * 40)
        print("SNAKE GAME - Difficulty Selection")
        print("=" * 40)
        print("1. Easy (150ms)")
        print("2. Medium (100ms)")
        print("3. Hard (75ms)")
        print("4. Expert (50ms)")
        print("Press 1-4 to select difficulty:")
