from turtle import Turtle

class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.l_score = 0
        self.r_score = 0
        self.goto(x=-100, y=200)
        self.write(self.l_score, align="center", font=("Courier", 80, "normal"))
        self.goto(x=100, y=200)
        self.write(self.r_score, align="center", font=("Courier", 80, "normal"))

    def l_point(self):
        self.l_score += 1

# we need to be able to update the scores. but all of that information is stuck in the "init" part of our class... so we need to take it out

class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.l_score = 0
        self.r_score = 0
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()  # so that the scores don't overlap when updating
        self.goto(x=-100, y=200)
        self.write(self.l_score, align="center", font=("Courier", 80, "normal"))
        self.goto(x=100, y=200)
        self.write(self.r_score, align="center", font=("Courier", 80, "normal"))

    def l_point(self):
        self.l_score += 1
        self.update_scoreboard()

    def r_point(self):
        self.r_score += 1
        self.update_scoreboard()
