from lark import Transformer, Token
from type import Type

class SPFTransformer(Transformer):

    def __init__(self, dumping_mode=False, tracing_mode=False):
        super().__init__()
        self.dumping_mode = dumping_mode
        self.tracing_mode = tracing_mode
        self.symbol_table = {}

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

    def assignation(self, args):
        variable = args[0].value
        value = args[1].children[0]

        self.symbol_table[variable]['value'] = value

        return self.symbol_table[variable]

    def afficher(self, args):
        printed = ""
        for arg in args:
            string = ""
            if isinstance(arg, Token):
                string = self.symbol_table[arg.value]['value']
            else:
                string = arg
            print(string)

    def liste(self,args):
        list = []
        tree = args[0]
        for sub_tree in tree.children:
            list.append(sub_tree.children[0])
        return list

    def entier(self,args):
        return int(args[0].value)

    def chaine(self,args):
        return args[0].value[1:-1]

    def booleen(self,args):
        return args[0].value == 'vrai'