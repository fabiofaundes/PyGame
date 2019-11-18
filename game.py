from enum import Enum
from math import floor
from random import randint
import pygame

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
                x = initialCoordinate.getX()
                y = initialCoordinate.getY()
                self.body[i] = pygame.Rect(x, y, self.seg_size, self.seg_size)
            else:
                self.body[i] = pygame.Rect(currentX, initialCoordinate.getY(), self.seg_size, self.seg_size)
            currentX -= self.seg_size

    def incPos(self):                
        for i in range(self.size):
            index = self.size -1 - i
            if not index == 0:
                self.body[index] = self.body[index -1].copy()
            
        if self.direction == Direction.RIGHT:
            self.body[0] = self.body[0].move(self.seg_size, 0)
        elif self.direction == Direction.DOWN:
            self.body[0] = self.body[0].move(0, self.seg_size)
        elif self.direction == Direction.LEFT:
            self.body[0] = self.body[0].move(-self.seg_size, 0)
        elif self.direction == Direction.UP:
            self.body[0] = self.body[0].move(0, -self.seg_size)

    def incSize(self):                
        self.body[self.size] = self.body[self.size-1].copy()
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
    def __init__(self, screen, level):  
        self.screen = screen
        self.level = level

        #iniciação da cobra, definindo a primeira posição como o meio da tela
        self.wallOne = pygame.Rect(0, 180, 480, 10)
        self.wallTwo = pygame.Rect(330, 450, 10, 150)
        self.wallThree = pygame.Rect(330, 450, 250, 10)

        self.initialCoordinate = Coordinate(floor(self.WIDTH/2)-self.SEG_SIZE, floor(self.HEIGHT/2)-self.SEG_SIZE)
        self.snake = Snake(10, Direction.RIGHT, self.initialCoordinate, self.SEG_SIZE)
        self.food = None
        self.generateFood()

    def generateFood(self):
        while(not self.foodValid()):
            x = randint(1, self.WIDTH/self.SEG_SIZE - 2)
            y = randint(1, self.HEIGHT/self.SEG_SIZE - 2)
            self.food = pygame.Rect(x*self.SEG_SIZE, y*self.SEG_SIZE, self.SEG_SIZE, self.SEG_SIZE)


    def foodValid(self):
        if self.food is None:
            return False

        for i in range(self.snake.getSize()):
            if(self.food.__eq__(self.snake.getSegment(i))):
                return False

        if self.level == 2:
            if(self.food.__eq__(self.wallOne)):
                return False
            if(self.food.__eq__(self.wallTwo)):
                return False
            if(self.food.__eq__(self.wallThree)):
                return False

        return True    

    def drawSnake(self):
        for i in range(self.snake.getSize()):            
            pygame.draw.rect(self.screen, (255,255,255), self.snake.getSegment(i))

    def drawFood(self):        
        pygame.draw.rect(self.screen,(255, 0, 0), self.food)

    def drawBackground(self):
        self.screen.fill((0,0,0))
        if self.level == 2:
            pygame.draw.rect(self.screen,(255, 255, 255), self.wallOne)
            pygame.draw.rect(self.screen,(255, 255, 255), self.wallTwo)
            pygame.draw.rect(self.screen,(255, 255, 255), self.wallThree)

    def checkCollision(self):
        head = self.snake.getSegment(0)
        for i in range(self.snake.getSize()):
            if not i == 0:
                if self.snake.getSegment(i).colliderect(head):
                    return True

        if(head.left < 0):
            return True
        if(head.left > self.WIDTH-self.SEG_SIZE):
            return True
        if(head.top < 0):
            return True
        if(head.top > self.HEIGHT-self.SEG_SIZE):
            return True

        if self.level == 2:
            if self.wallOne.colliderect(head):
                return True
            if self.wallTwo.colliderect(head):
                return True
            if self.wallThree.colliderect(head):
                return True

        return False

    def checkFood(self):
        head = self.snake.getSegment(0)
        if head.colliderect(self.food):
            return True

    def printScreen(self, txt, x, y):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(txt, True, (255,255,255), (0,0,0))
        textRect = text.get_rect()
        textRect.center = (x, y)
        self.screen.blit(text, textRect)

def levelOne(screen):
    over = False
    winn = False
    points = 0

    game = App(screen, 1)

    while not winn and not over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                over = True

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_UP]:
            if not game.snake.direction == Direction.DOWN:
                game.snake.changeDir(Direction.UP)
        elif key_pressed[pygame.K_DOWN]:
            if not game.snake.direction == Direction.UP:
                game.snake.changeDir(Direction.DOWN)
        elif key_pressed[pygame.K_RIGHT]:
            if not game.snake.direction == Direction.LEFT:
                game.snake.changeDir(Direction.RIGHT)
        elif key_pressed[pygame.K_LEFT]:
            if not game.snake.direction == Direction.RIGHT:
                game.snake.changeDir(Direction.LEFT)

        game.snake.incPos()
        game.drawBackground()
        game.drawFood()
        game.drawSnake()
        game.printScreen(str(points),20,20)
        game.printScreen('Level 1',300,20)
        pygame.display.flip()

        over = game.checkCollision()        
        if game.checkFood():
            game.snake.incSize()
            game.generateFood()
            points += 1
            if points == 1:
                winn = True

        clock.tick(15)
    
    return winn

def levelTwo(screen):
    over = False
    winn = False
    points = 0

    game = App(screen, 2)

    while not winn and not over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                over = True

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_UP]:
            if not game.snake.direction == Direction.DOWN:
                game.snake.changeDir(Direction.UP)
        elif key_pressed[pygame.K_DOWN]:
            if not game.snake.direction == Direction.UP:
                game.snake.changeDir(Direction.DOWN)
        elif key_pressed[pygame.K_RIGHT]:
            if not game.snake.direction == Direction.LEFT:
                game.snake.changeDir(Direction.RIGHT)
        elif key_pressed[pygame.K_LEFT]:
            if not game.snake.direction == Direction.RIGHT:
                game.snake.changeDir(Direction.LEFT)

        game.snake.incPos()
        game.drawBackground()
        game.drawFood()
        game.drawSnake()
        game.printScreen(str(points),20,20)
        game.printScreen('Level 2',300,20)
        pygame.display.flip()

        over = game.checkCollision()        
        if game.checkFood():
            game.snake.incSize()
            game.generateFood()
            points += 1
            if points == 10:
                winn = True

        clock.tick(15)

    return winn

def endScreen(screen):
    over = False
    quitGame = False
    game = App(screen, 0)

    while not quitGame and not over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                over = True

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_BACKSPACE]:
            quitGame = True
        elif key_pressed[pygame.K_SPACE]:
            over = True

        game.drawBackground()
        game.printScreen('Game Over',300,20)
        game.printScreen('Press [BACKSPACE] to quit',300,200)
        game.printScreen('Press [SPACE] to restart',300,300)
        pygame.display.flip()

        clock.tick(15)

    return quitGame


pygame.init()
screen = pygame.display.set_mode((600,600))

clock = pygame.time.Clock()

win2 = False
quitGame = False
while not quitGame:
    winn = levelOne( screen)
    
    if winn:
        win2 = levelTwo( screen)

    quitGame = endScreen(screen)