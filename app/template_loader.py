

def load(path):
    with open(path) as file:
        for coord in file:
            x, y = map(int, coord.strip().split(" "))
            yield (x, y)