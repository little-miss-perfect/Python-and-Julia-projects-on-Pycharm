# # TODO: absolute path
# with open("/Users/morni/Desktop/my_file.txt") as file:
#     contents = file.read()
#     print(contents)
#
# # this is how we'd access the file if it were in the desktop.
# # see how we didn't need to write the absolute path as is written
# # in the "properties" section of the file? we didn't have to write
# # "C:\Users\morni\Desktop\my_file.txt". and
# # we only wrote down forward slashes, no backslashes. and
# # the "root" is represented by "/"; no need to use "C:/" or "C:\".
#
# # that was for an absolute path.
#
# # TODO: relative path
# #for a relative path we do the following:
#
# # angela also says that for a relative path, one can use "./"
# # to go further into folders, or "../" to move outside of folders
# # all relative to a current "working directory" ("wd" as we've used in Linux)
#
# # we'll erase the "my_file.txt" from our desktop. but if you want
# # to check that this works in the future, you can just create the file in our desktop.
# # amazing
#
# # TODO: check this out!
# # although for Mac, you use a forward slash ("/") to represent movement through a path
# # while for Windows you use a backforward slash ("\"):
# # for Python code, you don't need to worry about this at all. all you need to do
# # to represent movement through a path is use
# # a forward slash ("/").
#
#
#
#
# # but now...
# TODO: relative paths with "../" (move out) and "./" (move in)
# right now, this "main.py" file is in the following location/environment:

# "C:\Users\morni\PycharmProjects\100_days_of_code\day-24 for absolute_and_relative_paths look at main.py".
# so how do we access
# the file in the "desktop", relative to this location? we need to move "out" twice, right? then move "in"
# once to the "desktop" folder. so... we need to use "../" to move "outside" of folders
# relative to where we are (and "./" to move "inside" of folders relative to where we are):

# in Python, "../../../" will take us to what our Windows computer sees as "\morni", right?
# after that, we just need to move forward by using "/". so we write:

with open("../../../Desktop/my_file.txt") as file:
    contents = file.read()
    print(contents)

# nice

# TODO: notice the following

# for a relative path,
# although in the current working directory
# you can write "./file.extension", the "./" is optional; for a relative path.
# look at the quiz on "day-24" (in the Udemy site/app) to understand all of this better.
