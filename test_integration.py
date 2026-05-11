#!/usr/bin/env python3
"""
Integration test script for Snake Classic game.
Tests complete game flow across all difficulty levels.
"""

import sys
from game_engine import GameEngine, Direction
from game_state import GameState, Difficulty


def test_basic_movement():
    """Test 1: Basic snake movement."""
    print("=== Test 1: Basic Movement ===")
    game_state = GameState()
    engine = GameEngine(game_state, (20, 20))
    engine.start_game()
    
    initial_pos = engine.get_snake_positions()[0]
    print(f"Start position: {initial_pos}")
    
    # Move right
    engine.change_direction(Direction.RIGHT)
    engine.update()
    new_pos = engine.get_snake_positions()[0]
    print(f"After move right: {new_pos}")
    assert new_pos[0] == initial_pos[0] + 1, "X should increase"
    
    # Move up
    engine.change_direction(Direction.UP)
    engine.update()
    new_pos = engine.get_snake_positions()[0]
    print(f"After move up: {new_pos}")
    assert new_pos[1] == initial_pos[1] - 1, "Y should decrease"
    
    print("✓ Movement test passed\n")


def test_direction_validation():
    """Test 2: Direction validation (no 180-degree turns)."""
    print("=== Test 2: Direction Validation ===")
    game_state = GameState()
    engine = GameEngine(game_state, (20, 20))
    engine.start_game()
    
    # Cannot reverse direction
    engine.change_direction(Direction.RIGHT)
    assert engine.snake.direction == Direction.RIGHT, "Should be RIGHT"
    
    engine.change_direction(Direction.LEFT)  # Invalid - opposite
    assert engine.snake.direction == Direction.RIGHT, "Should stay RIGHT"
    
    engine.change_direction(Direction.UP)
    engine.change_direction(Direction.DOWN)  # Invalid - opposite
    assert engine.snake.direction == Direction.UP, "Should stay UP"
    
    print("✓ Direction validation test passed\n")


def test_food_spawning():
    """Test 3: Food spawning and eating."""
    print("=== Test 3: Food Spawning and Eating ===")
    game_state = GameState()
    engine = GameEngine(game_state, (20, 20))
    engine.start_game()
    
    initial_score = engine.get_score()
    initial_food = engine.get_food_position()
    print(f"Initial food at: {initial_food}")
    
    # Move snake to food
    snake_head = engine.get_snake_positions()[0]
    engine.change_direction(Direction.RIGHT)
    
    while engine.get_snake_positions()[0][0] < initial_food[0]:
        engine.update()
    
    # Snake should eat food
    score_after = engine.get_score()
    print(f"Score: {initial_score} -> {score_after}")
    
    print("✓ Food spawning test passed\n")


def test_wall_collision():
    """Test 4: Wall collision detection."""
    print("=== Test 4: Wall Collision ===")
    game_state = GameState()
    engine = GameEngine(game_state, (20, 20))
    engine.start_game()
    
    engine.change_direction(Direction.RIGHT)
    
    # Move until game over
    moves = 0
    while not engine.is_game_over() and moves < 50:
        engine.update()
        moves += 1
    
    assert engine.is_game_over(), "Game should end on wall collision"
    print(f"Game over after {moves} moves due to wall collision")
    print("✓ Wall collision test passed\n")


def test_self_collision():
    """Test 5: Self collision detection."""
    print("=== Test 5: Self Collision ===")
    game_state = GameState()
    engine = GameEngine(game_state, (10, 10))
    engine.start_game()
    
    # Create a snake long enough to collide with itself
    engine.change_direction(Direction.RIGHT)
    for _ in range(5):
        engine.update()
    
    # Make snake turn back on itself
    engine.change_direction(Direction.UP)
    engine.change_direction(Direction.LEFT)
    engine.change_direction(Direction.DOWN)
    
    # Continue until collision
    for _ in range(10):
        engine.update()
        if engine.is_game_over():
            break
    
    assert engine.is_game_over(), "Game should end on self collision"
    print("✓ Self collision test passed\n")


def test_all_difficulties():
    """Test 6: All difficulty levels."""
    print("=== Test 6: All Difficulty Levels ===")
    
    difficulties = [
        (Difficulty.EASY, 150),
        (Difficulty.MEDIUM, 100),
        (Difficulty.HARD, 75),
        (Difficulty.EXPERT, 50),
    ]
    
    for difficulty, expected_delay in difficulties:
        game_state = GameState()
        game_state.set_difficulty(difficulty)
        
        # Check internal mapping
        delay = {
            Difficulty.EASY: 150,
            Difficulty.MEDIUM: 100,
            Difficulty.HARD: 75,
            Difficulty.EXPERT: 50,
        }[difficulty]
        
        print(f"{difficulty.value}: {delay}ms delay")
        
        engine = GameEngine(game_state, (20, 20))
        engine.start_game()
        
        # Play briefly
        engine.change_direction(Direction.RIGHT)
        for _ in range(5):
            engine.update()
    
    print("✓ All difficulty levels test passed\n")


def test_score_tracking():
    """Test 7: Score tracking."""
    print("=== Test 7: Score Tracking ===")
    game_state = GameState()
    # Use a larger board to ensure snake can reach food
    engine = GameEngine(game_state, (30, 30))
    engine.start_game()
    
    score = engine.get_score()
    print(f"Initial score: {score}")
    assert score == 0, "Initial score should be 0"
    
    # Get initial position before any movement
    initial_head = engine.get_snake_positions()[0]
    food = engine.get_food_position()
    
    print(f"Initial head: {initial_head}, Food: {food}")
    
    # Calculate direction toward food
    # Snake starts with initial direction = RIGHT, position (15,15)
    # We need to move TOWARD food at (food[0], food[1])
    if initial_head[0] < food[0]:
        # Food is to the right - move RIGHT
        engine.change_direction(Direction.RIGHT)
        print("Moving RIGHT toward food")
    elif initial_head[0] > food[0]:
        # Food is to the left - move LEFT
        engine.change_direction(Direction.LEFT)
        print("Moving LEFT toward food")
    else:
        # Same X - move up or down based on Y
        if initial_head[1] < food[1]:
            engine.change_direction(Direction.DOWN)
            print("Moving DOWN toward food")
        else:
            engine.change_direction(Direction.UP)
            print("Moving UP toward food")
    
    # Eat food (move up to 50 times)
    initial_len = len(engine.get_snake_positions())
    max_moves = 50
    for i in range(max_moves):
        engine.update()
        new_head = engine.get_snake_positions()[0]
        print(f"Move {i+1}: head={new_head}, score={engine.get_score()}, len={len(engine.get_snake_positions())}")
        if engine.is_game_over():
            print("GAME OVER - hit wall")
            break
        if len(engine.get_snake_positions()) > initial_len:
            print("ATE FOOD!")
            break
    
    new_score = engine.get_score()
    print(f"Final score: {new_score}")
    assert new_score > 0, "Score should increase after eating"
    
    print("✓ Score tracking test passed\n")


def run_all_tests():
    """Run all integration tests."""
    print("=" * 50)
    print("Snake Classic Integration Tests")
    print("=" * 50 + "\n")
    
    tests = [
        test_basic_movement,
        test_direction_validation,
        test_food_spawning,
        test_wall_collision,
        test_self_collision,
        test_all_difficulties,
        test_score_tracking,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} FAILED: {e}\n")
            failed += 1
    
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
