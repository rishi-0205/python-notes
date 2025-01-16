# i = 1

# while i <= 3:
#     print("Meow")
#     i+=1

# for i in [0 ,1 ,2]:
#     print("meow")

# for i in range(3):
#     print("meow")

# for _ in range(3):
#     print("meow")

# print("meow\n" * 3, end="")

# while True:
#     i = int(input("What's i? "))
#     if i > 0:
#         break

# for _ in range(i):
#     print("meow")

def main():
    number = get_number()
    meow(number)

def meow(number):
    for _ in range(number):
        print("meow")

def get_number():
    while True:
        i = int(input("What's i? "))
        if i > 0:
            return i

main()