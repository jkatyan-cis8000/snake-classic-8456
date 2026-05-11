# Input Handler Design Document

## Overview
The `input_handler.py` module provides keyboard input handling for the Snake game, capturing player input and translating it into directional changes for the snake.

## Architecture

### Key Components

#### Direction Enum
- **UP**: (0, -1) - Move up on the grid
- **DOWN**: (0, 1) - Move down on the grid
- **LEFT**: (-1, 0) - Move left on the grid
- **RIGHT**: (1, 0) - Move right on the grid

#### InputHandler Class
Main class responsible for capturing and processing keyboard input.

**Core Methods:**
- `handle_input(key)`: Maps key presses to directions, validates against 180-degree turns
- `listen_for_input(callback)`: Registers a callback function to receive direction updates
- `update_direction()`: Commits the next direction to current direction (called each game tick)
- `get_current_direction()`: Returns the current movement direction

**Validation Logic:**
- Prevents snake from reversing direction instantly (e.g., can't go LEFT when moving RIGHT)
- Opposite direction pairs: UP/DOWN, LEFT/RIGHT

## Key Mapping

### WASD Keys
- `w` or `W`: UP
- `a` or `A`: LEFT
- `s` or `S`: DOWN
- `d` or `D`: RIGHT

### Arrow Keys
- `\x1b[A`: UP (Escape sequence for up arrow)
- `\x1b[B`: DOWN (Escape sequence for down arrow)
- `\x1b[D`: LEFT (Escape sequence for left arrow)
- `\x1b[C`: RIGHT (Escape sequence for right arrow)

## Event Handling System

The handler uses a callback-based approach:
1. Client code registers a callback via `listen_for_input()`
2. When valid input is received, the callback is invoked with the new direction
3. The direction is stored in `_next_direction` until `update_direction()` is called

## Integration with Game Engine

The InputHandler is designed to integrate with `game_engine.py`:
- `GameEngine` calls `handle_input()` when keyboard events occur
- `GameEngine` calls `update_direction()` at the start of each game tick
- `GameEngine` retrieves current direction via `get_current_direction()`

## Usage Example

```python
from input_handler import InputHandler, Direction

def on_direction_changed(direction: Direction):
    print(f"Direction changed to {direction}")

handler = InputHandler()
handler.listen_for_input(on_direction_changed)

# Simulate key presses
handler.handle_input('w')  # Change to UP
handler.handle_input('a')  # Change to LEFT
handler.update_direction()  # Commit the direction
```

## Non-Obvious Constraints

1. **Buffered Input**: `_next_direction` allows input buffering between ticks, preventing missed keypresses
2. **Case Insensitivity**: WASD input is normalized to lowercase for consistent mapping
3. **No Direct Modification**: External code cannot directly modify `_current_direction` - only through `update_direction()`
4. **Escape Sequences**: Arrow keys use ANSI escape sequences which may vary by terminal
