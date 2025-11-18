# demo.py
# Demo script for Sudoku generator
from SUDOKU import generate

def print_board(board):
    """Print a Sudoku board in a nice format"""
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - + - - - + - - -")
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("| ", end="")
            if j == 8:
                print(board.grid[i][j] if board.grid[i][j] != 0 else ".")
            else:
                print(str(board.grid[i][j]) + " " if board.grid[i][j] != 0 else ". ", end="")

def main():
    print("Sudoku Generator Demo")
    print("=" * 40)
    
    # Generate a puzzle with 45 empty cells (medium difficulty)
    difficulty = 45
    puzzle, solution = generate(difficulty)
    
    print(f"\nGenerated Puzzle (Difficulty: {difficulty} empty cells):")
    print_board(puzzle)
    
    print(f"\nSolution:")
    print_board(solution)
    
    # Verify the puzzle is solvable
    puzzle_copy = puzzle.__class__(puzzle.grid)
    if puzzle_copy.solve():
        print("\nPuzzle verification: Solvable!")
    else:
        print("\nPuzzle verification: Not solvable!")

if __name__ == "__main__":
    main()
