import json
import os
from lark import Lark, LarkError


def format_text(string: str, maxwidth: int, indent: int) -> str:
    words = string.split(" ")
    lines: list[str] = []
    string = f"{' '*indent}"
    for word in words:
        x = len(string + " " + word)
        if x > maxwidth - indent:
            lines.append(string)
            string = f"{' '*indent}{word} "
        else:
            string += word + " "
    lines.append(string)
    return "\n".join(lines)


def grammar_desc() -> dict[str, str]:
    with open("grammars.json", encoding="utf-8") as f:
        return json.loads(f.read())


def choose_grammar() -> str:
    choices: dict[str, str] = {}
    number = 1
    for path, _ in grammar_desc().items():
        choices[str(number)] = path
    sel = ""
    show_descriptions(grammar_desc())
    while sel not in choices:
        print("Please choose a number from the options above")
        sel = input(">>: ")
    return choices[sel]


def show_descriptions(data: dict[str, str]) -> None:
    number = 1
    for path, desc in data.items():
        width, _ = os.get_terminal_size()
        print(f"{number}.  {path}")
        print(format_text(desc, width, 4))
        number += 1


def main():
    path = ""
    while path != "exit":
        print("Welcome to the quick and dirty CLI for these random grammars.")
        print()
        path = choose_grammar()
        start_repl(path)


def start_repl(grammar_path: str):
    x = ""
    verbose = False
    w, _ = os.get_terminal_size()

    print(format_text(f"Welcome to the REPL for {grammar_path}.", w, 0))
    print(format_text("If you want to quit this interactive prompt and try another grammar, type 'quit' to return to the main menu. If you want to turn on/off verbose error messages for unparsable sentences, type '/v'.", int(w/2), 4))
    while x != "quit":

        x = input(">>: ")
        if x == "/v":
            verbose ^= verbose
            continue

        try:
            parser = Lark.open(grammar_path, parser="earley")
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

if __name__ == "__main__":
    main()
