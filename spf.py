import argparse

def parserspf(program):
    print(program)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True, help="Input file")
    parser.add_argument("--dump", action="store_true", help="Dump mode")
    parser.add_argument("--trace", action="store_true", help="Trace mode")

    args = parser.parse_args()

    if args.dump:
        print("mode dumping")
    if args.trace:
        print("mode tracing")

    try:
        with open(args.input, "r") as f:
            program = f.read()
            parserspf(program)
    except FileNotFoundError:
        print(f"Erreur : le fichier '{args.input}' est introuvable.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

if __name__ == "__main__":
    main()