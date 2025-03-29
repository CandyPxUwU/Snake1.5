import tkinter
import random  
import time
import sys
import os

ROWS = 25
COLS = 45
TILE_SIZE = 40

pausecheck = False
Speed = 75

#Possible background colors
strings = ["Pink","DarkBlue","DarkGrey","Indigo","Maroon"]

RandomBG = random.choice(strings)

#Possible snake body colors
snakeybody = ["LimeGreen","Red","Yellow"]
SnakeBody = random.choice(snakeybody)
if SnakeBody == "LimeGreen":
    snakehead = "green"
if SnakeBody == "Red":
    snakehead = "DarkRed"
if SnakeBody == "Yellow":
    snakehead = "Orange"

WINDOW_WIDTH = TILE_SIZE * COLS #25*25 = 625
WINDOW_HEIGHT = TILE_SIZE * ROWS #25*25 = 625

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#game window
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg = RandomBG, width = WINDOW_WIDTH, height = WINDOW_HEIGHT, borderwidth = 0, highlightthickness = 0)
canvas.pack()
window.update()

#center the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width/4) - (window_width/4))
window_y = int((screen_height/2) - (window_height/2))

#format "(w)x(h)+(x)+(y)"
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

#initialize game
snake = Tile(TILE_SIZE * 5, TILE_SIZE * 5) #single tile, snake's head
food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)
velocityX = 0
velocityY = 0
snake_body = [] #multiple snake tiles
game_over = False
score = 0


def reset_game():
    global snake, food, snake_body, velocityX, velocityY, game_over, score

    # Reset the game variables
    snake = Tile(TILE_SIZE * 5, TILE_SIZE * 5)  # Reset snake's position
    food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)  # Reset food's position
    velocityX = 0
    velocityY = 0
    snake_body = []  # Clear the snake's body
    game_over = False  # Mark game as not over
    score = 0  # Reset the score
    RandomBG = random.choice(strings)
    canvas.configure(bg=RandomBG)  # Change to blue



def change_direction(e):  # e = event
    global velocityX, velocityY, game_over, score

    # Reset the game if it's over
    if game_over:
        scoresave()
        reset_game()  # Reset game variables
        return

    # Change direction based on key pressed
    if e.keysym == "w" and velocityY != 1:
        velocityX = 0
        velocityY = -1
    elif e.keysym == "s" and velocityY != -1:
        velocityX = 0
        velocityY = 1
    elif e.keysym == "a" and velocityX != 1:
        velocityX = -1
        velocityY = 0
    elif e.keysym == "d" and velocityX != -1:
        velocityX = 1
        velocityY = 0



def move():
    global snake, food, snake_body, game_over, score
    if (game_over):
     return
    
    if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        game_over = True
        return
    
    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            game_over = True
            return
    
    #collision
    if (snake.x == food.x and snake.y == food.y): 
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLS-1) * TILE_SIZE
        food.y = random.randint(0, ROWS-1) * TILE_SIZE
        score += 1

    #update snake body
    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if (i == 0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y
    
    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE


def draw():
    global snake, food, snake_body, game_over, score
    move()

    canvas.delete("all")

    #draw food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill = 'red')

    #draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill = snakehead)

    for tile in snake_body:
        
        
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = SnakeBody)

    if (game_over):
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font = "Arial 20", text = f"Game Over, Score: {score}, Press anything to play again!", fill = "white")
    else:
        canvas.create_text(60, 20, font = "Arial 20", text = f"Score: {score}", fill = "white")
    
    window.after(75, draw) #call draw again every 100ms (1/10 of a second) = 10 frames per second

# Add projectile variables
projectiles = []  # List to store active projectiles
PROJECTILE_SPEED = 1.5  # Reduced speed multiplier for projectiles
PROJECTILE_HITBOX_RADIUS = 30  # Increase hitbox radius for projectiles

class Projectile(Tile):
    def __init__(self, x, y, directionX, directionY):
        super().__init__(x, y)
        self.directionX = directionX
        self.directionY = directionY

def shoot():
    global projectiles, velocityX, velocityY
    if velocityX != 0 or velocityY != 0:  # Only shoot if the snake is moving
        # Create a projectile in the current direction
        projectile = Projectile(snake.x + TILE_SIZE // 2, snake.y + TILE_SIZE // 2, velocityX, velocityY)
        projectiles.append(projectile)

def move_projectiles():
    global projectiles, food, score
    for projectile in projectiles[:]:
        # Move projectile in its direction
        projectile.x += projectile.directionX * TILE_SIZE * PROJECTILE_SPEED
        projectile.y += projectile.directionY * TILE_SIZE * PROJECTILE_SPEED

        # Check if projectile hits the fruit using hitbox radius
        if (abs(projectile.x - (food.x + TILE_SIZE // 2)) <= PROJECTILE_HITBOX_RADIUS and
                abs(projectile.y - (food.y + TILE_SIZE // 2)) <= PROJECTILE_HITBOX_RADIUS):
            projectiles.remove(projectile)
            food.x = random.randint(0, COLS - 1) * TILE_SIZE
            food.y = random.randint(0, ROWS - 1) * TILE_SIZE
            snake_body.append(Tile(food.x, food.y))
            score += 1
            

        # Remove projectiles if they go out of bounds
        elif (projectile.x < 0 or projectile.x >= WINDOW_WIDTH or
              projectile.y < 0 or projectile.y >= WINDOW_HEIGHT):
            projectiles.remove(projectile)

def pause(e=None):  # Toggle pause state
    global pausecheck, content
    pausecheck = not pausecheck
    # Open the file in read mode
    with open("save.txt", "r") as file:
        # Read the entire contents of the file
        content = file.read()

# Update `draw` function to include pause functionality
def draw():
    global snake, food, snake_body, game_over, score, Speed, content

    # Check if the game is paused
    if pausecheck:
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, font="Arial 20",
                           text=f"Paused - Press 'Tab' to resume,\nscores:\n\n{content}", fill="white")
        window.after(100, draw)  # Continue checking while paused
        return

    move()

    # Move projectiles
    move_projectiles()

    canvas.delete("all")

    # Draw food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill='red')

    # Draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill=snakehead)

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill=SnakeBody)

    # Draw projectiles (larger size)
    for projectile in projectiles:
        canvas.create_oval(projectile.x - 10, projectile.y - 10, projectile.x + 10, projectile.y + 10, fill="yellow")

    if game_over:
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, font="Arial 20",
                           text=f"Game Over, Score: {score}, Press anything to play again!", fill="white")
    else:
        canvas.create_text(60, 20, font="Arial 20", text=f"Score: {score}", fill="white")

    window.after(75, draw)  # Call draw again every 75ms (13.3 FPS)

def scoresave(e=None):
    global score
    with open("save.txt", "a") as file:
        file.write(f"Score: {score}\n\n")
        # Open the file and read all lines
    with open("save.txt", "r") as file:
        lines = file.readlines()
    # Open the file and read all lines
    with open("save.txt", "r") as file:
        lines = file.readlines()
    
    # If the file has more than 24 lines, remove the top lines
    if len(lines) > 24:
        lines = lines[-24:]  # Keep only the last 24 lines
    
    # Rewrite the file with the updated lines
    with open("save.txt", "w") as file:
        file.writelines(lines)




# Bind 'p' key to pause and resume
window.bind("<KeyRelease-Tab>", pause)

# Other key bindings
window.bind("<KeyRelease-space>", lambda e: shoot())
window.bind("<KeyPress>", change_direction)  # Bind directional controls

draw()
window.mainloop()  # Used for listening to window events like key presses
