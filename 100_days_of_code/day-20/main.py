# from turtle import Screen, Turtle
#
# screen = Screen()
# screen.setup(width=600, height=600)
# screen.bgcolor("black")
# screen.title("My Snake Game")
#
# segment_1 = Turtle(shape="square")
# segment_1.color("white")
#
# segment_2 = Turtle(shape="square")
# segment_2.color("white")
# segment_2.goto(x=-20, y=0)
#
# segment_3 = Turtle(shape="square")
# segment_3.color("white")
# segment_3.goto(x=-40, y=0)
#
# screen.exitonclick()

# or we could simplify our code by writing the following

# from turtle import Screen, Turtle
#
# screen = Screen()
# screen.setup(width=600, height=600)
# screen.bgcolor("black")
# screen.title("My Snake Game")
#
# starting_positions = [(0, 0), (-20, 0), (-40, 0)]
#
# for position in starting_positions:
#     new_segment = Turtle(shape="square")
#     new_segment.color("white")
#     new_segment.goto(position)
#
# screen.exitonclick()

# now, we'll write the code for the video number "148"
#
# from turtle import Screen, Turtle
#
# screen = Screen()
# screen.setup(width=600, height=600)
# screen.bgcolor("black")
# screen.title("My Snake Game")
#
# starting_positions = [(0, 0), (-20, 0), (-40, 0)]  # we write tuples because the "goto()" method takes in the parameters "(x= x_position, y= y_position)"
# segments = []  # it'll be a list of instances of objects created from a class. these objects begin at a starting position defined by the above list
#
# # the following part of the code puts our "square objects" into their starting positions
# for position in starting_positions:
#     new_segment = Turtle(shape="square")
#     new_segment.color("white")
#     new_segment.penup()
#     new_segment.goto(position)
#     segments.append(new_segment)
#
# game_is_on = True
#
# # this part of the code moves our "square objects" from their starting positions (it moves them to the right)
# while game_is_on:
#     for seg in segments:
#         seg.forward(20)  # because each "Turtle" instance is "20" pixels long (and wide, right?)
#
# screen.exitonclick()

# the next part is to update frames
#
# from turtle import Screen, Turtle
# import time
#
# screen = Screen()
# screen.setup(width=600, height=600)
# screen.bgcolor("black")
# screen.title("My Snake Game")
# screen.tracer(0)
#
# starting_positions = [(0, 0), (-20, 0), (-40, 0)]
# segments = []
#
# for position in starting_positions:
#     new_segment = Turtle(shape="square")
#     new_segment.color("white")
#     new_segment.penup()
#     new_segment.goto(position)
#     segments.append(new_segment)
#
# game_is_on = True
#
# while game_is_on:
#     screen.update()
#     time.sleep(0.1)
#     for seg in segments:
#         seg.forward(20)  # because each "Turtle" instance is "20" pixels long (and wide, right?)
#
# screen.exitonclick()

# now, how do we move our "snake"? as in: how do we move our ENTIRE "snake"?

# from turtle import Screen, Turtle
# import time
#
# screen = Screen()
# screen.setup(width=600, height=600)
# screen.bgcolor("black")
# screen.title("My Snake Game")
# screen.tracer(0)
#
# starting_positions = [(0, 0), (-20, 0), (-40, 0)]
# segments = []
#
# for position in starting_positions:
#     new_segment = Turtle(shape="square")
#     new_segment.color("white")
#     new_segment.penup()
#     new_segment.goto(position)
#     segments.append(new_segment)
#
# game_is_on = True
#
# while game_is_on:
#     screen.update()
#     time.sleep(0.1)
#
#     for seg_num in range(len(segments) - 1, 0, -1):
#         new_x = segments[seg_num - 1].xcor()
#         new_y = segments[seg_num - 1].ycor()
#         segments[seg_num].goto(new_x, new_y)  # this makes the last segment go to the second to last segments position
#     segments[0].forward(20)
#     #segments[0].left(90)
#
# screen.exitonclick()

# now we've fixed the problem mentioned above. now the tail follows the head (and so do the objects inbetween). so let's continue

# from turtle import Screen, Turtle
# import time
#
# screen = Screen()
# screen.setup(width=600, height=600)
# screen.bgcolor("black")
# screen.title("My Snake Game")
# screen.tracer(0)
#
# starting_positions = [(0, 0), (-20, 0), (-40, 0)]
# segments = []
#
# for position in starting_positions:
#     new_segment = Turtle(shape="square")
#     new_segment.color("white")
#     new_segment.penup()
#     new_segment.goto(position)
#     segments.append(new_segment)
#
# game_is_on = True
#
# while game_is_on:
#     screen.update()
#     time.sleep(0.1)
#
#     for seg_num in range(len(segments) - 1, 0, -1):
#         new_x = segments[seg_num - 1].xcor()
#         new_y = segments[seg_num - 1].ycor()
#         segments[seg_num].goto(new_x, new_y)  # this makes the last segment go to the second to last segments position
#     segments[0].forward(20)
#
# screen.exitonclick()

# now, we'll clean up our code
#
# from turtle import Screen, Turtle
# from snake import Snake
# import time
#
# screen = Screen()
# screen.setup(width=600, height=600)
# screen.bgcolor("black")
# screen.title("My Snake Game")
# screen.tracer(0)
#
# snake = Snake()
#
# game_is_on = True
#
# while game_is_on:  # this loop is to refresh the screen
#     screen.update()
#     time.sleep(0.1)  # a delay for the screen "refresh"
#
#     snake.move()
#
# screen.exitonclick()

# now, anything (any mistake, any small modification we would like to write in the future) "snake" related can be checked in the other file. so things are more organized.
# now, let's do the next step

from turtle import Screen, Turtle
from snake import Snake
import time

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("My Snake Game")
screen.tracer(0)

snake = Snake()

screen.listen()

screen.onkey(fun=snake.up, key="Up")
screen.onkey(fun=snake.down, key="Down")
screen.onkey(fun=snake.left, key="Left")
screen.onkey(fun=snake.right, key="Right")

game_is_on = True

while game_is_on:  # this loop is to refresh the screen
    screen.update()
    time.sleep(0.1)  # a delay for the screen "refresh"

    snake.move()

screen.exitonclick()
