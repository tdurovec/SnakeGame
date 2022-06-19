from tkinter import Canvas
from random import randrange
from threading import Thread

class CONS:
    BOARD_WIDTH = 500
    BOARD_HEIGHT = 500
    TILE_SIZE = 50
    SNAKE_SIZE = TILE_SIZE
    FPS = 10


class Board:
    def __init__(self, canvas):
        self.canvas = canvas

    def drawBoard(self) -> None:
        for i in range(CONS.BOARD_WIDTH//CONS.TILE_SIZE):
            for j in range(CONS.BOARD_HEIGHT//CONS.TILE_SIZE):
                self.canvas.create_rectangle(
                                            i*CONS.TILE_SIZE, j*CONS.TILE_SIZE, 
                                            i*CONS.TILE_SIZE+CONS.TILE_SIZE,
                                            j*CONS.TILE_SIZE+CONS.TILE_SIZE,
                                            outline='white')

class Apple:

    def __init__(self, canvas):
        self.canvas = canvas

        self.foodX = randrange(0, CONS.BOARD_WIDTH, CONS.TILE_SIZE)
        self.foodY = randrange(0, CONS.BOARD_HEIGHT, CONS.TILE_SIZE)
    
    def resetFood(self) -> None:
        self.foodX = randrange(0, CONS.BOARD_WIDTH, CONS.TILE_SIZE)
        self.foodY = randrange(0, CONS.BOARD_HEIGHT, CONS.TILE_SIZE)

    def drawFood(self) -> None:
        self.canvas.create_rectangle(self.foodX, self.foodY,
                                     self.foodX + CONS.TILE_SIZE,
                                     self.foodY + CONS.TILE_SIZE,
                                     fill='lightblue') 

    @property
    def x(self) -> int:
        return self.foodX

    @property
    def y(self) -> int:
        return self.foodY


class Snake:
    KEYS = ["w", "a", "s", "d"]
    MAP_KEY_OPP = {"w": "s", "a": "d", "s": "w", "d": "a"}

    def __init__(self, canvas, apple):
        #
        #VARIABLES
        #
        self.canvas = canvas 
        self.apple = apple

        self.RUN = True
        #player

        self.snakeX = 0
        self.snakeY = CONS.BOARD_HEIGHT//2

        self.moveX = 1
        self.moveY = 0

        self.currentKey = "d"
        self.lastKey = self.currentKey

        self.tail = []
        self.snakeLengt = 3
        self.points = 0


    def moveSnake(self) -> None:
        self.lastKey = self.currentKey
        
        #head move
        self.snakeX += CONS.TILE_SIZE * self.moveX
        self.snakeY += CONS.TILE_SIZE * self.moveY

        #tail move
        self.tail.append({'x':self.snakeX, 'y':self.snakeY})
        self.tail = self.tail[-self.snakeLengt:]

        self.tailColision()


    def eatFood(self) -> None:

        if self.snakeX == self.apple.foodX and self.snakeY == self.apple.y:
            self.snakeLengt += 1
            self.points += 1

            self.appleSpawn()
            self.apple.resetFood()
    
    def appleSpawn(self) -> None:

        for part in self.tail:
            if part['x'] == self.apple.x and part['y'] == self.apple.y:
                self.apple.resetFood()
            
    def tailColision(self) -> None:
        for part in self.tail[:-1]:
            
            if part['x'] == self.snakeX and part['y'] == self.snakeY:
                self.RUN = False

    def wallColision(self) -> None:

        if self.snakeX > CONS.BOARD_WIDTH:
            self.snakeX = -CONS.TILE_SIZE

        elif self.snakeX < 0:
            self.snakeX = CONS.BOARD_WIDTH

        elif self.snakeY > CONS.BOARD_HEIGHT:
            self.snakeY = -CONS.TILE_SIZE

        elif self.snakeY < 0:
            self.snakeY = CONS.BOARD_HEIGHT

    def movement(self, event: Event) -> None:
        
        key = event.char
        if key in self.KEYS and key != self.MAP_KEY_OPP[self.lastKey]:
            self.currentKey = key

            if key == "w" and self.out_of_board():
                self.moveX = 0
                self.moveY = -1

            elif key == "s" and self.out_of_board():
                self.moveX = 0
                self.moveY = 1

            elif key == "a" and self.out_of_board():
                self.moveX = -1
                self.moveY = 0

            elif key == "d" and self.out_of_board():
                self.moveX = 1
                self.moveY = 0
    
    def out_of_board(self) -> bool:
        if not(self.snakeX>=CONS.BOARD_WIDTH) and not(self.snakeX<=0) and \
           not(self.snakeY>=CONS.BOARD_HEIGHT) and not(self.snakeY<=0):
            return True
        return False

    def drawSnake(self) -> None:
        #draw body
        for part in self.tail:
            
            self.canvas.create_rectangle(part['x'], part['y'],
                                         part['x']+CONS.TILE_SIZE,
                                         part['y']+CONS.TILE_SIZE,
                                         fill='lightgreen')

        #draw head 
        self.canvas.create_rectangle(self.snakeX, self.snakeY,
                                     self.snakeX+CONS.TILE_SIZE,
                                     self.snakeY+CONS.TILE_SIZE,
                                     fill='red')

class Game:
    def __init__(self) -> None:

        # Create Canvas
        self.canvas = Canvas(width=CONS.BOARD_WIDTH, height=CONS.BOARD_HEIGHT,
                             background='black')
        self.canvas.pack()        

        # Game objects
        self.board = Board(self.canvas)
        self.apple = Apple(self.canvas)
        self.snake = Snake(self.canvas, self.apple)
        
        bind_key = Thread(target=self.bind)
        gameLoop = Thread(target=self.gameLoop())
        bind_key.start()
        gameLoop.start()
        self.canvas.mainloop()

    def bind(self) -> None:
        self.canvas.bind_all("<KeyPress>",self.snake.movement)

    def gameLoop(self) -> None:
        if self.snake.RUN:
            self.canvas.delete(ALL)

            self.drawStaff()
            self.moveStaff()
            
            
            self.canvas.after(1000//CONS.FPS, self.gameLoop)
        else:
            self.canvas.create_text(CONS.BOARD_WIDTH//2, CONS.BOARD_HEIGHT//2, 
                                    text='GAME OVER\nScore:{}'.format(self.snake.points),
                                    font='arial 30', fill='yellow')

    def moveStaff(self) -> None:

        self.snake.moveSnake() 
        self.snake.wallColision()
        self.snake.eatFood()

    def drawStaff(self) -> None: 
        self.board.drawBoard()
        self.snake.drawSnake()
        self.apple.drawFood()

if __name__ == "__main__":
    Game()
