# from turtle import Turtle
#
# STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]  # because in Python, constants are named with all caps and are separated by "snake case" ("_")
# MOVE_DISTANCE = 20
#
# class Snake:
#
#     def __init__(self):
#
#         self.segments = []  # an attribute
#         self.create_snake()  # a method. this creates a "three segment snake"
#
#     def create_snake(self):
#
#         for position in STARTING_POSITIONS:
#             new_segment = Turtle(shape="square")
#             new_segment.color("white")
#             new_segment.penup()
#             new_segment.goto(position)
#             self.segments.append(new_segment)
#
#     def move(self):
#         for seg_num in range(len(self.segments) - 1, 0, -1):  # so... for each part of the snake's body, we'll get the "n-th" part to follow the "(n-1)th part" from "back to front (i.e. head)". this is genius
#             new_x = self.segments[seg_num - 1].xcor()
#             new_y = self.segments[seg_num - 1].ycor()
#             self.segments[seg_num].goto(new_x,
#                                    new_y)  # this makes the last segment go to the second to last segments position
#         self.segments[0].forward(MOVE_DISTANCE)
#
#     # for these next methods, you only need to control the movement of "the head of the snake"; this is due to the fact that in the previous method called "move", we ensured that the tail follows the head.
#     def up(self):
#         self.segments[0].setheading(90)
#
#     def down(self):
#         pass
#
#     def left(self):
#         pass
#
#     def right(self):
#         pass

#  since we're using a lot the "head of the snake", we should create an attribute for each object.

# from turtle import Turtle
#
# STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]  # because in Python, constants are named with all caps and are separated by "snake case" ("_")
# MOVE_DISTANCE = 20
#
# class Snake:
#
#     def __init__(self):
#
#         self.segments = []  # an attribute
#         self.create_snake()  # a method. this creates a "three segment snake"
#         self.head = self.segments[0]  # it's important to put this attribute here and not after "self.segments". because if we put this line after "self.segments", the next line is "self.create_snake()", so by this point, we'll have asked the class to get the "head" of the snake before it's created a snake... and therefore a head! so let's keep this line after writing "self.create_snake()"
#
#     def create_snake(self):
#
#         for position in STARTING_POSITIONS:
#             new_segment = Turtle(shape="square")
#             new_segment.color("white")
#             new_segment.penup()
#             new_segment.goto(position)
#             self.segments.append(new_segment)
#
#     def move(self):
#         for seg_num in range(len(self.segments) - 1, 0, -1):  # so... for each part of the snake's body, we'll get the "n-th" part to follow the "(n-1)th part" from "back to front (i.e. head)". this is genius
#             new_x = self.segments[seg_num - 1].xcor()
#             new_y = self.segments[seg_num - 1].ycor()
#             self.segments[seg_num].goto(new_x,
#                                    new_y)  # this makes the last segment go to the second to last segments position
#         self.head.forward(MOVE_DISTANCE)
#
#     # for these next methods, you only need to control the movement of "the head of the snake"; this is due to the fact that in the previous method called "move", we ensured that the tail follows the head.
#     def up(self):
#         self.head.setheading(90)
#
#     def down(self):
#         self.head.setheading(270)
#
#     def left(self):
#         self.head.setheading(180)
#
#     def right(self):
#         self.head.setheading(0)

# and we're closer! the problem now... is that in the original game, the snake isn't allowed to "turn in on itself" (i.e. if it's moving up, you can't make it move down immediately without it going through itself -again, these are just rules from the original game)

# from turtle import Turtle
# 
# STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]  # because in Python, constants are named with all caps and are separated by "snake case" ("_")
# MOVE_DISTANCE = 20
# 
# UP = 90
# DOWN = 270
# LEFT = 180
# RIGHT = 0
# 
# class Snake:
# 
#     def __init__(self):
# 
#         self.segments = []  # an attribute
#         self.create_snake()  # a method. this creates a "three segment snake"
#         self.head = self.segments[0]  # it's important to put this attribute here and not after "self.segments". because if we put this line after "self.segments", the next line is "self.create_snake()", so by this point, we'll have asked the class to get the "head" of the snake before it's created a snake... and therefore a head! so let's keep this line after writing "self.create_snake()"
# 
#     def create_snake(self):
# 
#         for position in STARTING_POSITIONS:
#             new_segment = Turtle(shape="square")
#             new_segment.color("white")
#             new_segment.penup()
#             new_segment.goto(position)
#             self.segments.append(new_segment)
# 
#     def move(self):
#         for seg_num in range(len(self.segments) - 1, 0, -1):  # so... for each part of the snake's body, we'll get the "n-th" part to follow the "(n-1)th part" from "back to front (i.e. head)". this is genius
#             new_x = self.segments[seg_num - 1].xcor()
#             new_y = self.segments[seg_num - 1].ycor()
#             self.segments[seg_num].goto(new_x,
#                                    new_y)  # this makes the last segment go to the second to last segments position
#         self.head.forward(MOVE_DISTANCE)
# 
#     # for these next methods, you only need to control the movement of "the head of the snake"; this is due to the fact that in the previous method called "move", we ensured that the tail follows the head.
#     def up(self):
#         if self.head.heading() != DOWN:  # careful because it's not "self.head.heading", it's "self.head.heading()".
#             self.head.setheading(UP)
# 
#     def down(self):
#         if self.head.heading() != UP:
#             self.head.setheading(DOWN)
# 
#     def left(self):
#         if self.head.heading() != RIGHT:
#             self.head.setheading(LEFT)
# 
#     def right(self):
#         if self.head.heading() != LEFT:
#             self.head.setheading(RIGHT)

# and now, we can continue programming our game.

from turtle import Turtle

# STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]  # because in Python, constants are named with all caps and are separated by "snake case" ("_")
# MOVE_DISTANCE = 20
#
# UP = 90
# DOWN = 270
# LEFT = 180
# RIGHT = 0
#
# class Snake:
#
#     def __init__(self):
#
#         self.segments = []  # an attribute
#         self.create_snake()  # a method. this creates a "three segment snake"
#         self.head = self.segments[0]  # it's important to put this attribute here and not after "self.segments". because if we put this line after "self.segments", the next line is "self.create_snake()", so by this point, we'll have asked the class to get the "head" of the snake before it's created a snake... and therefore a head! so let's keep this line after writing "self.create_snake()"
#
#     def create_snake(self):
#
#         for position in STARTING_POSITIONS:
#             new_segment = Turtle(shape="square")
#             new_segment.color("white")
#             new_segment.penup()
#             new_segment.goto(position)
#             self.segments.append(new_segment)
#
#     def move(self):
#         for seg_num in range(len(self.segments) - 1, 0, -1):  # so... for each part of the snake's body, we'll get the "n-th" part to follow the "(n-1)th part" from "back to front (i.e. head)". this is genius
#             new_x = self.segments[seg_num - 1].xcor()
#             new_y = self.segments[seg_num - 1].ycor()
#             self.segments[seg_num].goto(new_x,
#                                    new_y)  # this makes the last segment go to the second to last segments position
#         self.head.forward(MOVE_DISTANCE)
#
#     # for these next methods, you only need to control the movement of "the head of the snake"; this is due to the fact that in the previous method called "move", we ensured that the tail follows the head.
#     def up(self):
#         if self.head.heading() != DOWN:  # careful because it's not "self.head.heading", it's "self.head.heading()".
#             self.head.setheading(UP)
#
#     def down(self):
#         if self.head.heading() != UP:
#             self.head.setheading(DOWN)
#
#     def left(self):
#         if self.head.heading() != RIGHT:
#             self.head.setheading(LEFT)
#
#     def right(self):
#         if self.head.heading() != LEFT:
#             self.head.setheading(RIGHT)

# now... how do we detect a collision with our own tail?

from turtle import Turtle

STARTING_POSITIONS = [(0, 0), (-20, 0), (-40, 0)]  # because in Python, constants are named with all caps and are separated by "snake case" ("_")
MOVE_DISTANCE = 20

UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0

class Snake:

    def __init__(self):

        self.segments = []  # an attribute
        self.create_snake()  # a method. this creates a "three segment snake"
        self.head = self.segments[0]  # it's important to put this attribute here and not after "self.segments". because if we put this line after "self.segments", the next line is "self.create_snake()", so by this point, we'll have asked the class to get the "head" of the snake before it's created a snake... and therefore a head! so let's keep this line after writing "self.create_snake()"

    def create_snake(self):

        for position in STARTING_POSITIONS:
            self.add_segment(position)

    def add_segment(self, position):
        new_segment = Turtle(shape="square")
        new_segment.color("white")
        new_segment.penup()
        new_segment.goto(position)
        self.segments.append(new_segment)

    def extend(self):
        self.add_segment(self.segments[-1].position())  # think about this for a while. it does... make sense, right?

    def move(self):
        for seg_num in range(len(self.segments) - 1, 0, -1):  # so... for each part of the snake's body, we'll get the "n-th" part to follow the "(n-1)th part" from "back to front (i.e. head)". this is genius
            new_x = self.segments[seg_num - 1].xcor()
            new_y = self.segments[seg_num - 1].ycor()
            self.segments[seg_num].goto(new_x,
                                   new_y)  # this makes the last segment go to the second to last segments position
        self.head.forward(MOVE_DISTANCE)

    def up(self):
        if self.head.heading() != DOWN:  # careful because it's not "self.head.heading", it's "self.head.heading()".
            self.head.setheading(UP)

    def down(self):
        if self.head.heading() != UP:
            self.head.setheading(DOWN)

    def left(self):
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)

    def right(self):
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)
