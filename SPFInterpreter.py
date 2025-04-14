from lark import Tree, Token
from lark.visitors import Interpreter
from Memory import Memory

class SPFInterpreter(Interpreter):

    def __init__(self, dumping_mode=False, tracing_mode=False):
        super().__init__()
        self.tracing_mode = tracing_mode
        self.symbol_table = Memory(dumping_mode)

    def declaration(self,tree):
        children = tree.children

        var_type = children[0].value # 1er child -> Token -> type
        var_name = children[1].value # 2e  child -> Token -> Name

        self.symbol_table.declare(var_type, var_name) # Create new value object uninitialized

        if len(children) == 3: # if 3e Child -> Tree -> value
            value = self.visit(children[2]) # Visit the tree for the value
            self.symbol_table.set(var_name, value) # assignation of the value to the value object

    def assignation(self, tree):
        children = tree.children

        var_name = children[0].value    # 1er child -> Token -> Name
        value = self.visit(children[1]) # 2e child -> Tree -> Visit for get the value

        self.symbol_table.set(var_name, value)  # assignation of the value to the value object

    def afficher(self, tree):
        result = []
        for child in tree.children:
            if isinstance(child, Tree):
                result.append(self.visit(child))
            elif isinstance(child, Token):
                value = self.symbol_table.get(child.value)
                result.append(str(value.get_value()))
        printed = ' '.join(result)
        print(printed)

    def entier(self, tree):
        return int(tree.children[0])

    def chaine(self,tree):
        return tree.children[0].value[1:-1]

    def booleen(self,tree):
        return tree.children[0].value == 'vrai'

    def liste(self,tree):
        list = []
        for child in tree.children:
            list.append(child)
        return list