import tkinter
import random

ROWS = 25
COLS = 50

TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * ROWS
WINDOW_HEIGHT = TILE_SIZE * COLS


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# gamewindow
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(
    window,
    bg="black",
    width=WINDOW_WIDTH,
    height=WINDOW_HEIGHT,
    borderwidth=0,
    highlightthickness=0,
)
canvas.pack()
window.update()

# center the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")


# init the game
snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)
food = Tile(10 * TILE_SIZE, 10 * TILE_SIZE)
snake_body = []  # multiple snake tiles
velocityx = 0
velocityy = 0
game_over = False


def change_dirc(e):  # e=event
    global velocityx, velocityy, game_over
    if game_over:
        return
    if e.keysym == "Up" and velocityy != 1:
        velocityx = 0
        velocityy = -1
    elif e.keysym == "Down" and velocityy != -1:
        velocityx = 0
        velocityy = 1
    elif e.keysym == "Left" and velocityx != 1:
        velocityx = -1
        velocityy = 0
    elif e.keysym == "Right" and velocityx != -1:
        velocityx = 1
        velocityy = 0


def move():
    global snake, food, snake_body, game_over
    if game_over:
        return

    if (
        snake.x < 0
        or snake.x >= WINDOW_WIDTH
        or snake.y < 0
        or snake.y >= WINDOW_HEIGHT
    ):
        game_over = True
        return

    for tile in snake_body:
        if snake.x == tile.x and snake.y == tile.y:
            game_over = True
            return

    # detecet colli
    if snake.x == food.x and snake.y == food.y:
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE

    # update snake body
    for i in range(len(snake_body) - 1, -1, -1):
        tile = snake_body[i]
        if i == 0:
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i - 1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y

    snake.x += velocityx * TILE_SIZE
    snake.y += velocityy * TILE_SIZE


def draw():
    global snake
    move()

    canvas.delete("all")

    # draw food
    canvas.create_rectangle(
        food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill="red"
    )
    canvas.create_rectangle(
        snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill="lime green"
    )

    for tile in snake_body:
        canvas.create_rectangle(
            tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill="limegreen"
        )

    window.after(100, draw)


draw()

window.bind("<KeyRelease>", change_dirc)
window.mainloop()
