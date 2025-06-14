# with open("weather_data.csv") as data_file:
#     data = data_file.readlines()
#     print(data)

import csv

# with open("weather_data.csv") as data_file:
#     data = csv.reader(data_file)
#     # print(data)
#     temperatures = []
#     for row in data:
#         print(row)

# with open("weather_data.csv") as data_file:
#     data = csv.reader(data_file)
#     # print(data)
#     temperatures = []
#     for row in data:
#         if row[1] != "temp":
#             temperatures.append(row[1])
#     print(temperatures)

# with open("weather_data.csv") as data_file:
#     data = csv.reader(data_file)
#     # print(data)
#     temperatures = []
#     for row in data:
#         if row[1] != "temp":
#             temperatures.append(int(row[1]))
#     print(temperatures)

import pandas

# data = pandas.read_csv("weather_data.csv")
# print(data)  # this is a dataframe (the whole "table")

# data = pandas.read_csv("weather_data.csv")
# print(data["temp"])

# data = pandas.read_csv("weather_data.csv")
# print(type(data))
# #print(data["temp"])  # this is a "series" (just a column)

data = pandas.read_csv("weather_data.csv")
#print(type(data))
#print(type(data["temp"]))

# data_dict = data.to_dict()
# print(data_dict)
#
# # temp_list = data["temp"].to_list()
# # print(temp_list)
#
# temp_list = data["temp"].to_list()
# print(temp_list)
#
# # average = sum(temp_list) / len(temp_list)  # "sum" sums up all the elements in a given list, right?
# # print(average)
#
# print(data["temp"].mean())  # or get the mean in one line
# print(data["temp"].max())
#
# # get data in columns
# print(data["condition"])
# print(data.condition)

# # get data in row
# print(data[data.day == "Monday"])  # remember that "data[data.day]" is the same as "data[data["day"]]
# # print(data[data.temp == data["temp"].max()])
# print(data[data.temp == data.temp.max()])

# monday = data[data.day == "Monday"]  # a row
# # but how do we access the values under different columns in this row?
# print(monday.condition)

# monday = data[data.day == "Monday"]
# monday_temp = monday.temp[0]
# monday_temp_F = monday_temp * 9/5 + 32
# print(monday_temp_F)

# monday = data[data.day == "Monday"]
# monday_temp = monday.temp[0]
# monday_temp_F = monday_temp * 9/5 + 32
# print(monday_temp_F)

# create a dataframe from scratch
data_dict = {
    "students": ["Amy", "James", "Angela"],
    "scores": [76, 56, 65]
}

# data = pandas.DataFrame(data_dict)
# print(data)

data = pandas.DataFrame(data_dict)
data.to_csv("new_data.csv")  # its input is the path to which I want to save this file
