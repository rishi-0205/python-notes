# with open("names.txt", "r") as file:
#     lines = file.readlines()

# for line in lines:
#     print("hello, ",line.rstrip())
#######################################

# with open("names.txt", "r") as file:
#     for line in file:
#         print("hello,", line.rstrip())
########################################

# names = []

# with open("names.txt") as file:
#     for line in file:
#         names.append(line.rstrip())

# for name in sorted(names):
#     print(f"hello, {name}")

########################################
# with open("names.txt") as file:
#     for line in sorted(file):
#         print("hello,",line.rstrip())

########################################
# with open("students.csv") as file:
#     for line in file:
#         name, house =line.rstrip().split(",")
#         print(f"{name} is in {house}")

########################################
# students = []
# with open("students.csv") as file:
#     for line in file:
#         name, house = line.rstrip().split(",")
#         student = {"name":name, "house":house}
#         students.append(student)

# # def get_name(student):
# #     return student["name"]

# for student in sorted(students, key=lambda student: student["name"], reverse=True):
#     print(f"{student['name']} is in {student['house']}")
##########################################
# import csv


# students = []
# with open("students.csv") as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         students.append(row)

# for student in sorted(students, key=lambda student: student["name"], reverse=True):
#     print(f"{student['name']} is in {student['home']}")
###########################################
import csv

name = input("What's your name? ")
home = input("Where's your home? ")

with open("students.csv", "a") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "home"])
    writer.writerow({"name": name, "home": home})

#use pillow library to work with images