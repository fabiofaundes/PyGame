from tkinter import *
from enum import Enum
from math import floor
from random import randint
from time import sleep as sleep

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class Coordinate(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def getX(self):        
        return self.x

    def getY(self):       
        return self.y

    def __str__(self):
        return '<' + str(self.getX()) + ',' + str(self.getY()) + '>'
    
    def __eq__(self, other):
        return self.y == other.y and self.x == other.x
    
    def __repr__(self):
        return "Coordinate(%d, %d)" % (self.x, self.y)

class Snake:    
    def __init__(self, size, direction, initialCoordinate, seg_size):
        self.size = size
        self.direction = direction
        self.seg_size = seg_size

        self.body = [None] * 1000
        currentX = initialCoordinate.getX()
        for i in range(self.size):
            if i == 0:
                self.body[i] = initialCoordinate
            else:
                self.body[i] = Coordinate(currentX, initialCoordinate.getY())
            currentX -= self.seg_size

    def incPos(self):        
        if self.direction == Direction.RIGHT:
            self.body[0] = Coordinate(self.body[0].getX()+self.seg_size, self.body[0].getY())
        elif self.direction == Direction.DOWN:
            self.body[0] = Coordinate(self.body[0].getX(), self.body[0].getY()+self.seg_size)
        elif self.direction == Direction.LEFT:
            self.body[0] = Coordinate(self.body[0].getX()-self.seg_size, self.body[0].getY())
        elif self.direction == Direction.TOP:
            self.body[0] = Coordinate(self.body[0].getX(), self.body[0].getY()-self.seg_size)

        for i in range(self.size):
            if i != 0:
                self.body[i] = Coordinate(self.body[i-1].getX(), self.body[i-1].getY())

    def incSize(self):        
        lastSeg = self.body[self.size-1]
        self.body[self.size] = Coordinate(lastSeg.getX(), lastSeg.getY())
        self.incPos()
        self.size += 1

    def changeDir(self, direction):
        self.direction = direction

    def getSegment(self, index):
        return self.body[index]
    
    def getSize(self):
        return self.size

#Classe para gerenciar o jogo e a tela
class App:
    #Constantes de configuração do jogo
    WIDTH = 600
    HEIGHT = 600    
    SEG_SIZE = 10 #Tamanho de cada quadrado
    def __init__(self, master=None):
        
        self.wdg1 = Frame(master)
        self.wdg1.pack(fill='both', expand=True)

        self.wdg1.canvas = Canvas(master, width=self.WIDTH, height=self.HEIGHT, bd=5, bg="black")
        self.wdg1.canvas.pack()

        #iniciação da cobra, definindo a primeira posição como o meio da tela
        self.initialCoordinate = Coordinate(floor(self.WIDTH/2)-self.SEG_SIZE, floor(self.HEIGHT/2)-self.SEG_SIZE)
        self.snake = Snake(10, Direction.RIGHT, self.initialCoordinate, self.SEG_SIZE)
        self.food = None
        self.generateFood()        

        #desenha tudo na tela
        self.drawBackground()
        self.drawSnake()
        self.drawFood()

    def generateFood(self):
        while(not self.foodValid()):
            x = randint(1, self.WIDTH/self.SEG_SIZE - 2)
            y = randint(1, self.HEIGHT/self.SEG_SIZE - 2)
            self.food = Coordinate(x*self.SEG_SIZE, y*self.SEG_SIZE)


    def foodValid(self):
        if self.food is None:
            return False

        for i in range(self.snake.getSize()):
            if(self.food.__eq__(self.snake.getSegment(i))):
                return False

        return True    

    def drawSnake(self):
        for i in range(self.snake.getSize()):
            x = self.snake.getSegment(i).getX()
            y = self.snake.getSegment(i).getY()
            self.wdg1.canvas.create_rectangle(x, y, x+self.SEG_SIZE, y+self.SEG_SIZE, fill='white', outline='white')

    def drawFood(self):
        x = self.food.getX()
        y = self.food.getY()
        self.wdg1.canvas.create_rectangle(x, y, x+self.SEG_SIZE, y+self.SEG_SIZE, fill='red', outline='red')

    def drawBackground(self):
        self.wdg1.canvas.create_rectangle(0,0,self.WIDTH,self.HEIGHT, fill='black', outline='white')              

root = Tk()
root.geometry("600x600")
root.resizable(0, 0)
app = App(root)

def gameloop():
    sleep(100)
    app.snake.incPos()
    app.drawBackground()
    app.drawFood()
    app.drawSnake()
    root.after(100, gameloop())

root.after(1000, gameloop())
root.mainloop()

    