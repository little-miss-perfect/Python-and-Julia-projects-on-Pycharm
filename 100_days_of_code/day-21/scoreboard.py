# from turtle import Turtle
#
# class Scoreboard(Turtle):
#
#     def __init__(self):
#         super().__init__()
#
#         self.score = 0
#         self.color('white')  # again, the order matters. first set the color to white, then show the "scoreboard". because if you show the scoreboard (which is in black) and then change the color to white... well you've already shown the scoreboard, so there's no change
#         self.penup()
#         self.goto(0, 260)
#         self.write(f"Score: {self.score}", align="center", font=("Arial", 24, "normal"))  # notice that the documentation requieres you to write the parameter "font" as a tuple
#         self.hideturtle()
#
#     def increase_score(self):
#         self.score += 1
#         self.write(f"Score: {self.score}", align="center", font=("Arial", 24, "normal"))

# # and the next modification is so that he scoreboard doesn't overlap text
#
# from turtle import Turtle
#
#
# class Scoreboard(Turtle):
#
#     def __init__(self):
#         super().__init__()
#
#         self.score = 0
#         self.color('white')
#         self.penup()
#         self.goto(0, 260)
#         self.hideturtle()
#         self.update_scoreboard()
#
#     def update_scoreboard(self):
#         self.write(f"Score: {self.score}", align="center", font=("Arial", 24, "normal"))
#
#     def increase_score(self):
#         self.score += 1
#         self.clear()
#         self.update_scoreboard()

# and the next modification is... a bit aesthetic

# from turtle import Turtle
#
# ALIGNMENT = "center"
# FONT = ("Courier", 24, "normal")
#
# class Scoreboard(Turtle):
#
#     def __init__(self):
#         super().__init__()
#
#         self.score = 0
#         self.color('white')
#         self.penup()
#         self.goto(0, 260)
#         self.hideturtle()
#         self.update_scoreboard()
#
#     def update_scoreboard(self):
#         self.write(f"Score: {self.score}", align=ALIGNMENT, font=FONT)
#
#     def increase_score(self):
#         self.score += 1
#         self.clear()
#         self.update_scoreboard()

# now, for wall detection we'll have

# from turtle import Turtle
#
# ALIGNMENT = "center"
# FONT = ("Courier", 24, "normal")
#
# class Scoreboard(Turtle):
#
#     def __init__(self):
#         super().__init__()
#
#         self.score = 0
#         self.color('white')
#         self.penup()
#         self.goto(0, 260)
#         self.hideturtle()
#         self.update_scoreboard()
#
#     def update_scoreboard(self):
#         self.write(f"Score: {self.score}", align=ALIGNMENT, font=FONT)
#
#     def game_over(self):
#         self.goto(0, 0)
#         self.write('GAME OVER', align=ALIGNMENT, font=FONT)
#
#     def increase_score(self):
#         self.score += 1
#         self.clear()
#         self.update_scoreboard()

# now... how do we detect a collision with our own tail?

from turtle import Turtle

ALIGNMENT = "center"
FONT = ("Courier", 24, "normal")

class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()

        self.score = 0
        self.color('white')
        self.penup()
        self.goto(0, 260)
        self.hideturtle()
        self.update_scoreboard()

    def update_scoreboard(self):
        self.write(f"Score: {self.score}", align=ALIGNMENT, font=FONT)

    def game_over(self):
        self.goto(0, 0)
        self.write('GAME OVER', align=ALIGNMENT, font=FONT)

    def increase_score(self):
        self.score += 1
        self.clear()
        self.update_scoreboard()
