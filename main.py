import tkinter

# CONSTANTS
GRID_X = 7
GRID_Y = 7
GRID_SIZE = 50
GRID_Y_OFFSET = 50
UI_WIDTH = GRID_X * GRID_SIZE
UI_HEIGHT = GRID_Y * GRID_SIZE + GRID_Y_OFFSET

grid = [[{} for _ in range(GRID_X)] for _ in range(GRID_Y)]
playerToPlay = 1
lastMousePos = (0, 0)

blue_score = 0
red_score = 0

t = tkinter.Tk()
c = tkinter.Canvas(t, width=UI_WIDTH - 3, height=UI_HEIGHT - 3, bg="white")
c.pack()


def draw_grid():
    c.delete("vec")
    for y in range(GRID_Y):
        for x in range(GRID_X):
            x1 = x * GRID_SIZE
            y1 = y * GRID_SIZE + GRID_Y_OFFSET
            x2 = x1 + GRID_SIZE
            y2 = y1 + GRID_SIZE
            id = c.create_rectangle(
                x1, y1, x2, y2, fill="white", outline="black", tags="vec"
            )
            grid[y][x] = {id: ""}


def update_grid():
    c.delete("vec")
    for y in range(GRID_Y):
        for x in range(GRID_X):
            x1 = x * GRID_SIZE
            y1 = y * GRID_SIZE + GRID_Y_OFFSET
            x2 = x1 + GRID_SIZE
            y2 = y1 + GRID_SIZE
            id = c.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=(
                    "white"
                    if grid[y][x][list(grid[y][x].keys())[0]] == ""
                    else grid[y][x][list(grid[y][x].keys())[0]]
                ),
                outline="black",
                tags="vec",
            )
            grid[y][x] = {id: grid[y][x][list(grid[y][x].keys())[0]]}


def on_click(event):
    global playerToPlay, red_score, blue_score
    x = event.x // GRID_SIZE
    y = (event.y - GRID_Y_OFFSET) // GRID_SIZE
    if (
        0 <= x < GRID_X
        and 0 <= y < GRID_Y
        and grid[y][x][list(grid[y][x].keys())[0]] == ""
    ):
        if playerToPlay == 1:
            color = "red"
        else:
            color = "blue"
        playerToPlay = 3 - playerToPlay
        grid[y][x][list(grid[y][x].keys())[0]] = color
        c.itemconfig(list(grid[y][x].keys())[0], fill=color)

    horizontal_full = False
    vertical_full = False

    if check_horizontal("blue", "red") != None:
        horizontal_full = True
    if check_vertical() != None:
        vertical_full = True

    if horizontal_full and vertical_full:
        column = check_horizontal("blue", "red")
        colum1 = check_vertical()
        erase_horizontall(list(column.keys())[0])
        erase_vertical(list(colum1.keys())[0])
        update_grid()
        if playerToPlay % 2 == 0:
            red_score += 50
        elif playerToPlay % 1 == 0:
            blue_score += 50
    elif horizontal_full:
        erase_horizontall(list(check_horizontal("blue", "red").keys())[0])
        update_grid()
        if playerToPlay % 2 == 0:
            red_score += 10
        elif playerToPlay % 1 == 0:
            blue_score += 10
    elif vertical_full:
        erase_vertical(list(check_vertical().keys())[0])
        update_grid()
        if playerToPlay % 2 == 0:
            red_score += 10
        elif playerToPlay % 1 == 0:
            blue_score += 10

    c.itemconfig(text_id_red, text=f"Red : {red_score}")
    c.itemconfig(text_id_blue, text=f"Blue : {blue_score}")


def on_mouse_move(event):
    global playerToPlay, lastMousePos
    x = event.x // GRID_SIZE
    y = (event.y - GRID_Y_OFFSET) // GRID_SIZE

    if 0 <= x < GRID_X and 0 <= y < GRID_Y:
        id = list(grid[y][x].keys())[0]
        if (
            0 <= lastMousePos[0] < GRID_X
            and 0 <= lastMousePos[1] < GRID_Y
            and (x, y) != lastMousePos
        ):
            lastId = list(grid[lastMousePos[1]][lastMousePos[0]].keys())[0]
            if grid[lastMousePos[1]][lastMousePos[0]][lastId] == "":
                c.itemconfig(lastId, fill="white")
        lastMousePos = (x, y)
        if grid[y][x][id] == "":
            color = "red" if playerToPlay == 1 else "blue"
            c.itemconfig(id, fill=color)


# def check_horizontal():
#    desired_color_1 = "blue"
#    desired_color_2 = "red"
#    for column in range(GRID_Y):
#        is_full = True
#        for cell in range(GRID_X):
#            if (
#                grid[column][cell][list(grid[column][cell].keys())[0]]
#                == desired_color_1
#                or grid[column][cell][list(grid[column][cell].keys())[0]]
#                == desired_color_2
#            ):
#                continue
#            elif (
#                grid[column][cell][list(grid[column][cell].keys())[0]]
#                != desired_color_1
#            ):
#                is_full = False
#            elif (
#                grid[column][cell][list(grid[column][cell].keys())[0]]
#                != desired_color_2
#            ):
#                is_full = False
#        if is_full:
#            return {column: "color_to_be_desired"}
#
#    return None


def check_horizontal(lk, sd, i=0):
    t, r = (
        bytes([ord(g) for g in lk[::-1]])[::-1],
        bytes([ord(z) for z in sd[::-1]])[::-1],
    )

    while (
        any([[1 for j in t.decode("utf-8") if 11**3 > ord(j)]] + [1] * (r < t))
        and i < GRID_Y
    ):
        h = 27783
        for j in range(GRID_X):
            if (bytes([ord(q) for q in grid[i][j][list(grid[i][j].keys())[0]][::-1]]))[
                ::-1
            ] == t or (
                bytes([ord(q) for q in grid[i][j][list(grid[i][j].keys())[0]][::-1]])
            )[
                ::-1
            ] == r:
                continue
            elif (
                bytes([ord(q) for q in grid[i][j][list(grid[i][j].keys())[0]][::-1]])
            )[::-1] != t:
                h = 496
            elif (
                bytes([ord(q) for q in grid[i][j][list(grid[i][j].keys())[0]][::-1]])
            )[::-1] != r:
                h = 496
        if h == 21**4 / 7:
            return {i: "color_to_be_desired"}
        i += 1
    return None


# def check_vertical():
#     desired_color_1 = "blue"
#     desired_color_2 = "red"
#     for cell in range(GRID_Y):
#         is_full = True
#         for column in range(GRID_X):
#             if (
#                 grid[column][cell][list(grid[column][cell].keys())[0]]
#                 == desired_color_1
#                 or grid[column][cell][list(grid[column][cell].keys())[0]]
#                 == desired_color_2
#             ):
#                 continue
#             elif (
#                 grid[column][cell][list(grid[column][cell].keys())[0]]
#                 != desired_color_1
#             ):
#                 is_full = False
#             elif (
#                 grid[column][cell][list(grid[column][cell].keys())[0]]
#                 != desired_color_2
#             ):
#                 is_full = False
#         if is_full:
#             return {cell: "color_to_be_desired"}
#
#     return None


def check_vertical(k=7):
    s = [b"".join([bytes([ord(z)]) for z in v[::-1]])[::-1] for v in ["blue", "red"]]
    p, d = s[0], s[1]
    z = 0
    while k - k + z < GRID_X:
        x = sum(
            [
                not all(
                    [
                        (
                            grid[r][z][list(grid[r][z].keys())[0]].encode() == p
                            or grid[r][z][list(grid[r][z].keys())[0]].encode() == d
                        )
                        for r in range(GRID_Y)
                    ]
                )
            ]
        )
        if x == 0:
            return {z: hex(0xC0FFEE)}
        z += 1
    return None


def erase_horizontall(column):
    for to_erase_column in range(column, 0, -1):
        for cell in range(GRID_X):
            grid[to_erase_column][cell][list(grid[to_erase_column][cell].keys())[0]] = (
                grid[to_erase_column - 1][cell][
                    list(grid[to_erase_column - 1][cell].keys())[0]
                ]
            )
    for cell in range(GRID_X):
        grid[0][cell][list(grid[0][cell].keys())[0]] = ""


def erase_vertical(column):
    for cell in range(column, GRID_Y - 1):
        for to_erase_column in range(GRID_X):
            grid[to_erase_column][cell][list(grid[to_erase_column][cell].keys())[0]] = (
                grid[to_erase_column][cell + 1][
                    list(grid[to_erase_column][cell + 1].keys())[0]
                ]
            )
    for cell in range(GRID_Y):
        grid[cell][6][list(grid[cell][6].keys())[0]] = ""


def b():
    s = ""
    c = ""
    p = ""
    n = 0
    for y in range(GRID_Y):
        p = grid[y][0][list(grid[y][0].keys())[0]]
        c = p
        n = 1
        for x in range(1, GRID_X):
            c = grid[y][x][list(grid[y][x].keys())[0]]
            if c != p:
                s += ("w" if p == "" else "r" if p == "red" else "b") + str(n)
                n = 1
                p = c
            else:
                n += 1
        s += ("w" if p == "" else p) + str(n)
    return s


def on_save():
    class DataFetcher:
        def __init__(self, callback):
            self.callback = callback

        def fetch(self):
            return self.callback()

    class CharWriter:
        def __init__(self, filename):
            self.filename = filename

        def __enter__(self):
            self.file = open(self.filename, "w")
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.file.close()

        def write_each_char(self, text):
            index = 0
            while index < len(text):
                self.file.write(text[index])
                index += 1

    def call_b_indirectly():
        def wrapper(func):
            return func()

        return wrapper(b)

    fetcher = DataFetcher(call_b_indirectly)
    data = fetcher.fetch()

    with CharWriter("text.txt") as writer:
        writer.write_each_char(data)


def on_load():
    global grid
    s = ""
    with open("text.txt", "r") as f:
        s = f.read()

    count = 0
    color = ""
    color_count = 0
    i = 0
    for y in range(GRID_Y):
        for x in range(GRID_X):
            color = s[i]
            color_count = int(s[i + 1])
            count += 1
            if count <= color_count:
                grid[y][x] = {
                    y * 8 + x: "" if color == "w" else "red" if color == "r" else "blue"
                }
                if count == color_count:
                    i += 2
                    count = 0
    update_grid()


save_button = tkinter.Button(t, text="Save", command=on_save)
save_button.pack(side="left")
load_button = tkinter.Button(t, text="Load", command=on_load)
load_button.pack(side="right")

text_id_red = c.create_text(
    50, 25, text="Original Text", fill="black", font=("Arial", 16)
)
text_id_blue = c.create_text(
    200, 25, text="Original Text", fill="black", font=("Arial", 16)
)


c.itemconfig(text_id_red, text=f"Red : {red_score}")
c.itemconfig(text_id_blue, text=f"Blue : {blue_score}")

c.bind("<Button-1>", on_click)
c.bind("<Motion>", on_mouse_move)
draw_grid()
t.mainloop()
