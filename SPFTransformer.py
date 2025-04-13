from lark import Transformer
from type import Type

# décorateur trace / dump
def trace_and_dump(func):
    def wrapper(self, *args, **kwargs):
        name = func.__name__
        if self.tracing_mode:
            print("===========")
            print(f"[TRACE] Appel de {name} avec args=\n{args}")
            print("===========")
        result = func(self, *args, **kwargs)
        if self.dumping_mode:
            print("===========")
            print(f"[DUMP] Résultat de {name}: \n{result}")
            print("===========")
        return result
    return wrapper


class SPFTransformer(Transformer):

    def __init__(self, dumping_mode=False, tracing_mode=False):
        self.dumping_mode = dumping_mode
        self.tracing_mode = tracing_mode
        self.symbol_table = {}

    @trace_and_dump
    def declaration(self, args):
        type = args[0].value
        variable = args[1].value

        if len(args) == 3:
            value = args[2].value
            self.symbol_table[variable] = {'type': Type(type), 'value': value}
        else:
            self.symbol_table[variable] = {'type': Type(type)}

        return self.symbol_table[variable]

    @trace_and_dump
    def assignation(self, args):
        variable = args[0].value
        value = args[1].value

        self.symbol_table[variable]['value'] = value

        return self.symbol_table[variable]

    @trace_and_dump
    def afficher(self, args):
        printed = ""
        for arg in args:
            string = ""
            if arg.type == 'STRING':
                string = arg.value[1:-1]
            if arg.type == 'VARIABLE':
                string = self.symbol_table[arg.value]['value'][1:-1]
            print(string)
            printed += "print " + string + "\n"
        return printed
