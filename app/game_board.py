import collections


class GameBoard:
    def __init__(self):
        self.cell_buffer = set()
        self.discard_queue = collections.deque()
        self.add_queue = collections.deque()

        self.generations = 0

    def __getitem__(self, cell):
        return cell in self.cell_buffer

    @staticmethod
    def get_surroundings(x, y):
        for i in range(y-1, y+2):
            for j in range(x-1, x+2):
                if not (j == x and i == y):
                    yield (j, i)

    def step(self):
        updateable_cells = self.cell_buffer.copy()

        for x, y in self.cell_buffer:
            for cell in self.get_surroundings(x, y):
                updateable_cells.add(cell)

        for cell in updateable_cells:
            self.__update_cell(cell)

        self.__clear_queues()

        self.generations += 1

    def __update_cell(self, cell):
        neightbours = 0
        alive = self[*cell]
        for x, y in self.get_surroundings(*cell):
            neightbours += self[x, y]

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
            self.cell_buffer.discard((x, y))
        else:
            self.cell_buffer.add((x, y))


        