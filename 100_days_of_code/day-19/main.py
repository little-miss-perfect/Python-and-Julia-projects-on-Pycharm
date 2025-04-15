# from turtle import Turtle, Screen
#
# tim = Turtle()
# screen = Screen()
#
# def move_forwards():
#     tim.forward(10)
#
# def move_backwards():
#     tim.backward(10)
#
# def turn_left():
#     new_heading = tim.heading() + 10
#     tim.setheading(new_heading)
#
# def turn_right():
#     new_heading = tim.heading() - 10
#     tim.setheading(new_heading)
#
# def clear():
#     tim.clear() # just tim's lines, not everything on the screen. it clears the turtle, not the whole screen, per se
#     tim.penup()
#     tim.home()
#     tim.pendown()
#
# screen.listen()
# screen.onkey(fun = move_forwards, key = "w")
# screen.onkey(fun = move_backwards, key = "s")
# screen.onkey(fun = turn_left, key = "a")
# screen.onkey(fun = turn_right, key = "d")
# screen.onkey(fun = clear, key = "c")
# screen.exitonclick()
import turtle
#now, we'll write the code for video number "143"
#
# from turtle import Turtle, Screen
#
# screen = Screen()
# screen.setup(width=500, height=400)
# user_bet = screen.textinput(title="Make your bet", prompt="Which turtle will win the race? Enter a color: ")  # this returns a string
# colors = ["red", "orange", "yellow", "green", "blue", "purple"]
# y_positions = [-70, -40, -10, 20, 50, 80]
#
# for turtle_index in range(0, 6):  # why not use "range(len(colors))"? would that work? yes it would
#     tim = Turtle(shape="turtle")
#     tim.color(colors[turtle_index])
#     tim.penup()
#     tim.goto(x=-230, y=y_positions[turtle_index])
#
#
# screen.exitonclick()

#now, we'll write the code for video number "144"


from turtle import Turtle, Screen
import random

is_race_on = False

screen = Screen()
screen.setup(width=500, height=400)
user_bet = screen.textinput(title="Make your bet", prompt="Which turtle will win the race? Enter a color: ")  # this returns a string
colors = ["red", "orange", "yellow", "green", "blue", "purple"]
y_positions = [-70, -40, -10, 20, 50, 80]
all_turtles = []

for turtle_index in range(0, 6):  # why not use "range(len(colors))"? would that work? yes it would
    new_turtle = Turtle(shape="turtle")
    new_turtle.color(colors[turtle_index])
    new_turtle.penup()
    new_turtle.goto(x=-230, y=y_positions[turtle_index])

    all_turtles.append(new_turtle)  # so now we'll have a list of multiple turtle instances (multiple instances of these objects created from the same class); each of these instances will start off in a different state

if user_bet:
    is_race_on = True

while is_race_on:

    for turtle in all_turtles:  # first, we'll create a random distance for each turtle (this happens throughout every loop)

        if turtle.xcor() > 230:

            is_race_on = False  # but wha if two or more turtles get to the finish line at the same time? how do we code the winner?

            winning_color = turtle.pencolor()

            if winning_color == user_bet:
                print(f"You've won! The {winning_color} turtle is the winner!")
            else:
                print(f"You've lost! The {winning_color} turtle is the winner!")

        rand_distance = random.randint(0,10)  # this set is inclusive. we can get either zero or ten or any number inbetween
        turtle.forward(rand_distance)

screen.exitonclick()

# be aware of how the coordinate system works
