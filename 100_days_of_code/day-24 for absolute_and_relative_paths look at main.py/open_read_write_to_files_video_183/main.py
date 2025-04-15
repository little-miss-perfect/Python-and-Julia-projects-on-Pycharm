# file = open("my_file.txt")  # first, we just open the file. nothing more.
# contents = file.read()  # then we ask to read the file. it stores this as a string. it does nothing more. but now we've read the file and saved it to a variable.
# print(contents)  # now we see this variable
# # but now we need to close the file. because we opened it. we could just not do this, but it'd be "taking up space". like when you leave tons of browser tabs open when you use chrome.
# # so that the speed of our computer isn't affected by having lots of files opened and being used
# file.close()

# TODO: or, you could use the following syntax

# with open("my_file.txt") as file:
#     contents = file.read()
#     print(contents)
#     # and now we don't need to be closing our file every time.

# but what if what I'd like to do was to not just read the file but also write to it? well we'd need to do the following:

# with open("my_file.txt", mode="w") as file:  # by default, the file is opened in "read only" mode. so we need to change this mode if we want to edit the file (by writing)
#     file.write("New text.")

# but this will add text by replacing ALL the previous text in the file. so what do we do?

# with open("my_file.txt", mode="a") as file:  # we change the "mode" to "a" for "append"
#     file.write("\n New text.")

# but what if we "open" a file that doesn't exist? well, then it's created (although, where is it created? in the same folder that this "main.py" file exists).
# this is only works when you're in the "write" mode and this file doesn't exist.

with open("my_file.txt") as file:
    contents = file.read()
    print(contents)

with open("new_file.txt", mode="w") as file:
    file.write("New text.")
