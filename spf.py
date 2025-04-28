import argparse
import logging

from interpreter.SPFInterpreter import SPFInterpreter
from interpreter.Memory import Memory
from interpreter.SPFException import SPFException
from lark import Lark, UnexpectedInput

dumping_mode = False
tracing_mode = False


def main():
    global dumping_mode, tracing_mode

    parser = argparse.ArgumentParser(description="SPF Interpreter")
    parser.add_argument("-i", "--input", type=str, required=True, help="Le chemin vers le fichier .spf.")
    parser.add_argument("-d", "--dump", action="store_true", help="Permet d'afficher les accès mémoire pendant l'exécution du programme.")
    parser.add_argument("-t", "--trace", action="store_true", help="Permet d'afficher le mémoire à la fin du programme.")

    args = parser.parse_args()

    
    if args.dump:
        logging.basicConfig(
            level=logging.DEBUG,
            format="Debug: %(message)s"
        )
    parser = Lark.open("interpreter/spf.lark", parser="lalr", start="program", propagate_positions=True)
    with open("example_code/" + args.input, "r", encoding='utf-8') as f:
            program = f.read()
    try:
        memory : Memory = SPFInterpreter().visit(parser.parse(program))
    except FileNotFoundError:
        print(f"Erreur : le fichier '{args.input}' est introuvable.")
    except UnexpectedInput as e:
        print(f"Erreur : entrée inattendue à la ligne {e.line}, Syntaxe invalide.")
        return
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        return
    if args.trace:
        import sys
        print(memory, file=sys.stderr)
    

if __name__ == "__main__":
    main()