import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard

screen = Screen()
screen.bgcolor("black")
screen.setup(width=600, height=600)
screen.tracer(0)  # so we need to use the "time module" in the "while" loop

player = Player()
car_manager = CarManager()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(fun=player.go_up, key="Up")

game_is_on = True
while game_is_on:
    time.sleep(0.1)
    screen.update()

    car_manager.create_car()
    car_manager.move_cars()

    # now let's detect a collision with a car
    for car in car_manager.all_cars:
        if car.distance(player) < 20:  # this distance is because of the size (in pixels) of the objects being created (the "turtle" and the "cars")
            game_is_on = False
            scoreboard.game_over()

    # now let's detect a successful crossing
    if player.is_at_finish_line():  # putting this as the condition makes sense because this method returns a boolean *variable
        player.go_to_start()
        car_manager.level_up()
        scoreboard.increase_level()

screen.exitonclick()

# we almost had it correct. there's some object being created in the center. some arrow. what did we not write correctly? :(
