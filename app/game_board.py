import collections


class GameBoard:
    def __init__(self, size: tuple[int, int]|None=None):
        self.cell_buffer = set()
        self.discard_queue = collections.deque()
        self.add_queue = collections.deque()

        self.size = size

        self.generations = 0

    def __getitem__(self, cell):
        return self.get_border_adjusted(cell) in self.cell_buffer

    @staticmethod
    def get_surroundings(x, y):
        for i in range(y-1, y+2):
            for j in range(x-1, x+2):
                if not (j == x and i == y):
                    yield (j, i)

    def get_border_adjusted(self, cell):
        if self.size is None:
            return cell
        
        x, y = cell
        width, height = self.size

        return (x % width, y % height)

    def step(self):
        updateable_cells = self.cell_buffer.copy()

        for x, y in self.cell_buffer:
            for cell in self.get_surroundings(x, y):
                updateable_cells.add(self.get_border_adjusted(cell)) # MODULU HERE
                # updateable_cells.add(cell) # MODULU HERE

        for cell in updateable_cells:
            self.__update_cell(cell)

        self.__clear_queues()

        self.generations += 1

    def __update_cell(self, cell):
        neightbours = 0
        alive = self[*cell]
        for x, y in self.get_surroundings(*cell):
            neightbours += self[x, y] # MODOLU HERE

        if alive and not 2 <= neightbours <= 3:
            self.discard_queue.append(cell)
        elif neightbours == 3:
            self.add_queue.append(cell)

    def __clear_queues(self):
        while self.discard_queue:
            cell = self.discard_queue.pop()
            self.cell_buffer.discard(cell)

        while self.add_queue:
            cell = self.add_queue.pop()
            self.cell_buffer.add(cell)

    def toggle_cell(self, x, y):
        if self[x, y]:
            self.cell_buffer.discard(self.get_border_adjusted((x, y)))
        else:
            self.cell_buffer.add(self.get_border_adjusted((x, y)))


        