# sudoku.py
# Main Sudoku generator and solver implementation
import copy
import random

class SudokuBoard:
    def __init__(self, grid):
        # Use deepcopy to ensure the original grid is not modified
        self.grid = copy.deepcopy(grid)
        self.size = 9

    def is_valid(self, row, col, num):
        # Check row
        for i in range(self.size):
            if self.grid[row][i] == num:
                return False

        # Check column
        for i in range(self.size):
            if self.grid[i][col] == num:
                return False

        # Check 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.grid[i + start_row][j + start_col] == num:
                    return False
        
        return True

    def find_empty(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    return (i, j)  # row, col
        return None

    def solve(self, randomize=False):
        find = self.find_empty()
        if not find:
            return True
        else:
            row, col = find

        numbers = list(range(1, self.size + 1))
        if randomize:
            random.shuffle(numbers)

        for num in numbers:
            if self.is_valid(row, col, num):
                self.grid[row][col] = num
                if self.solve(randomize):
                    return True
                self.grid[row][col] = 0  # Backtrack
        return False
    
    def count_solve_steps(self):
        """Count the number of recursive calls needed to solve the puzzle."""
        steps = [0]  # Use list to make it mutable in nested function
        
        def solve_with_count():
            steps[0] += 1
            find = self.find_empty()
            if not find:
                return True
            
            row, col = find
            for num in range(1, self.size + 1):
                if self.is_valid(row, col, num):
                    self.grid[row][col] = num
                    if solve_with_count():
                        return True
                    self.grid[row][col] = 0  # Backtrack
            return False
        
        solve_with_count()
        return steps[0]

    def has_unique_solution(self):
        """
        Check if the Sudoku puzzle has a unique solution.
        Returns True if the puzzle has exactly one solution, False otherwise.
        """
        solution_count = 0

        def count_solutions():
            nonlocal solution_count
            find = self.find_empty()
            if not find:
                solution_count += 1
                return

            row, col = find
            for num in range(1, self.size + 1):
                if self.is_valid(row, col, num):
                    self.grid[row][col] = num
                    count_solutions()
                    self.grid[row][col] = 0  # Backtrack

                    # Stop early if more than one solution is found
                    if solution_count > 1:
                        return

        count_solutions()
        return solution_count == 1

    def score_difficulty(self):
        """
        Score the difficulty of a Sudoku puzzle based on empty cells and solving complexity.
        Returns 'Easy', 'Medium', or 'Hard'.
        
        Algorithm:
        1. Count empty cells (primary factor)
        2. Measure solving steps (secondary factor for complexity)
        3. Calculate weighted difficulty score
        
        Difficulty classification:
        - Easy: Score ≤ 40
        - Medium: Score 41-60
        - Hard: Score > 60
        """
        import copy
        
        # Count empty cells
        empty_cells = sum(row.count(0) for row in self.grid)
        
        # Create a copy to measure solving complexity
        test_board = SudokuBoard(copy.deepcopy(self.grid))
        solving_steps = test_board.count_solve_steps()
        
        # Calculate weighted difficulty score
        # Empty cells contribute 70%, solving complexity contributes 30%
        difficulty_score = (empty_cells * 0.7) + (solving_steps * 0.3)
        
        # Classify based on score
        if difficulty_score <= 40:
            return "Easy"
        elif difficulty_score <= 60:
            return "Medium"
        else:
            return "Hard"


def generate(difficulty):
    # 1. Create a full, random solution
    empty_grid = [[0] * 9 for _ in range(9)]
    solution_board = SudokuBoard(empty_grid)
    solution_board.solve(randomize=True)  # Use the randomized solver

    # 2. Create a puzzle by removing cells
    puzzle_board = SudokuBoard(solution_board.grid)
    
    cells_to_remove = difficulty
    while cells_to_remove > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)

        if puzzle_board.grid[row][col] != 0:
            puzzle_board.grid[row][col] = 0
            cells_to_remove -= 1
            
    return puzzle_board, solution_board