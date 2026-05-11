# Game State Design Document

## Overview
The `game_state.py` module manages the persistent state of the Snake game, including score tracking, food positioning, and difficulty configuration.

## Architecture

### Difficulty Enum
Four difficulty levels are defined, each mapping to a specific tick rate:
- **EASY**: 150ms per tick (slower pace for beginners)
- **MEDIUM**: 100ms per tick (standard gameplay)
- **HARD**: 75ms per tick (fast movement)
- **EXPERT**: 50ms per tick (extreme speed)

### GameState Class
Tracks the core game state:

#### Constructor
- Initializes difficulty (defaults to MEDIUM)
- Sets initial score to 0
- Sets initial food position to (0, 0)
- Loads speed mapping from difficulty

#### Properties
- `speed`: Returns the current tick delay in milliseconds based on difficulty

#### Methods
- `spawn_food(snake_positions, board_size)`: Generates a random food position that doesn't overlap with the snake
- `update_score(points)`: Increments the score by the specified points (default: 1)
- `set_difficulty(difficulty)`: Changes the difficulty level dynamically

## Key Design Decisions

### Food Spawning Algorithm
The `spawn_food()` method uses a rejection sampling approach:
1. Generates random coordinates within the board bounds
2. Checks if the position conflicts with any snake segment
3. Repeats until a valid position is found

This ensures food never spawns on the snake body.

**Parameters**:
- `snake_positions`: Set of (x, y) tuples representing snake segments
- `board_size`: Tuple of (width, height) for board boundaries (default: 20x20)

### Speed Configuration
Speed is stored as a dictionary mapping difficulties to millisecond delays. This allows:
- Easy lookup of current speed via property
- Simple addition of new difficulty levels
- Clean separation between difficulty and speed values

## Usage Example

```python
from game_state import GameState, Difficulty

# Create game state with default difficulty
state = GameState()

# Or specify difficulty explicitly
state = GameState(Difficulty.HARD)

# Spawn food (avoiding snake at positions [(0,0), (0,1)])
snake_pos = {(0, 0), (0, 1)}
state.spawn_food(snake_pos)

# Update score
state.update_score()

# Check current speed (returns ms delay)
print(state.speed)  # 75 for HARD difficulty
```

## Future Considerations
- Could add level progression based on score thresholds
- Could track high scores per difficulty level
- Could support custom board sizes per difficulty
