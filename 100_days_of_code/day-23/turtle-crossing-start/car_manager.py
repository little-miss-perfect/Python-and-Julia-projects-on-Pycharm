# from turtle import Turtle
# import random
#
# COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
# STARTING_MOVE_DISTANCE = 5
# MOVE_INCREMENT = 10
#
#
# class CarManager(Turtle):
#
#     def __init__(self):
#         super().__init__()
#         self.all_cars = []  # remember that its elements are all turtles (square shaped "turtle objects")
#         self.car_speed = STARTING_MOVE_DISTANCE
#
#     def create_car(self):
#         random_chance = random.randint(1, 6)
#         if random_chance == 1:  # so that we don't get too many cars being generated. if that weren't a problem, then we'd just remove this "if" statement
#             new_car = Turtle("square")
#             new_car.shapesize(stretch_wid=1, stretch_len=2)  # so that the "cars" are the right shape
#             new_car.penup()
#             new_car.color(random.choice(COLORS))
#             random_y = random.randint(-250, 250)
#             new_car.goto(300, random_y)
#             self.all_cars.append(new_car)
#
#     def move_cars(self):
#         for car in self.all_cars:
#             car.backward(self.car_speed)  # we inherit the method "backward" from the "Turtle" class

# now... how do we control the car speed?

# from turtle import Turtle
# import random
#
# COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
# STARTING_MOVE_DISTANCE = 5
# MOVE_INCREMENT = 10
#
#
# class CarManager(Turtle):
#
#     def __init__(self):
#         super().__init__()
#         self.all_cars = []  # remember that its elements are all turtles (square shaped "turtle objects")
#         self.car_speed = STARTING_MOVE_DISTANCE
#
#     def create_car(self):
#         random_chance = random.randint(1, 6)
#         if random_chance == 1:  # so that we don't get too many cars being generated. if that weren't a problem, then we'd just remove this "if" statement
#             new_car = Turtle("square")
#             new_car.shapesize(stretch_wid=1, stretch_len=2)  # so that the "cars" are the right shape
#             new_car.penup()
#             new_car.color(random.choice(COLORS))
#             random_y = random.randint(-250, 250)
#             new_car.goto(300, random_y)
#             self.all_cars.append(new_car)
#
#     def move_cars(self):
#         for car in self.all_cars:
#             car.backward(self.car_speed)
#
#     def level_up(self):
#         self.car_speed += MOVE_INCREMENT  # every frame the cars will move "backwards" further each time we level up. if you took a video with a fixed frame rate, and recorded a bunch of cars, this would be the definition of increasing their speed. think about it; it makes sense this way

# now... what about the scoreboard?

from turtle import Turtle
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10


class CarManager(Turtle):

    def __init__(self):
        super().__init__()
        self.all_cars = []  # remember that its elements are all turtles (square shaped "turtle objects")
        self.car_speed = STARTING_MOVE_DISTANCE

    def create_car(self):
        random_chance = random.randint(1, 6)
        if random_chance == 1:  # so that we don't get too many cars being generated. if that weren't a problem, then we'd just remove this "if" statement
            new_car = Turtle("square")
            new_car.shapesize(stretch_wid=1, stretch_len=2)  # so that the "cars" are the right shape
            new_car.penup()
            new_car.color(random.choice(COLORS))
            random_y = random.randint(-250, 250)
            new_car.goto(300, random_y)
            self.all_cars.append(new_car)

    def move_cars(self):
        for car in self.all_cars:
            car.backward(self.car_speed)

    def level_up(self):
        self.car_speed += MOVE_INCREMENT  # every frame the cars will move "backwards" further each time we level up. if you took a video with a fixed frame rate, and recorded a bunch of cars, this would be the definition of increasing their speed. think about it; it makes sense this way

