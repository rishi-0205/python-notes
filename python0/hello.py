def main():
    #Ask user for name, Remove whitespaces and capitalize
    name = input("What's your name?: ").strip().title()

    #Greet the user
    #print(f"Hello, {name}")

    #hello()

    """
    This is a
    multiline
    comment.
    """
    hello(name)


def hello(to="world"):
    print("hello,",to)


main()