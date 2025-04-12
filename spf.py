import argparse
from SPFTransformer import SPFTransformer
from lark import Lark

dumping_mode = False
tracing_mode = False

def getLarkParser():
    with open("spf.lark", "r") as f:
        grammar = f.read()

    return Lark(grammar, parser="lalr")


def SPFParser(program):
    parser = getLarkParser() # crée un parser avec la grammaire défini dans spf.lark

    tree = parser.parse(program) # parse le fichier programme en un arbre
    result = SPFTransformer(dumping_mode,tracing_mode).transform(tree)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True, help="Input file")
    parser.add_argument("--dump", action="store_true", help="Dump mode")
    parser.add_argument("--trace", action="store_true", help="Trace mode")

    args = parser.parse_args()

    if args.dump:
        print("dumping mode on")
        dumping_mode = True

    if args.trace:
        print("tracing mode on")
        tracing_mode = True

    try:
        with open("example_code/" + args.input, "r") as f:
            program = f.read()
            SPFParser(program)
    except FileNotFoundError:
        print(f"Erreur : le fichier '{args.input}' est introuvable.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

if __name__ == "__main__":
    main()