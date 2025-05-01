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

t = tkinter.Tk()
c = tkinter.Canvas(t, width=UI_WIDTH - 3, height=UI_HEIGHT - 3, bg="white")
c.pack()


def draw_grid():
    for y in range(GRID_Y):
        for x in range(GRID_X):
            x1 = x * GRID_SIZE
            y1 = y * GRID_SIZE + GRID_Y_OFFSET
            x2 = x1 + GRID_SIZE
            y2 = y1 + GRID_SIZE
            id = c.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
            grid[y][x] = {id: ""}


def on_click(event):
    global playerToPlay
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


c.bind("<Button-1>", on_click)
c.bind("<Motion>", on_mouse_move)
draw_grid()
t.mainloop()
