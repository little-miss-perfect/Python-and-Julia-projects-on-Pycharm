# from turtle import Turtle
#
# STARTING_POSITION = (0, -280)
# MOVE_DISTANCE = 10
# FINISH_LINE_Y = 280
#
#
# class Player(Turtle):
#
#     def __init__(self):
#         super().__init__()
#         self.shape("turtle")
#         self.penup()
#         self.goto(STARTING_POSITION)  # which is already defined as a tuple above
#         self.setheading(90)  # let the turtle face north when starting the game
#
#     def go_up(self):
#         self.forward(MOVE_DISTANCE)
#
#     def go_to_start(self):
#         self.goto(STARTING_POSITION)
#
#     def is_at_finish_line(self):
#         if self.ycor() > FINISH_LINE_Y:
#             return True
#         else:
#             return False

# and to avoid repetition, let's modify the following

from turtle import Turtle

STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 20
FINISH_LINE_Y = 280


class Player(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.color("white")
        self.penup()
        self.go_to_start()
        self.setheading(90)  # let the turtle face north when starting the game

    def go_up(self):
        self.forward(MOVE_DISTANCE)

    def go_to_start(self):
        self.goto(STARTING_POSITION)

    def is_at_finish_line(self):
        if self.ycor() > FINISH_LINE_Y:
            return True
        else:
            return False

