from lark import Transformer, Token

# décorateur trace / dump
def trace_and_dump(func):
    def wrapper(self, *args, **kwargs):
        name = func.__name__
        if self.tracing_mode:
            print(f"[TRACE] Appel de {name} avec args={args}")
        result = func(self, *args, **kwargs)
        if self.dumping_mode:
            print(f"[DUMP] Résultat de {name}: \n{result}")
        return result
    return wrapper


class SPFTransformer(Transformer):

    def __init__(self, dumping_mode=False, tracing_mode=False):
        self.dumping_mode = dumping_mode
        self.tracing_mode = tracing_mode
        self.symbol_table = {}

    @trace_and_dump
    def declaration(self, args):
        print(args)

    @trace_and_dump
    def assignation(self, args):
        print(args)

    @trace_and_dump
    def afficher(self, args):
        printed = ""
        for tree in args:
            token = tree.children[0]
            if token.type == 'ESCAPED_STRING':
                string = token.value[1:-1]
                print(string)
                printed += "   print " + string + "\n"
            #if token.type == 'CNAME':


        return printed
