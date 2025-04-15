# from turtle import Screen, Turtle
#
# screen = Screen()
# screen.bgcolor('black')
# screen.setup(width=800, height=600)
# screen.title("Pong")
#
# paddle = Turtle()
# paddle.shape("square")
# paddle.color("white")
# paddle.shapesize(stretch_wid=5, stretch_len=1)
# paddle.penup()
# paddle.goto(x=350, y=0)
#
# def go_up():
#     new_y = paddle.ycor() + 20
#     paddle.goto(x=paddle.xcor(), y=new_y)
#
# def go_down():
#     new_y = paddle.ycor() - 20
#     paddle.goto(x=paddle.xcor(), y=new_y)
#
# screen.listen()
# screen.onkeypress(key="Up", fun=go_up)  # when using a function as a parameter, you shouldn't use parenthesis
# screen.onkeypress(key="Down", fun=go_down)
#
# screen.exitonclick()

# but the paddle gets "created" at the center and then moves to the edge of the screen. let's solve this

# from turtle import Screen, Turtle
#
# screen = Screen()
# screen.bgcolor('black')
# screen.setup(width=800, height=600)
# screen.title("Pong")
# screen.tracer(0)
#
# paddle = Turtle()
# paddle.shape("square")
# paddle.color("white")
# paddle.shapesize(stretch_wid=5, stretch_len=1)
# paddle.penup()
# paddle.goto(x=350, y=0)
#
# def go_up():
#     new_y = paddle.ycor() + 20
#     paddle.goto(x=paddle.xcor(), y=new_y)
#
# def go_down():
#     new_y = paddle.ycor() - 20
#     paddle.goto(x=paddle.xcor(), y=new_y)
#
# screen.listen()
# screen.onkeypress(key="Up", fun=go_up)
# screen.onkeypress(key="Down", fun=go_down)
#
# game_is_on = True
#
# while game_is_on:
#     screen.update()
#
# screen.exitonclick()

# now, let's clean up our code by creating a class
#
# from turtle import Screen, Turtle
# from paddle import Paddle
#
# screen = Screen()
# screen.bgcolor('black')
# screen.setup(width=800, height=600)
# screen.title("Pong")
# screen.tracer(0)
#
# r_paddle = Paddle((350, 0))
# l_paddle = Paddle((-350, 0))
#
# screen.listen()
# screen.onkeypress(key="Up", fun=r_paddle.go_up)
# screen.onkeypress(key="Down", fun=r_paddle.go_down)
# screen.onkeypress(key="w", fun=l_paddle.go_up)
# screen.onkeypress(key="s", fun=l_paddle.go_down)
#
# game_is_on = True
#
# while game_is_on:
#     screen.update()
#
# screen.exitonclick()

# now, what about the "ball"?
#
# from turtle import Screen, Turtle
# from paddle import Paddle
# from ball import Ball
# import time
#
# screen = Screen()
# screen.bgcolor('black')
# screen.setup(width=800, height=600)
# screen.title("Pong")
# screen.tracer(0)
#
# r_paddle = Paddle((350, 0))
# l_paddle = Paddle((-350, 0))
# ball = Ball()
#
# screen.listen()
# screen.onkeypress(key="Up", fun=r_paddle.go_up)
# screen.onkeypress(key="Down", fun=r_paddle.go_down)
# screen.onkeypress(key="w", fun=l_paddle.go_up)
# screen.onkeypress(key="s", fun=l_paddle.go_down)
#
# game_is_on = True
#
# while game_is_on:
#     time.sleep(0.1)
#     screen.update()
#     ball.move()
#
# screen.exitonclick()

# now... how do we detect a collision?
#
# from turtle import Screen, Turtle
# from paddle import Paddle
# from ball import Ball
# import time
#
# screen = Screen()
# screen.bgcolor('black')
# screen.setup(width=800, height=600)
# screen.title("Pong")
# screen.tracer(0)
#
# r_paddle = Paddle((350, 0))
# l_paddle = Paddle((-350, 0))
# ball = Ball()
#
# screen.listen()
# screen.onkeypress(key="Up", fun=r_paddle.go_up)
# screen.onkeypress(key="Down", fun=r_paddle.go_down)
# screen.onkeypress(key="w", fun=l_paddle.go_up)
# screen.onkeypress(key="s", fun=l_paddle.go_down)
#
# game_is_on = True
#
# while game_is_on:
#     time.sleep(0.1)
#     screen.update()
#     ball.move()
#
#     # here is where we'll detect a collision
#     if ball.ycor() > 280 or ball.ycor() < -280:  # so that we can see this in our screen of height "600 px"
#         #we need to bounce
#         ball.bounce()
#
# screen.exitonclick()

# now... how do we detect a collision? now, with the paddle
#
# from turtle import Screen, Turtle
# from paddle import Paddle
# from ball import Ball
# import time
#
# screen = Screen()
# screen.bgcolor('black')
# screen.setup(width=800, height=600)
# screen.title("Pong")
# screen.tracer(0)
#
# r_paddle = Paddle((350, 0))
# l_paddle = Paddle((-350, 0))
# ball = Ball()
#
# screen.listen()
# screen.onkeypress(key="Up", fun=r_paddle.go_up)
# screen.onkeypress(key="Down", fun=r_paddle.go_down)
# screen.onkeypress(key="w", fun=l_paddle.go_up)
# screen.onkeypress(key="s", fun=l_paddle.go_down)
#
# game_is_on = True
#
# while game_is_on:
#     time.sleep(0.1)
#     screen.update()
#     ball.move()
#
#     # here is where we'll detect a collision with the wall
#     if ball.ycor() > 280 or ball.ycor() < -280:
#         ball.bounce_y()
#
#     # here is where we'll detect a collision with the paddle
#     if ball.distance(r_paddle) < 50 and ball.xcor() > 320 or ball.distance(l_paddle) < 50 and ball.xcor() < -320:  # so that we can see this in our screen of width "800 px" and the ball doesn't go into the paddle
#         # we need to bounce
#         ball.bounce_x()
#
# screen.exitonclick()

# now... how do we detect the ball going past the screen?
#
# from turtle import Screen, Turtle
# from paddle import Paddle
# from ball import Ball
# import time
#
# screen = Screen()
# screen.bgcolor('black')
# screen.setup(width=800, height=600)
# screen.title("Pong")
# screen.tracer(0)
#
# r_paddle = Paddle((350, 0))
# l_paddle = Paddle((-350, 0))
# ball = Ball()
#
# screen.listen()
# screen.onkeypress(key="Up", fun=r_paddle.go_up)
# screen.onkeypress(key="Down", fun=r_paddle.go_down)
# screen.onkeypress(key="w", fun=l_paddle.go_up)
# screen.onkeypress(key="s", fun=l_paddle.go_down)
#
# game_is_on = True
#
# while game_is_on:
#     time.sleep(0.1)
#     screen.update()
#     ball.move()
#
#     if ball.ycor() > 280 or ball.ycor() < -280:
#         ball.bounce_y()
#
#     if ball.distance(r_paddle) < 50 and ball.xcor() > 320 or ball.distance(l_paddle) < 50 and ball.xcor() < -320:
#         ball.bounce_x()
#
#     # now, let's detect when the right paddle misses the ball
#     if ball.xcor() > 380:
#         ball.reset_position()
#
#     # now, let's detect when the right paddle misses the ball
#     if ball.xcor() < -380:
#         ball.reset_position()
#
# screen.exitonclick()

#now... how do we keep track of the score?

# from turtle import Screen, Turtle
# from paddle import Paddle
# from ball import Ball
# from scoreboard import Scoreboard
# import time
#
# screen = Screen()
# screen.bgcolor('black')
# screen.setup(width=800, height=600)
# screen.title("Pong")
# screen.tracer(0)
#
# r_paddle = Paddle((350, 0))
# l_paddle = Paddle((-350, 0))
# ball = Ball()
# scoreboard = Scoreboard()
#
# screen.listen()
# screen.onkeypress(key="Up", fun=r_paddle.go_up)
# screen.onkeypress(key="Down", fun=r_paddle.go_down)
# screen.onkeypress(key="w", fun=l_paddle.go_up)
# screen.onkeypress(key="s", fun=l_paddle.go_down)
#
# game_is_on = True
#
# while game_is_on:
#     time.sleep(0.1)
#     screen.update()
#     ball.move()
#
#     if ball.ycor() > 280 or ball.ycor() < -280:
#         ball.bounce_y()
#
#     if ball.distance(r_paddle) < 50 and ball.xcor() > 320 or ball.distance(l_paddle) < 50 and ball.xcor() < -320:
#         ball.bounce_x()
#
#     # now, let's detect when the right paddle misses the ball
#     if ball.xcor() > 380:
#         ball.reset_position()
#         scoreboard.l_point()
#
#     # now, let's detect when the right paddle misses the ball
#     if ball.xcor() < -380:
#         ball.reset_position()
#         scoreboard.r_point()
#
# screen.exitonclick()

# and... how could you increase the speed of the ball everytime it hits a paddle?

from turtle import Screen, Turtle
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time

screen = Screen()
screen.bgcolor('black')
screen.setup(width=800, height=600)
screen.title("Pong")
screen.tracer(0)

r_paddle = Paddle((350, 0))
l_paddle = Paddle((-350, 0))
ball = Ball()
scoreboard = Scoreboard()

screen.listen()
screen.onkeypress(key="Up", fun=r_paddle.go_up)
screen.onkeypress(key="Down", fun=r_paddle.go_down)
screen.onkeypress(key="w", fun=l_paddle.go_up)
screen.onkeypress(key="s", fun=l_paddle.go_down)

game_is_on = True

while game_is_on:
    time.sleep(ball.move_speed)  # genius
    screen.update()
    ball.move()

    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()

    if ball.distance(r_paddle) < 50 and ball.xcor() > 320 or ball.distance(l_paddle) < 50 and ball.xcor() < -320:
        ball.bounce_x()

    # now, let's detect when the right paddle misses the ball
    if ball.xcor() > 380:
        ball.reset_position()
        scoreboard.l_point()

    # now, let's detect when the right paddle misses the ball
    if ball.xcor() < -380:
        ball.reset_position()
        scoreboard.r_point()

screen.exitonclick()

# the only problem with this game... is that we can't seem to move both paddles simultaneously.
