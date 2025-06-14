import turtle
import pandas

screen = turtle.Screen()
screen.title("U.S. States Game")

# turtle.shape("turtle")
# but we can also "import" more shapes (like the ".gif" file)
image = "blank_states_img.gif"
screen.addshape(image)

turtle.shape(image)



# # def get_mouse_click_coor(x, y):
# #     '''
# #
# #     :param x: input
# #     :param y: input
# #     :return: it prints them out
# #     '''
# #     print(x, y)
# #
# # turtle.onscreenclick(get_mouse_click_coor)  # this passes the coordinates of the "click location"
# #
# # turtle.mainloop()
# #
# #
# #
# # # screen.exitonclick()  # because we're using the "turtle.mainloop()"
# #
# # # but we don't actually need this block of code because the ".csv" file already has the positions
#
# answer_state = screen.textinput(title="Guess the State", prompt="What's another state's name?")
# # print(answer_state)  # to see what's been input

# data = pandas.read_csv("50_states.csv")
#
#
# answer_state = screen.textinput(title="Guess the State", prompt="What's another state's name?")
# print(answer_state)  # to see what's been input
#
#
# # if answer_state is one of the states in all the states in 50_states_csv
#     # if they got it right:
#         # create a turtle to write the name of the state at the state's x and y coordinate
#
#
# # data.state  # which is the same as data["state"]

# data = pandas.read_csv("50_states.csv")
# all_states = data.state.to_list()
#
# answer_state = screen.textinput(title="Guess the State", prompt="What's another state's name?")
# print(answer_state)
#
# # if answer_state in all_states:
# #     t = turtle.Turtle()
# #     t.hideturtle()
# #     t.penup()
# #     state_data = data[data.state == answer_state] # it'll get the row where the state equals the answer_state
# #     t.goto(state_data.x, state_data.y)  # because this is a row of data, we can tap into its attributes using the names of the columns
# #
# #     t.write(state_data.state)  # we access the attribute "state"
# #
# # but that will give us an error. let's fix it
#
# # if answer_state in all_states:
# #     t = turtle.Turtle()
# #     t.hideturtle()
# #     t.penup()
# #     state_data = data[data.state == answer_state]  # it'll get the row where the state equals the answer_state
# #     t.goto(state_data.x.item(),  # but careful, "state_data.x" is actually a pandas series (a column) called "x": this series actually contains an index and the coordinate (we only want the coordinate). that's why we write "state_data.x.item()"
# #            state_data.y.item())
# #
# #     t.write(state_data.state)  # we access the attribute "state"
# #
# # screen.exitonclick()
#
# # if answer_state in all_states:
# #     t = turtle.Turtle()
# #     t.hideturtle()
# #     t.penup()
# #     state_data = data[data.state == answer_state]  # it'll get the row where the state equals the answer_state
# #     t.goto(state_data.x.item(),  # but careful, "state_data.x" is actually a pandas series (a column) called "x": this series actually contains an index and the coordinate (we only want the coordinate). that's why we write "state_data.x.item()"
# #            state_data.y.item())
# #
# #     t.write(answer_state)  # since we already confirmed this is a valid state, it doesn't matter if we use the answer_state, or the state_data
# #
# # screen.exitonclick()
#
#
#
#
# # # but maybe we want to use state_data. so:
# #
# # if answer_state in all_states:
# #     t = turtle.Turtle()
# #     t.hideturtle()
# #     t.penup()
# #     state_data = data[data.state == answer_state]  # it'll get the row where the state equals the answer_state
# #     t.goto(state_data.x.item(),  # but careful, "state_data.x" is actually a pandas series (a column) called "x": this series actually contains an index and the coordinate (we only want the coordinate). that's why we write "state_data.x.item()"
# #            state_data.y.item())
# #
# #     t.write(state_data.state.item())  # like what we used for the coordinates (since "state_data.state" is a pandas series). ".item()" will get the first value from the row
# #     # but using "state_data.state.item()" here, might be overkill
# #
# # screen.exitonclick()




# # now let's make it repeat itself everytime the user makes a guess
#
# data = pandas.read_csv("50_states.csv")
# all_states = data.state.to_list()
# guessed_states = []
#
#
# while len(guessed_states) < len(all_states):
#     answer_state = screen.textinput(title="Guess the State", prompt="What's another state's name?")
#     print(answer_state)
#
#     if answer_state in all_states:
#         guessed_states.append(answer_state)
#
#         t = turtle.Turtle()
#         t.hideturtle()
#         t.penup()
#         state_data = data[data.state == answer_state]  # it'll get the row where the state equals the answer_state
#         t.goto(state_data.x.item(), state_data.y.item())
#         t.write(answer_state)
#
# screen.exitonclick()





# # but now we'd like to make the title a bit more dynamic
#
# data = pandas.read_csv("50_states.csv")
# all_states = data.state.to_list()
# guessed_states = []
#
# while len(guessed_states) < len(all_states):
#     answer_state = screen.textinput(title=f"{len(guessed_states)}/{len(all_states)} States Correct", prompt="What's another state's name?")
#     print(answer_state)
#
#     if answer_state in all_states:
#         guessed_states.append(answer_state)
#
#         t = turtle.Turtle()
#         t.hideturtle()
#         t.penup()
#         state_data = data[data.state == answer_state]  # it'll get the row where the state equals the answer_state
#         t.goto(state_data.x.item(), state_data.y.item())
#         t.write(answer_state)
#
# screen.exitonclick()




# what about capital letters even though you wrote the correct state? (i.e. these states' names have "title case")

data = pandas.read_csv("50_states.csv")
all_states = data.state.to_list()
guessed_states = []

while len(guessed_states) < len(all_states):
    answer_state = screen.textinput(title=f"{len(guessed_states)}/{len(all_states)} States Correct",
                                    prompt="What's another state's name?").title()  # this makes the first letter a capital letter (and it makes every other letter a lowercase letter?)
    print(answer_state)

    if answer_state in all_states:
        guessed_states.append(answer_state)

        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        state_data = data[data.state == answer_state]  # it'll get the row where the state equals the answer_state
        t.goto(state_data.x.item(), state_data.y.item())
        t.write(answer_state)

screen.exitonclick()