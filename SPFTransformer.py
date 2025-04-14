from lark import Transformer, Token
from type import Type
from Memory import Memory
from functools import wraps
from SPFException import *

def trace(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.tracing_mode:
            print(f"[TRACE] Appel de {func.__name__}({', '.join(map(repr, args))})")
        result = func(self, *args, **kwargs)
        if self.tracing_mode:
            print(f"[TRACE] {func.__name__} a retourné {result!r}")
        return result
    return wrapper

def exception_handler(func):
    @wraps(func)
    def wrapper(self,*args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e: #TODO REFAIRE AU PROPRE
            current_token = args[0][0]

            if isinstance(e, SPFUnknownVariable):
                print(f"[ERROR] Line {current_token.line} : The variable '{current_token}' is not defined")
            elif isinstance(e, SPFUninitializedVariable):
                print(f"[ERROR] Line {current_token.line} : The variable '{current_token}' is not initialized")
            elif isinstance(e, SPFAlreadyDefined):
                current_token = args[0][1]
                print(f"[ERROR] Line {current_token.line} : The variable '{current_token}' is already defined in this scope")
            elif isinstance(e, SPFIncompatibleType):
                print(f"[ERROR] Line {current_token.line} : Type error '{current_token}' blabla")

            raise Exception
    return wrapper

class SPFTransformer(Transformer):

    def __init__(self, dumping_mode=False, tracing_mode=False):
        super().__init__()
        self.tracing_mode = tracing_mode
        self.symbol_table = Memory(dumping_mode)

    @trace
    @exception_handler
    def declaration(self, args):
        var_type = args[0].value
        variable = args[1].value

        new_var = self.symbol_table.declare(variable, Type(var_type))

        if len(args) == 3:
            sub_tree = args[2]
            value = sub_tree.children[0]

            new_var = self.symbol_table.set(variable,value)

        return new_var

    @trace
    @exception_handler
    def assignation(self, args):
        variable = args[0].value
        value = args[1].children[0]

        new_var = self.symbol_table.set(variable,value)

        return new_var

    @trace
    @exception_handler
    def afficher(self, args):
        result = []
        for arg in args:
            if isinstance(arg, Token):
                value = self.symbol_table.get(arg.value)
                string = value.get_value()
            else:
                string = arg
            result.append(str(string))
        printed = " ".join(result)
        print(printed)
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