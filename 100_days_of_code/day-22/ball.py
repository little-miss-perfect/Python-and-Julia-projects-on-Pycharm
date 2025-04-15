# from turtle import Turtle
#
# class Ball(Turtle):
#
#     def __init__(self):
#         super().__init__()
#         self.color('white')
#         self.shape('circle')  # or make it a square if you want
#         self.penup()
#
#     def move(self):
#         new_x = self.xcor() + 10
#         new_y = self.ycor() + 10
#         self.goto(new_x, new_y)

# now... how do we detect a collision? first, with the wall
#
# from turtle import Turtle
#
# class Ball(Turtle):
#
#     def __init__(self):
#         super().__init__()
#         self.color('white')
#         self.shape('circle')  # or make it a square if you want
#         self.penup()
#         self.x_move = 10
#         self.y_move = 10
#
#     def move(self):
#         new_x = self.xcor() + self.x_move
#         new_y = self.ycor() + self.y_move
#         self.goto(new_x, new_y)
#
#     def bounce(self):
#         self.y_move *= -1  # this will reverse the "direction". genius
#

# now... how do we detect a collision? now, with the paddle

# from turtle import Turtle
#
# class Ball(Turtle):
#
#     def __init__(self):
#         super().__init__()
#         self.color('white')
#         self.shape('circle')  # or make it a square if you want
#         self.penup()
#         self.x_move = 10
#         self.y_move = 10
#
#     def move(self):
#         new_x = self.xcor() + self.x_move
#         new_y = self.ycor() + self.y_move
#         self.goto(new_x, new_y)
#
#     def bounce_y(self):
#         self.y_move *= -1
#
#     def bounce_x(self):
#         self.x_move *= -1

# now... how do we detect the ball going past the screen?
#
# from turtle import Turtle
#
# class Ball(Turtle):
#
#     def __init__(self):
#         super().__init__()
#         self.color('white')
#         self.shape('circle')  # or make it a square if you want
#         self.penup()
#         self.x_move = 10
#         self.y_move = 10
#
#     def move(self):
#         new_x = self.xcor() + self.x_move
#         new_y = self.ycor() + self.y_move
#         self.goto(new_x, new_y)
#
#     def bounce_y(self):
#         self.y_move *= -1
#
#     def bounce_x(self):
#         self.x_move *= -1
#
#     def reset_position(self):
#         self.goto(0, 0)
#         self.bounce_x()  # to reverse the "direction" of the ball (these are just game rules)
#         # maybe we should add a similar line of code so that the "y" coordinate "reverses" randomly

# and... how could you increase the speed of the ball everytime it hits a paddle?

from turtle import Turtle

class Ball(Turtle):

    def __init__(self):
        super().__init__()
        self.color('white')
        self.shape('turtle')
        self.penup()
        self.x_move = 10
        self.y_move = 10
        self.move_speed = 0.1  # we'll start with the ball moving relatively slow. genius. and everytime a ball bounces in the "x" direction, it'll mean that it's touched a paddle. so we need to modify something in the "bounce_x" method.

    def move(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        self.y_move *= -1

    def bounce_x(self):
        self.x_move *= -1
        self.move_speed *= 0.9  # values less than one will increase the speed every time. but his can't go on indefinitely. it needs to restart once someone scores. so let's modify the method "reset_position"

    def reset_position(self):
        self.goto(0, 0)
        self.move_speed = 0.1  # and we need to do this before bouncing the ball (i.e. changing its direction), right?
        self.bounce_x()
