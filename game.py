import turtle
from turtle import Screen
import random
import math 
import time

HEIGHT =  1
SPEED = 1
SCORE = 0

# Screen 

win = Screen()
win.title("Reinforcement Snake Game")

# food 

food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.shapesize(0.50, 0.50)
x , y = random.randint(-290,290) , random.randint(-290,290)
food.goto(x,y)


# Snake 

snake = turtle.Turtle()
snake.turtlesize(0.6,1)
snake.shape("square")
snake.speed(0)
snake.penup()
snake.setposition(0,-300)
snake.pencolor("blue")
snake.pensize(3)
snake.speed(1)
snake.setheading(90)


# Border ; 600 * 600 px
border = turtle.Turtle()
border.pensize(4)
border.speed(0)
border.hideturtle()
border.penup()
border.setposition(-300,-300)
border.pendown()

# Pen

pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("black")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0", align="center", font=("Courier", 24, "normal"))

for _ in range(4):
    border.forward(600)
    border.left(90)

turtle.listen()

def moveright():
    if int(snake.heading()) != 180:
        snake.setheading(0)


def moveleft():
    if int(snake.heading()) != 0:
        snake.setheading(180)

def movetop():
    if int(snake.heading()) != 270:
        snake.setheading(90)

def movebottom():
    if int(snake.heading()) != 90:
        snake.setheading(270)


def move():
    if snake.heading() == 90:
        y = snake.ycor() #y coordinate of the turtle
        snake.sety(y + 20)
 
    if snake.heading() == 270:
        y = snake.ycor() #y coordinate of the turtle
        snake.sety(y - 20)
 
    if snake.heading() == 0:
        x = snake.xcor() #y coordinate of the turtle
        snake.setx(x + 20)
 
    if snake.heading() == 180:
        x = snake.xcor() #y coordinate of the turtle
        snake.setx(x - 20)


while True:
    win.update()
    move()
    turtle.listen()
    turtle.onkey(movetop , 'w')
    turtle.onkey(moveleft , 'a')
    turtle.onkey(moveright , 'd')
    turtle.onkey(movebottom , 's')
    snake.speed(SPEED)
    snake.turtlesize(0.6,HEIGHT)



    if snake.pos()[0] - 15 < x < snake.pos()[0] + 15 and snake.pos()[1] - 15 < y < snake.pos()[1] + 15:
        SPEED += 0.1
        food.hideturtle()
        x , y = random.randint(-290,290) , random.randint(-290,290)
        food.goto(x,y)
        food.showturtle()
        SCORE += 1
        pen.clear()
        pen.write("Score: {}".format(SCORE), align="center", font=("Courier", 24, "normal")) 

    
    if snake.xcor() >= 300 or snake.xcor() <= -300 or snake.ycor() >= 300 or snake.ycor() <= -300:
        break



turtle.mainloop()