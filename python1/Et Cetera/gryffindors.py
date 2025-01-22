# students = [
#     {"name": "Hermione", "house": "Gryffindor"},
#     {"name": "Harry", "house": "Gryffindor"},
#     {"name": "Ron", "house": "Gryffindor"},
#     {"name": "Draco", "house": "Slytherin"},
#     {"name": "Padma", "house": "Ravenclaw"}
# ]

# # gryffindor = [student["name"] for student in students if student["house"] == "Gryffindor"]

# # print(*sorted(gryffindor))

# # def is_gryffindor(s):
# #     return s["house"] == "Gryffindor"

# gryffindors = filter(lambda s : s["house"] == "Gryffindor", students)

# print(*sorted(gryffindors, key=lambda s : s["name"]))


students = ["Hermione", "Harry", "Ron"]

# gryffindors = []

# for student in students:
#     gryffindors.append({"name": student, "house":"Gryffindor"})

# 

# gryffindors = {student: "Gryfindor" for student in students}

# print(gryffindors)

for i, student in enumerate(students):
    print(i+1, student)


# print(*enumerate(students))