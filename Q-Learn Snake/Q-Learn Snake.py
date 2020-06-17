import numpy as np
import pickle
import turtle
from turtle import Screen
import time 
import random
import math


# For enviornment

LEARNING_RATE = 0.1
EPOCHS = 25000
DISCOUNT = 0.95
STOP_PENALTY = -20
CORRECT_MOVE_REWARD = 10
WRONG_MOVE_PENALTY = -10
FOOD_REWARD = 100
SHOW_EVERY = 3000

# For snake


HEIGHT =  1
SPEED = 1
SCORE = 0

start_q_table = None


class Border(turtle.Turtle):
    def __init__(self):

        self.border = turtle.Turtle()
        self.border.pensize(4)
        self.border.speed(0)
        self.border.hideturtle()
        self.border.penup()
        self.border.setposition(-200,-200)
        self.border.pendown()

        for _ in range(4):
            self.border.forward(400)
            self.border.left(90)


class Score(turtle.Turtle):
    def __init__(self):
        self.SCORE = 0
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.speed(0)
        self.pen.shape("square")
        self.pen.color("black")
        self.pen.penup()
        self.pen.goto(0, 160)
        self.pen.write(f"Score: {self.SCORE}", align="center", font=("Courier", 14, "normal"))

    def _updatescore(self):
        self.SCORE += 1
        self.pen.clear()
        self.pen.write(f"Score: {self.SCORE}", align="center", font=("Courier",14, "normal"))


class Food(turtle.Turtle):
    def __init__(self):
        self.food = turtle.Turtle()
        self.food.speed(0)
        self.food.shape("circle")
        self.food.color("red")
        self.food.penup()
        self.food.shapesize(0.50, 0.50)
        self.x = random.randint(-190,190)
        self.y = random.randint(-190,190)
        self.food.goto(self.x,self.y)

    def getx(self):
        """

        Returns the x coordinate of the snake

        """
        return self.x

    def gety(self):
        """

        Returns the y coordinate of the snake

        """
        return self.y

    def getcor(self):
        """

        Returns the coordinates of the snake

        """
        return (self.x , self.y)

    def _update(self):
        self.food.hideturtle()
        self.x = random.randint(-190,190)
        self.y = random.randint(-190,190)
        self.food.goto(self.x,self.y)
        self.food.showturtle()



    def __str__(self):
        print(f"Location of food : {self.x , self.y}")
    
    def __repr__(self):
        print(f"Location of food : {self.x , self.y}")


class Snake(turtle.Turtle):
    def __init__(self):
        self.speed = 0
        self.snake = turtle.Turtle()
        self.snake.turtlesize(0.5,1)
        self.snake.shape("square")
        self.snake.speed(self.speed)
        self.snake.penup()
        self.x = random.randint(-200,200)
        self.y = random.randint(-200,200)
        self.snake.setposition(self.x , self.y)
        self.snake.pencolor("blue")
        self.snake.pensize(3)
        self.snake.speed(1)
        self.snake.setheading(90)
        self.new_x = self.x
        self.new_y = self.y
    
    def action(self , choice):
        """
        
        Gives us total 4 total movement options (0,1,2,3)
        0 : top
        1 : right
        2 : bottom
        3 : left
        
        """

        if choice == 0:
            if int(self.snake.heading()) != 270:
                self.snake.setheading(90)
                self.move(y = 27)

        elif choice ==  1:
            if int(self.snake.heading()) != 180:
                self.snake.setheading(0)
                self.move(x = 27)

        elif choice ==  2:
            if int(self.snake.heading()) != 90:
                self.snake.setheading(270)
                self.move(y = -27)

        elif choice ==  3:
            if int(self.snake.heading()) != 0:
                self.snake.setheading(180)
                self.move(x = -27)

    def move(self , x = False , y = False):

        if x != False:
            self.snake.setx(self.x + x)
            self.x += x
        elif y != False:
            self.snake.sety(self.y + y)
            self.y += y

        # If snake is out of bounds

        if self.x <= -200:
            self.x = -200
        elif self.x >= 200:
            self.x = 200
        if self.y <= -200:
            self.y = -200
        elif self.y >= 200:
            self.y = 200

    def getx(self):
        """

        Returns the x coordinate of the snake

        """
        return self.x

    def gety(self):
        """

        Returns the y coordinate of the snake

        """
        return self.y

    def getcor(self):
        """

        Returns the coordinates of the snake

        """
        return (self.x , self.y)
    

    def __str__(self):
        print(f"Location of Snake : {self.x , self.y}")

    def __repr__(self):
        print(f"Location of Snake : {self.x , self.y}")


if start_q_table == None:
    q_table = {} # {(x1,y1) : [random_vales_of_reward],{} ...}
    for x1 in range(-400,400):
        for x2 in range(-400,400):
            q_table[(x1,x2)] = [np.random.uniform(-5,0) for _ in range(4)]
else:
    with open(start_q_table , 'rb') as f:
        q_table = pickle.load(f)

border = Border()
food = Food()
snake = Snake()
score = Score()

for episode in range(EPOCHS):
    init_distance = math.sqrt((food.x - snake.x)**2 + (food.y - snake.y)**2)

    obs = (food.x - snake.x , food.y - snake.y)
    action = np.argmax(q_table[obs])
    snake.action(action)

    new_distance = math.sqrt((food.x - snake.x)**2 + (food.y - snake.y)**2)


    if snake.x - 15 < food.x < snake.x + 15 and snake.y - 15 < food.y < snake.y + 15:
        reward = FOOD_REWARD
    elif init_distance  > new_distance:
        reward = CORRECT_MOVE_REWARD
    elif new_distance >= init_distance:
        reward = WRONG_MOVE_PENALTY
    else:
        reward = STOP_PENALTY

    new_obs = (food.x- snake.x , food.y - snake.y)
    max_future_q = np.max(q_table[new_obs])
    current_q = q_table[obs][action]


    if reward == FOOD_REWARD:
        new_q = FOOD_REWARD
    else:
        new_q = (1-LEARNING_RATE)*current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q) # q learn formula
    
    q_table[obs][action] = new_q

    if reward == FOOD_REWARD:
        print(f"Success in epoch : {episode}")
        score._updatescore()
        food._update()

        

with open("qtable-.pickle", "wb") as f:
    pickle.dump(q_table, f)