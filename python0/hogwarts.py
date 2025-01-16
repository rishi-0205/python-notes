# students = ["Hermione", "Harry", "Ron"]

# for student in students:
#     print(student)

# for i in range(len(students)):
#     print(i+1, students[i])

#################################################

# students = {
#     "Hermione": "Gryffindor",
#     "Harry": "Gryfindor",
#     "Ron": "Gryffindor",
#     "Draco": "Slytherin",
# }

# for keys in students:
#     print(keys,students[keys], sep=": ")

#################################################

students = [
    {
        "name":"Hermione",
        "House":"Gryffindor",
        "Patronus":"Otter",
    },
    {
        "name":"Harry",
        "House":"Gryffindor",
        "Patronus":"Stag",
    },
    {
        "name":"Ron",
        "House":"Gryffindor",
        "Patronus":"Jack Russell Terrier",
    },
    {
        "name":"Draco",
        "House":"Gryffindor",
        "Patronus":None,
    },
]

for student in students:
    for key in student:
        print(key, student[key], sep=": ")
    print()