import tkinter as tk
from tkinter import messagebox
import random

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def is_board_valid(board):
    for row in range(9):
        for col in range(9):
            num = board[row][col]
            if num != 0:
                board[row][col] = 0
                if not is_valid(board, row, col, num):
                    board[row][col] = num
                    return False
                board[row][col] = num
    return True

def generate_sudoku():
    board = [[0] * 9 for _ in range(9)]
    for i in range(9):
        for j in range(9):
            num_list = list(range(1, 10))
            while num_list:
                num = random.choice(num_list)
                num_list.remove(num)
                if is_valid(board, i, j, num):
                    board[i][j] = num
                    if solve_sudoku(board):
                        break
                    board[i][j] = 0
    for i in range(40):
        row, col = random.randint(0, 8), random.randint(0, 8)
        while board[row][col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
        board[row][col] = 0
    return board

class SudokuGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku")
        self.board = [[0] * 9 for _ in range(9)]
        self.solved_board = None
        self.cells = [[None] * 9 for _ in range(9)]
        self.timer_running = False
        self.time_elapsed = 0
        
        self.light_mode_colors = {
            "bg": "white",
            "fg": "black",
            "cell_bg1": "yellow",
            "cell_bg2": "white",
            "button_bg": "lightgrey",
            "button_fg": "black",
        }
        self.dark_mode_colors = {
            "bg": "black",
            "fg": "white",
            "cell_bg1": "grey",
            "cell_bg2": "darkgrey",
            "button_bg": "grey",
            "button_fg": "white",
        }
        self.current_colors = self.light_mode_colors
        self.create_widgets()
        self.apply_colors()

    def create_widgets(self):
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)
        self.settings_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Settings", menu=self.settings_menu)
        self.settings_menu.add_command(label="Light Mode", command=lambda: self.set_mode("light"))
        self.settings_menu.add_command(label="Dark Mode", command=lambda: self.set_mode("dark"))

        self.frame = tk.Frame(self.master, padx=10, pady=10)
        self.frame.pack()

        for row in range(9):
            for col in range(9):
                self.cells[row][col] = tk.Entry(self.frame, width=3, font=('Arial', 18), justify='center', relief="solid")
                self.cells[row][col].grid(row=row, column=col, padx=2, pady=2)

        self.timer_label = tk.Label(self.master, text="Time: 00:00", font=('Arial', 12))
        self.timer_label.pack()

        self.button_frame = tk.Frame(self.master, pady=10)
        self.button_frame.pack()

        self.solve_button = tk.Button(self.button_frame, text="Solve", command=self.solve, font=('Arial', 12), padx=10)
        self.solve_button.grid(row=0, column=0, padx=5)

        self.generate_button = tk.Button(self.button_frame, text="Generate", command=self.generate, font=('Arial', 12), padx=10)
        self.generate_button.grid(row=0, column=1, padx=5)

        self.check_button = tk.Button(self.button_frame, text="Check", command=self.check_solution, font=('Arial', 12), padx=10)
        self.check_button.grid(row=0, column=2, padx=5)

        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear, font=('Arial', 12), padx=10)
        self.clear_button.grid(row=0, column=3, padx=5)

    def apply_colors(self):
        self.master.config(bg=self.current_colors["bg"])
        self.frame.config(bg=self.current_colors["bg"])
        self.button_frame.config(bg=self.current_colors["bg"])

        for row in range(9):
            for col in range(9):
                color = self.current_colors["cell_bg1"] if (row // 3 + col // 3) % 2 == 0 else self.current_colors["cell_bg2"]
                self.cells[row][col].config(bg=color, fg=self.current_colors["fg"])

        self.solve_button.config(bg=self.current_colors["button_bg"], fg=self.current_colors["button_fg"])
        self.generate_button.config(bg=self.current_colors["button_bg"], fg=self.current_colors["button_fg"])
        self.check_button.config(bg=self.current_colors["button_bg"], fg=self.current_colors["button_fg"])
        self.clear_button.config(bg=self.current_colors["button_bg"], fg=self.current_colors["button_fg"])

    def set_mode(self, mode):
        if mode == "light":
            self.current_colors = self.light_mode_colors
        else:
            self.current_colors = self.dark_mode_colors
        self.apply_colors()

    def solve(self):
        self.read_board()
        if not is_board_valid(self.board):
            messagebox.showinfo("Sudoku", "The board is invalid")
            return
        self.solved_board = [row[:] for row in self.board]
        if solve_sudoku(self.solved_board):
            self.update_board(self.solved_board)
            self.stop_timer()
        else:
            messagebox.showinfo("Sudoku", "No solution exists")

    def generate(self):
        self.board = generate_sudoku()
        self.solved_board = [row[:] for row in self.board]
        solve_sudoku(self.solved_board)  # Get the solved board
        self.update_board(self.board)
        self.start_timer()

    def check_solution(self):
        self.read_board()
        if self.board == self.solved_board:
            messagebox.showinfo("Sudoku", "Congratulations! Your solution is correct.")
            self.stop_timer()
        else:
            messagebox.showinfo("Sudoku", "Sorry, your solution is incorrect.")

    def clear(self):
        self.board = [[0] * 9 for _ in range(9)]
        self.update_board(self.board)
        self.reset_timer()

    def read_board(self):
        for row in range(9):
            for col in range(9):
                try:
                    value = int(self.cells[row][col].get())
                    self.board[row][col] = value if 1 <= value <= 9 else 0
                except ValueError:
                    self.board[row][col] = 0

    def update_board(self, board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    self.cells[row][col].delete(0, tk.END)
                else:
                    self.cells[row][col].delete(0, tk.END)
                    self.cells[row][col].insert(0, str(board[row][col]))

    def start_timer(self):
        if not self.timer_running:
            self.time_elapsed = 0
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        if self.timer_running:
            mins, secs = divmod(self.time_elapsed, 60)
            time_formatted = f"Time: {mins:02}:{secs:02}"
            self.timer_label.config(text=time_formatted)
            self.time_elapsed += 1
            self.master.after(1000, self.update_timer)

    def stop_timer(self):
        self.timer_running = False

    def reset_timer(self):
        self.stop_timer()
        self.time_elapsed = 0
        self.timer_label.config(text="Time: 00:00")

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()
