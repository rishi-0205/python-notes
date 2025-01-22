# def total(galleons, sickles, knuts):
#     return (galleons*17 + sickles)*29 + knuts

# coins = [100, 50, 25]

# print(total(*coins), "Knuts")

# # using * before the list will unpack it
# # using ** before a dictionary unpacks it


def f(*args, **kwargs):
    if args:
        print("Positional:", args)
    if kwargs:
        print("Named:", kwargs)

f(100, 50, 25)
f(galleons=100, sickles=50, knuts=25)

#using *before an argument in function gives it an ability to take multiple positional arguements as input
#using ** before an arguement in function gives it an ability to take multiple named arguements as input
