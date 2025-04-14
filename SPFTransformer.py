from lark import Transformer, Token
from type import Type
import functools

def trace(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if args[0].tracing_mode:
            arg_str = ', '.join(
                [repr(a) for a in args[1:]] +
                [f"{k}={v!r}" for k, v in kwargs.items()]
            )
            print(f"[TRACE] Appel de {func.__name__}({arg_str})")

        result = func(*args, **kwargs)

        if args[0].tracing_mode:
            print(f"[TRACE] {func.__name__} a retourné {result!r}")

        return result
    return wrapper


class SPFTransformer(Transformer):

    def __init__(self, dumping_mode=False, tracing_mode=False):
        super().__init__()
        self.dumping_mode = dumping_mode
        self.tracing_mode = tracing_mode
        self.symbol_table = {}

    @trace
    def declaration(self, args):
        type = args[0].value
        variable = args[1].value

        if len(args) == 3:
            sub_tree = args[2]
            value = sub_tree.children[0]
            self.symbol_table[variable] = {'type': type, 'value': value}
        else:
            self.symbol_table[variable] = {'type': Type(type)}

        return self.symbol_table[variable]

    @trace
    def assignation(self, args):
        variable = args[0].value
        value = args[1].children[0]

        self.symbol_table[variable]['value'] = value

        return self.symbol_table[variable]

    @trace
    def afficher(self, args):
        printed = ""
        for arg in args:
            if isinstance(arg, Token):
                string = self.symbol_table[arg.value]['value']
            else:
                string = arg
            print(string)
            printed += str(string) + " "
        return printed

    @trace
    def liste(self,args):
        list = []
        tree = args[0]
        for sub_tree in tree.children:
            list.append(sub_tree.children[0])
        return list

    @trace
    def entier(self,args):
        return int(args[0].value)

    @trace
    def chaine(self,args):
        return args[0].value[1:-1]

    @trace
    def booleen(self,args):
        return args[0].value == 'vrai'