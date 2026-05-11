# Snake Game Architecture

## Overview
A classic Snake game implementation with multiple difficulty levels, score tracking, and clean modular architecture.

## Module Structure

### 1. game_engine.py
**Responsibility**: Core game logic including snake movement, collision detection, and game state transitions.

**Interfaces**:
- `Snake` class: manages snake position, direction, and growth
- `GameEngine` class: handles game loop, collision detection, and win/loss conditions
- `Direction` enum: UP, DOWN, LEFT, RIGHT

**Key Functions**:
- `move_snake(direction)`: updates snake position
- `check_collision()`: returns True if snake hits wall or itself
- `eat_food()`: handles food consumption and growth

---

### 2. game_state.py
**Responsibility**: Manages game state including score, food positioning, and difficulty settings.

**Interfaces**:
- `GameState` class: stores current score, level, and food position
- `Difficulty` enum: EASY, MEDIUM, HARD, EXPERT

**Key Functions**:
- `spawn_food()`: generates random food position not on snake
- `update_score(points)`: increments score
- `get_speed()`: returns tick rate based on difficulty

---

### 3. input_handler.py
**Responsibility**: Handles keyboard input for game controls.

**Interfaces**:
- `InputHandler` class: captures and processes keyboard events
- `handle_input(key)`: maps keys to direction changes

**Key Functions**:
- `listen_for_input(callback)`: registers callback for input events
- `validate_direction(new_direction)`: prevents 180-degree turns

---

### 4. renderer.py
**Responsibility**: Renders the game state to the console.

**Interfaces**:
- `Renderer` class: draws the game board, snake, and food

**Key Functions**:
- `render_board()`: draws the grid with snake and food
- `render_score()`: displays current score
- `render_game_over()`: displays final score and restart option

---

### 5. main.py
**Responsibility**: Application entry point and game loop orchestration.

**Interfaces**:
- `Game` class: orchestrates all components
- `run()`: main game loop

**Key Functions**:
- `initialize_game()`: sets up all components
- `game_loop()`: runs the game until completion
- `restart_game()`: resets state and starts new game

---

## File Organization
```
snake-classic-8456/
├── main.py              # Entry point
├── game_engine.py       # Core game logic
├── game_state.py        # State and difficulty management
├── input_handler.py     # Keyboard input handling
├── renderer.py          # Display/rendering system
├── requirements.txt     # Dependencies (if any)
└── opencode.json        # Configuration
```

## Data Flow
1. `main.py` initializes all components
2. `InputHandler` captures keypresses and updates direction
3. `GameEngine` moves snake and checks collisions
4. `GameState` tracks score and food position
5. `Renderer` displays updated state

## Difficulty Levels
- **Easy**: 150ms per tick, larger safe zones
- **Medium**: 100ms per tick, standard board
- **Hard**: 75ms per tick, faster movement
- **Expert**: 50ms per tick, extreme speed

## Game Loop
1. Process input → 2. Update game state → 3. Render → 4. Wait (difficulty-based delay) → Repeat
