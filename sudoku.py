# Name: Julia Liem
# Student number: 12043761
"""
Includes a sudoku class to solve a given unsolved sudoku
"""


from __future__ import annotations
from typing import Iterable


COORDINATE_VALUES = {0, 1, 2, 3, 4, 5, 6, 7, 8}


class Sudoku:
    """A mutable sudoku puzzle."""

    def __init__(self, puzzle: Iterable[Iterable]):
        # grid in string and integer format
        self._grid: list[str] = []
        self._grid_int: list[list[int]] = []
        # list of empty cell coordinates
        self._empty_cells: list[list[int]] = []

        # copy grid from input into _grid and _grid_int
        y = -1

        for puzzle_row in puzzle:
            x = -1
            y += 1

            row_str = ""
            row_int = []

            for element in puzzle_row:
                x += 1

                # copy each element into temporary row
                row_str += element
                row_int.append(int(element))

                # if cell is empty, write down coordinates
                if element == "0":
                    self._empty_cells.append([x, y])

            # copy each row into grids
            self._grid.append(row_str)
            self._grid_int.append(row_int)

    def place(self, value: int, x: int, y: int) -> None:
        """Place value at x,y and remove empty cell coordinates"""
        self._grid_int[y][x] = value
        self._empty_cells.remove([x, y])

    def unplace(self, x: int, y: int) -> None:
        """Remove (unplace) a number at x,y and add empty cell coordinates"""
        self._grid_int[y][x] = 0
        self._empty_cells.insert(1, [x, y])

    # this function is unused for solving the sudoku
    # as such, this function will not be further optimized
    def value_at(self, x: int, y: int) -> int:
        """Returns the value at x,y."""
        value = -1

        if x in COORDINATE_VALUES and y in COORDINATE_VALUES:
            row = self._grid_int[y]
            value = int(row[x])

        return value

    def options_at(self, x: int, y: int) -> Iterable[int]:
        """Returns all possible values (options) at x,y."""
        options = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        # Remove all values from the row
        for value in self.row_values(y):
            if value in options:
                options.remove(value)

        # Remove all values from the column
        for value in self.column_values(x):
            if value in options:
                options.remove(value)

        # Get the index of the block based from x,y
        block_index = (y // 3) * 3 + x // 3

        # Remove all values from the block
        for value in self.block_values(block_index):
            if value in options:
                options.remove(value)

        return options

    def next_empty_index(self) -> tuple[int, int]:
        """
        Returns the next index (x,y) that is empty (value 0).
        If there is no empty spot, returns (-1,-1)
        """
        # checks if there are still empty cells
        # if there are, take coordinates from first entry of empty cell list
        if len(self._empty_cells) == 0:
            next_x = -1
            next_y = -1
        else:
            next_coordinates = self._empty_cells[0]
            next_x = next_coordinates[0]
            next_y = next_coordinates[1]

        return next_x, next_y

    def row_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th row."""
        values = self._grid_int[i]

        return values

    def column_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th column."""
        values = []

        for j in range(9):
            row = self._grid_int[j]
            values.append(row[i])

        return values

    def block_values(self, i: int) -> Iterable[int]:
        """
        Returns all values at i-th block.
        The blocks are arranged as follows:
        0 1 2
        3 4 5
        6 7 8
        """
        values = []

        x_start = (i % 3) * 3
        y_start = (i // 3) * 3

        for x in range(x_start, x_start + 3):
            for y in range(y_start, y_start + 3):
                values.append(self._grid_int[y][x])

        return values

    def cast_solved(self) -> None:
        """
        formats the integer grid into a string grid and saves it into self._grid
        """
        y = -1

        for row_puzzle in self._grid_int:
            y += 1
            row = ""

            # cast every digit into string and add it to the row
            for digit in row_puzzle:
                row += str(digit)

            # add row to string grid
            self._grid[y] = row

    def is_solved(self) -> bool:
        """
        Reformats and saves the integer grid and returns True if and only if all rows,
        columns and blocks contain only the numbers 1 through 9. False otherwise.
        """
        if len(self._empty_cells) != 0:
            return False

        self.cast_solved()

        return True

    def __str__(self) -> str:
        representation = ""

        for row in self._grid:
            representation += row + "\n"

        return representation.strip()


def load_from_file(filename: str) -> Sudoku:
    """Load a Sudoku from filename."""
    puzzle: list[str] = []

    with open(filename) as f:
        for line in f:

            # strip newline and remove all commas
            line = line.strip().replace(",", "")

            puzzle.append(line)

    return Sudoku(puzzle)
