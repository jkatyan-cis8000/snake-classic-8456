class Renderer:
    """Renders the game state to the console using ASCII characters."""

    def __init__(self, board_size: tuple[int, int] = (20, 20)):
        self.board_size = board_size

    def render_board(self, snake_positions: set[tuple[int, int]], food_position: tuple[int, int]) -> None:
        """Draw the game grid with snake and food."""
        board_width, board_height = self.board_size
        snake_set = set(snake_positions)

        print("+" + "-" * board_width + "+")

        for y in range(board_height):
            row = "|"
            for x in range(board_width):
                position = (x, y)
                if position in snake_set:
                    if position == snake_positions[0]:
                        row += "@"  # Snake head
                    else:
                        row += "#"  # Snake body
                elif position == food_position:
                    row += "O"  # Food
                else:
                    row += "."  # Empty
            row += "|"
            print(row)

        print("+" + "-" * board_width + "+")

    def render_score(self, score: int) -> None:
        """Display current score."""
        print(f"Score: {score}")

    def render_game_over(self, score: int) -> None:
        """Display final score and restart option."""
        print("\n" + "=" * 30)
        print("       GAME OVER")
        print("=" * 30)
        print(f"   Final Score: {score}")
        print("=" * 30)
        print("Press any key to restart...")
        print()
