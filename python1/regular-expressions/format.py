import re

name = input("What's your name? ").strip()

# if "," in  name:
#     last, first = name.split(", ?")
#     name = f"{first} {last}"
# print(f"hello, {name}")


if matches := re.search(r"^(.+), *(.+)$", name):
    #last, first = matches.groups()
    name = matches.group(2) + " " + matches.group(1)

print(f"Hello, {name}")
print(matches.group(0))