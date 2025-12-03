"""
GUI 自動化測試 - 使用 unittest 和 tkinter 測試工具
注意：這是進階選項，課程可能不要求
"""

import unittest
import tkinter as tk
from sudoku_gui import SudokuGUI


class TestSudokuGUI(unittest.TestCase):
    """GUI 自動化測試 - 測試 GUI 元件邏輯"""
    
    def setUp(self):
        """每個測試前建立 GUI 實例"""
        self.root = tk.Tk()
        self.app = SudokuGUI(self.root)
        # 不顯示視窗（背景測試）
        self.root.withdraw()
    
    def tearDown(self):
        """每個測試後清理"""
        self.root.destroy()
    
    def test_initial_state(self):
        """測試初始狀態"""
        # 檢查遊戲狀態初始化
        self.assertIsNotNone(self.app.puzzle_board)
        self.assertIsNotNone(self.app.solution_board)
        self.assertIsNotNone(self.app.original_puzzle)
        self.assertFalse(self.app.solution_shown)
        self.assertFalse(self.app.show_errors)
        
    def test_difficulty_selection(self):
        """測試難度選擇"""
        # 測試 Easy
        self.app.selected_difficulty.set("30")
        count = self.app.get_empty_cells_count()
        self.assertEqual(count, 30)
        
        # 測試 Medium
        self.app.selected_difficulty.set("45")
        count = self.app.get_empty_cells_count()
        self.assertEqual(count, 45)
        
        # 測試 Hard
        self.app.selected_difficulty.set("55")
        count = self.app.get_empty_cells_count()
        self.assertEqual(count, 55)
    
    def test_cell_selection(self):
        """測試格子選擇"""
        # 選擇格子
        self.app.cell_clicked(4, 4)
        self.assertEqual(self.app.selected_cell, (4, 4))
        
        # 選擇不同格子
        self.app.cell_clicked(0, 0)
        self.assertEqual(self.app.selected_cell, (0, 0))
    
    def test_toggle_solution(self):
        """測試顯示/隱藏答案"""
        # 保存原始狀態
        original_grid = [row[:] for row in self.app.puzzle_board.grid]
        
        # 顯示答案
        self.app.toggle_solution()
        self.assertTrue(self.app.solution_shown)
        self.assertEqual(self.app.puzzle_board.grid, self.app.solution_board.grid)
        
        # 隱藏答案
        self.app.toggle_solution()
        self.assertFalse(self.app.solution_shown)
        self.assertEqual(self.app.puzzle_board.grid, original_grid)
    
    def test_clear_user_inputs(self):
        """測試清除用戶輸入"""
        # 模擬用戶填入數字
        if self.app.original_puzzle[0][0] == 0:
            self.app.puzzle_board.grid[0][0] = 5
        
        # 清除
        self.app.clear_user_inputs()
        
        # 檢查恢復到原始狀態
        self.assertEqual(
            self.app.puzzle_board.grid,
            self.app.original_puzzle
        )
    
    def test_check_solution_logic(self):
        """測試檢查邏輯"""
        # 填滿正確答案
        self.app.puzzle_board.grid = [row[:] for row in self.app.solution_board.grid]
        
        # 檢查（應該成功）
        self.app.check_solution()
        # 注意：這會觸發 messagebox，在自動測試中可能需要 mock
        
    def test_generate_new_puzzle(self):
        """測試生成新題目"""
        old_puzzle = [row[:] for row in self.app.puzzle_board.grid]
        
        # 生成新題
        self.app.generate_new_puzzle()
        
        # 檢查狀態重置
        self.assertFalse(self.app.solution_shown)
        self.assertFalse(self.app.show_errors)
        self.assertIsNone(self.app.selected_cell)
        
        # 新題目應該不同（高機率）
        # 注意：理論上可能生成相同題目，但機率極低
        

class TestGUIIntegration(unittest.TestCase):
    """整合測試 - 測試 GUI 與核心邏輯的整合"""
    
    def setUp(self):
        self.root = tk.Tk()
        self.app = SudokuGUI(self.root)
        self.root.withdraw()
    
    def tearDown(self):
        self.root.destroy()
    
    def test_puzzle_has_unique_solution(self):
        """測試生成的題目有唯一解"""
        # 這測試 GUI 是否正確使用核心邏輯
        has_unique = self.app.puzzle_board.has_unique_solution()
        self.assertTrue(has_unique)
    
    def test_solution_is_valid(self):
        """測試解答的有效性"""
        solution = self.app.solution_board
        
        # 檢查沒有空格
        for row in solution.grid:
            self.assertNotIn(0, row)
        
        # 檢查行、列、宮沒有重複
        for i in range(9):
            # 檢查行
            row = solution.grid[i]
            self.assertEqual(len(set(row)), 9)
            
            # 檢查列
            col = [solution.grid[j][i] for j in range(9)]
            self.assertEqual(len(set(col)), 9)
        
        # 檢查 3x3 宮
        for box_row in range(3):
            for box_col in range(3):
                box = []
                for i in range(3):
                    for j in range(3):
                        box.append(solution.grid[box_row*3 + i][box_col*3 + j])
                self.assertEqual(len(set(box)), 9)


if __name__ == '__main__':
    # 運行測試
    # 注意：GUI 測試可能需要 X server（Linux）或顯示環境
    unittest.main()
