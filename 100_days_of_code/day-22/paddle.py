# from turtle import Turtle
#
# class Paddle(Turtle):  # we need this class to inherit from the "Turtle" class
#
#     def __init__(self, position):
#         super().__init__()  # we need to initialize the class we're inheriting from
#
#         self.shape("square")
#         self.color("white")
#         self.shapesize(stretch_wid=5, stretch_len=1)
#         self.penup()
#         self.goto(position)
#
#
#     def go_up(self):
#         new_y = self.ycor() + 20
#         self.goto(x=self.xcor(), y=new_y)
#
#     def go_down(self):
#         new_y = self.ycor() - 20
#         self.goto(x=self.xcor(), y=new_y)

# now, what about the "ball"?

# from turtle import Turtle
#
# class Paddle(Turtle):  # we need this class to inherit from the "Turtle" class
#
#     def __init__(self, position):
#         super().__init__()  # we need to initialize the class we're inheriting from
#
#         self.shape("square")
#         self.color("white")
#         self.shapesize(stretch_wid=5, stretch_len=1)
#         self.penup()
#         self.goto(position)
#
#     def go_up(self):
#         new_y = self.ycor() + 20
#         self.goto(x=self.xcor(), y=new_y)
#
#     def go_down(self):
#         new_y = self.ycor() - 20
#         self.goto(x=self.xcor(), y=new_y)

# now... how do we prevent the paddle from moving out of the screen (it does this vertically). we don't really need this for the program to work, but it'd be nice to have it, right?

from turtle import Turtle

class Paddle(Turtle):  # we need this class to inherit from the "Turtle" class

    def __init__(self, position):
        super().__init__()  # we need to initialize the class we're inheriting from

        self.shape("square")
        self.color("white")
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.penup()
        self.goto(position)

    def go_up(self):
        if self.ycor() < 260:  # just like what we did in the "snake game" so that the snake didn't "move into itself"
            new_y = self.ycor() + 20
            self.goto(x=self.xcor(), y=new_y)

    def go_down(self):
        if self.ycor() > -260:  # careful, remember that we want this "if" statement to allow us to move if we haven't yet reached the bottom of the screen
            new_y = self.ycor() - 20
            self.goto(x=self.xcor(), y=new_y)
