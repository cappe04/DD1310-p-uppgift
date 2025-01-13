import collections
from app.config import Cell


class GameBoard:
    """
    Handles the game-logic for Game of Life
    """
    def __init__(self, size: tuple[int, int] | None=None):
        self.cell_buffer = set()
        self.discard_queue = collections.deque()
        self.add_queue = collections.deque()
        
        self.size = size
        
        self.generations = 0

    def __getitem__(self, cell: Cell) -> bool:
        """ Makes it so bracket notaion gives the state of that given cell, i.e. game_board[x, y] or self[x, y] """
        return self.get_border_adjusted(cell) in self.cell_buffer

    @staticmethod
    def get_surroundings(x, y):
        """ Returns a generator that yields the surrounding cells, excluding the given cell. Like a donut. """
        for i in range(y-1, y+2):
            for j in range(x-1, x+2):
                if not (j == x and i == y):
                    yield (j, i)

    def get_border_adjusted(self, cell: Cell) -> Cell:
        """ Adjust the cell to fit into the border if there is one """
        if self.size is None:
            return cell
        
        x, y = cell
        width, height = self.size

        return (x % width, y % height)

    def step(self):
        """ Do one simulation of the entire board. """
        updatable_cells = self.cell_buffer.copy() # Cells to be updated

        for x, y in self.cell_buffer:
            for cell in self.get_surroundings(x, y):
                updatable_cells.add(self.get_border_adjusted(cell))

        for cell in updatable_cells:
            self.__update_cell(cell)

        self.__clear_queues() # execute and clears queues

        self.generations += 1

    def __update_cell(self, cell: Cell):
        """ Apply Game of Life rules on the given cell. """
        neightbours = 0
        alive = self[*cell]
        for x, y in self.get_surroundings(*cell):
            neightbours += self[x, y]

        # Adds to queue, must be done this way as
        # the other cells yet to update might be relying
        # on the current state of this cell.
        if alive and not 2 <= neightbours <= 3:
            self.discard_queue.append(cell)
        elif neightbours == 3:
            self.add_queue.append(cell)

    def __clear_queues(self):
        """ Clears and exectues the queues. """
        while self.discard_queue:
            cell = self.discard_queue.pop()
            self.cell_buffer.discard(cell)

        while self.add_queue:
            cell = self.add_queue.pop()
            self.cell_buffer.add(cell)

    def toggle_cell(self, x: int, y: int):
        """ Toggles state of cell. """
        if self[x, y]:
            self.cell_buffer.discard(self.get_border_adjusted((x, y)))
        else:
            self.cell_buffer.add(self.get_border_adjusted((x, y)))

    def clear_board(self):
        """ Clears the board and resets the generations. """
        self.cell_buffer.clear()
        self.generations = 0


        