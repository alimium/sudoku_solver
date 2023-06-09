from sudoku.game.sudoku import SudokuGame
from typing import List, Dict
import copy
from enum import Enum
from colorama import Fore


class SelectionMethod(Enum):
    ROW = "Row"
    COLUMN = "Column"
    GRID = "Grid"
    RANDOM = "Random"
    LEAST_CONSTRAINED = "Least Constrained"
    MOST_CONSTRAINED = "Most Constrained"


class SudokuSolver:
    def __init__(self, game: SudokuGame = None, log=True) -> None:
        self.original_game: SudokuGame = game
        self.game: SudokuGame = SudokuGame(self.original_game.array_board)
        self.solve_history: List[SudokuGame] = [self.original_game]
        self._is_solved: bool = False
        self._log: bool = log
        self._steps: int = 0
        self._time: int = 0

    def log(self, msg: str) -> None:
        if self._log:
            print(
                f"{Fore.YELLOW} ------> {Fore.RESET}SOLVER [{Fore.YELLOW}{self.__class__.__name__}{Fore.RESET}] |\t{msg}"
            )

    def _reset_solver(self):
        self.game: SudokuGame = SudokuGame(self.original_game.array_board)
        self.solve_history: List[SudokuGame] = [self.original_game]
        self._is_solved: bool = False
        self._steps: int = 0
        self._time: int = 0
        self._backtracks: int = 0

    def _game_is_valid(self, game, row: int, col: int, num: int) -> bool:
        game.array_board[row, col] = num
        row_const, col_const, grid_const = self._constraint_check(game)
        if all(row_const) and all(col_const) and all(grid_const):
            res = True
        else:
            res = False

        return res

    def _constraint_check(
        self, game: SudokuGame
    ) -> Dict[str, Dict[int, Dict[int, int]]]:
        board_check = game.validate(ignore_empty_cells=True)
        rows = board_check["rows"]
        columns = board_check["columns"]
        grids = board_check["grids"]

        return rows, columns, grids

    def _is_solvable(self) -> bool:
        for i in self.game.rows:
            visited = set()
            for j in i:
                if j != 0:
                    if j in visited:
                        return False
                    visited.add(j)

        for i in self.game.columns:
            visited = set()
            for j in i:
                if j != 0:
                    if j in visited:
                        return False
                    visited.add(j)

        for i in self.game.grids:
            visited = set()
            for j in i.flatten():
                if j != 0:
                    if j in visited:
                        return False
                    visited.add(j)

        return True
