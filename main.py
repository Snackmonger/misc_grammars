from lark import Lark, LarkError

x = ""
verbose = False
while x != "quit":

    x = input(">>: ")
    if x == "/v":
        verbose ^= verbose
        continue

    try:
        parser = Lark.open("grammars/chord_symbol.lark", parser="earley")
    except LarkError as e:
        print("Oops! You made a change to the grammar that broke the program...")
        print("---->:", e)
        continue

    try:
        print(parser.parse(x).pretty())
    except LarkError as e:
        print("Sorry, that sentence could not be parsed.")
        if verbose:
            print(e)
