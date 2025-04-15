# from turtle import Turtle
# import random
#
# class Food(Turtle):
#
#     def __init__(self):
#         super().__init__()
#         self.shape("circle")
#         self.penup()
#         self.shapesize(stretch_len=0.5,stretch_wid=0.5)
#         self.color("blue")
#         self.speed("fastest")
#         random_x = random.randint(-280, 280)
#         random_y = random.randint(-280, 280)
#         self.goto(random_x, random_y)
#         self.refresh()  # so it's initialized with this random location? but it's not sent to this random location. hmmm... are we misunderstanding this?
#
#     def refresh(self):
#         random_x = random.randint(-280, 280)
#         random_y = random.randint(-280, 280)
#         self.goto(random_x, random_y)

# now, the next modification

from turtle import Turtle
import random

class Food(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len=0.5,stretch_wid=0.5)
        self.color("blue")
        self.speed("fastest")
        random_x = random.randint(-280, 280)
        random_y = random.randint(-280, 280)
        self.goto(random_x, random_y)
        self.refresh()  # so it's initialized with this random location? but it's not sent to this random location. hmmm... are we misunderstanding this?

    def refresh(self):
        random_x = random.randint(-280, 280)
        random_y = random.randint(-280, 280)
        self.goto(random_x, random_y)
