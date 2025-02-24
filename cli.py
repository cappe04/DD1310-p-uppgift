import app.game_board
import app.config
import app.template_loader


num_gen = input("Hur många generatoioner: ")
size = input("size: ").split(" ")
size = (int(size[0]), int(size[1]))
board = app.game_board.GameBoard(size)

for x, y in app.template_loader.load_from_path("templates/glidare.txt"):
    board.toggle_cell(x, y)

if num_gen != "":
    num_gen = int(num_gen)
    for _ in range(num_gen):
        board.step()


while True:

    for x in range(size[0]):
        for y in range(size[1]):
            print("*" if board[x, y] else "-", end="")
        print("")

    command = input("Command: ")

    if command == "q":
        quit()

    if command != "" and command[0] == "t":
        args = command.split(" ")[1:3]
        board.toggle_cell(int(args[0]), int(args[1]))
    
    if command == "":

        board.step()
    

