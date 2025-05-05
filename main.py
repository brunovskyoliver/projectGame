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
            
def update_grid():
    for y in range(GRID_Y):
        for x in range(GRID_X):
            x1 = x * GRID_SIZE
            y1 = y * GRID_SIZE + GRID_Y_OFFSET
            x2 = x1 + GRID_SIZE
            y2 = y1 + GRID_SIZE
            id = c.create_rectangle(x1, y1, x2, y2, fill="white" if grid[y][x][list(grid[y][x].keys())[0]] == "" else grid[y][x][list(grid[y][x].keys())[0]], outline="black")
            grid[y][x] = {id: grid[y][x][list(grid[y][x].keys())[0]]}


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
    
    horizontal_full = False
    vertical_full = False
        
    if check_horizontal() != None:
        horizontal_full = True
    if check_vertical() != None:
        vertical_full = True

    if horizontal_full and vertical_full:
        column = check_horizontal()
        colum1 = check_vertical()
        erase_horizontall(list(column.keys())[0])
        erase_vertical(list(colum1.keys())[0])
        update_grid()
    elif horizontal_full:
        erase_horizontall(list(check_horizontal().keys())[0])
        update_grid()
    elif vertical_full:
        erase_vertical(list(check_vertical().keys())[0])
        update_grid()
        
        


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
    

        
    
    
            
def check_horizontal():
    desired_color_1 = "blue"
    desired_color_2 = "red"
    for column in range(GRID_Y):
        is_full = True
        for cell in range(GRID_X):
            if (grid[column][cell][list(grid[column][cell].keys())[0]] == 
                desired_color_1 or 
                grid[column][cell][list(grid[column][cell].keys())[0]] == 
                desired_color_2):
                continue
            elif grid[column][cell][list(grid[column][cell].keys())[0]] != desired_color_1:
                is_full = False
            elif grid[column][cell][list(grid[column][cell].keys())[0]] != desired_color_2:
                is_full = False
        if is_full:
            return {column: "color_to_be_desired"}
    
    return None

def check_vertical():
    desired_color_1 = "blue"
    desired_color_2 = "red"
    for cell in range(GRID_Y):
        is_full = True
        for column in range(GRID_X):
            if (grid[column][cell][list(grid[column][cell].keys())[0]] == 
                desired_color_1 or 
                grid[column][cell][list(grid[column][cell].keys())[0]] == 
                desired_color_2):
                continue
            elif grid[column][cell][list(grid[column][cell].keys())[0]] != desired_color_1:
                is_full = False
            elif grid[column][cell][list(grid[column][cell].keys())[0]] != desired_color_2:
                is_full = False
        if is_full:
            return {cell: "color_to_be_desired"}
    
    return None
    
    
def erase_horizontall(column):
    for to_erase_column in range(column, 0, -1):
        for cell in range(GRID_X):
            grid[to_erase_column][cell][list(grid[to_erase_column][cell].keys())[0]] = grid[to_erase_column-1][cell][list(grid[to_erase_column-1][cell].keys())[0]]
    for cell in range(GRID_X):
        grid[0][cell][list(grid[0][cell].keys())[0]] = ""
    
def erase_vertical(column):
    for cell in range(column, GRID_Y-1):
        for to_erase_column in range(GRID_X):
            grid[to_erase_column][cell][list(grid[to_erase_column][cell].keys())[0]] = grid[to_erase_column][cell+1][list(grid[to_erase_column][cell+1].keys())[0]]
    for cell in range(GRID_Y):
        grid[cell][6][list(grid[cell][6].keys())[0]] = ""
        


c.bind("<Button-1>", on_click)
c.bind("<Motion>", on_mouse_move)
draw_grid()
t.mainloop()
