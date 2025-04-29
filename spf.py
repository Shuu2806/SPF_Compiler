import argparse
import logging

from interpreter.SPFInterpreter import SPFInterpreter
from interpreter.Memory import Memory
from interpreter.SPFException import SPFException
from lark import Lark, UnexpectedInput

dumping_mode = False
tracing_mode = False


def getLarkParser():
    with open("interpreter/spf.lark", "r", encoding='utf-8') as f:
        grammar = f.read()

    return Lark(grammar, parser="lalr", propagate_positions=True)


def SPFParser(program):
    parser = getLarkParser()  # crée un parser avec la grammaire défini dans spf.lark

    tree = parser.parse(program)  # parse le fichier programme en un arbre

    #print("Arbre syntaxique :")
    #print(tree.pretty())

    SPFInterpreter(dumping_mode, tracing_mode).visit(tree)

def main():
    global dumping_mode, tracing_mode

    parser = argparse.ArgumentParser(description="SPF Interpreter")
    parser.add_argument("-i", "--input", type=str, required=True, help="Le chemin vers le fichier .spf.")
    parser.add_argument("-d", "--dump", action="store_true", help="Permet d'afficher les accès mémoire pendant l'exécution du programme.")
    parser.add_argument("-t", "--trace", action="store_true", help="Permet d'afficher le mémoire à la fin du programme.")

    args = parser.parse_args()

    if args.dump:
        dumping_mode = True

    if args.trace:
        tracing_mode = True

    parser = Lark.open("interpreter/spf.lark", parser="lalr", start="program", propagate_positions=True)
    with open("example_code/" + args.input, "r", encoding='utf-8') as f:
            program = f.read()
    try:
        SPFParser(program)
    except FileNotFoundError:
        print(f"Erreur : le fichier '{args.input}' est introuvable.")
    except UnexpectedInput as e:
        print(f"Erreur : entrée inattendue à la ligne {e.line}, Syntaxe invalide.")
        return
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        return
    

if __name__ == "__main__":
    main()