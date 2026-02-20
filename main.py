import tkinter
import random
import winsound


def load_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except:
        return 0
    
def save_high_score(score):
    with open("highscore.txt", "w") as file:
        file.write(str(score))
ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDHT = TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y 

#game window
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg = "#969696", width = WINDOW_WIDHT, height = WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
canvas.pack()
canvas.update()

#center the window
window_widht = window.winfo_width()
window_height = window.winfo_height()
screen_widht = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_widht/2) - (window_widht/2))
window_y = int((screen_height/2) - (window_widht/2))

window.geometry(f"{window_widht}x{window_height}+{window_x}+{window_y}")

#initiliaze game
snake = Tile(5*TILE_SIZE, 5*TILE_SIZE) #single tile snake's head
food = Tile(10*TILE_SIZE, 10*TILE_SIZE)
snake_body = [] #multiple snake tiles
velocityX = 1
velocityY = 0
game_over = False
score = 0 
speed = 100
high_score = load_high_score()


def change_direction(e):
    # print(e)
    # print(e.keysym)
    global velocityX, velocityY, game_over

    if e.keysym == "r" or e.keysym == "R":
        restart()
        return

    if (game_over):
        return

    if (e.keysym == "Up" and velocityY != 1):
        velocityX = 0
        velocityY = -1
    elif (e.keysym == "Down" and velocityY != -1):
        velocityX = 0
        velocityY = 1
    elif (e.keysym == "Left" and velocityX != 1):
        velocityX = -1
        velocityY = 0
    elif (e.keysym == "Right" and velocityX != -1):
        velocityX = 1
        velocityY = 0

def move():
    global snake, food, snake_body, game_over, score, high_score, speed
    if (game_over):
        return
    
    if (snake.x < 0 or snake.x >= WINDOW_WIDHT or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        game_over = True
        if score > high_score:
            save_high_score(score)

        winsound.Beep(500, 150)
        winsound.Beep(300, 300)
        return
    
    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            game_over = True
            if score > high_score:
               save_high_score(score)

            winsound.Beep(500, 150)
            winsound.Beep(300, 300)
            return

    #collision
    if (snake.x == food.x and snake.y == food.y):
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLS-1) * TILE_SIZE
        food.y = random.randint(0, ROWS-1) * TILE_SIZE
        score += 1
        speed = max(40, speed - 5)

        winsound.Beep(800, 100)   # frekans, süre(ms)

    #update snake body
    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if i == 0:
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y
                          

    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE

def restart():
    global snake, food, snake_body, velocityX, velocityY, game_over, score, speed

    snake = Tile(5*TILE_SIZE, 5*TILE_SIZE)
    food = Tile(10*TILE_SIZE, 10*TILE_SIZE)
    snake_body = []
    velocityX = 1
    velocityY = 0
    game_over = False
    score = 0
    speed = 100

def draw():
    global snake, food, snake_body, game_over, score
    move()

    canvas.delete("all")

    #draw food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill = "red")

    #draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill = "lime green")

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = "lime green") 

    window.after(speed, draw) #100ms = 1/10 seconds, 10 frames/second

    if (game_over):
        canvas.create_text(WINDOW_WIDHT/2, WINDOW_HEIGHT/2 - 20, font = "Arial 20", text = f"Game over: {score}", fill = "black")
        canvas.create_text(WINDOW_WIDHT/2, WINDOW_HEIGHT/2 + 20, font = "Arial 12", text = "Press R to restart", fill = "black")
    else:
        canvas.create_text(60, 20, font = "Arial 10", text = f"Score: {score}    High: {high_score}", fill = "black")

draw()

window.bind("<KeyRelease>", change_direction)
window.mainloop()