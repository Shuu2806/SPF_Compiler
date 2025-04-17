from lark import Tree, Token
from lark.visitors import Interpreter
from interpreter.Memory import Memory
from functools import wraps

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

#def exception_handler(func): #TODO REFAIRE AU PROPRE
#    @wraps(func)
#    def wrapper(self,*args, **kwargs):
#        try:
#            return func(self, *args, **kwargs)
#        except Exception as e:
#            current_token = args[0][0]
#
#            if isinstance(e, SPFUnknownVariable):
#                print(f"[ERROR] Line {current_token.line} : The variable '{current_token}' is not defined")
#            elif isinstance(e, SPFUninitializedVariable):
#                print(f"[ERROR] Line {current_token.line} : The variable '{current_token}' is not initialized")
#            elif isinstance(e, SPFAlreadyDefined):
#                current_token = args[0][1]
#                print(f"[ERROR] Line {current_token.line} : The variable '{current_token}' is already defined in this scope")
#            elif isinstance(e, SPFIncompatibleType):
#                print(f"[ERROR] Line {current_token.line} : Type error '{current_token}' blabla")
#
#            raise Exception
#    return wrapper

class SPFInterpreter(Interpreter):

    def __init__(self, dumping_mode=False, tracing_mode=False):
        super().__init__()
        self.tracing_mode = tracing_mode
        self.symbol_table = Memory(dumping_mode)

    @trace
    def declaration(self,tree):
        children = tree.children

        var_type = children[0].value # 1er child -> Token -> type
        var_name = children[1].value # 2e  child -> Token -> Name

        self.symbol_table.declare(var_type, var_name) # Create new value object uninitialized

        if len(children) == 3: # if 3e Child -> Tree -> value
            value = self.visit(children[2]) # Visit the tree for the value
            self.symbol_table.set(var_name, value) # assignation of the value to the value object

    @trace
    def assignation(self, tree):
        children = tree.children

        var_name = children[0].value    # 1er child -> Token -> Name
        value = self.visit(children[1]) # 2e child -> Tree -> Visit for get the value

        self.symbol_table.set(var_name, value)  # assignation of the value to the value object

    @trace
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

    # TODO BCP DE CODE DUPLIQUER PEUT OPTI
    # ========== Math expression ==========

    def expression_add(self, tree):
        children = tree.children

        left = self.visit(children[0])
        right = self.visit(children[1])

        return left + right

    def expression_sub(self, tree):
        children = tree.children

        left = self.visit(children[0])
        right = self.visit(children[1])

        return left - right

    def expression_mul(self, tree):
        children = tree.children

        left = self.visit(children[0])
        right = self.visit(children[1])

        return left * right

    def expression_div(self, tree):
        children = tree.children

        left = self.visit(children[0])
        right = self.visit(children[1])

        return int(left / right)

    def expression_neg(self, tree):
        children = tree.children

        child = self.visit(children[0])

        return -child

    # ========== Bool expression ==========

    def expression_or(self,tree):
        children = tree.children

        left = self.visit(children[0])
        right = self.visit(children[1])

        return left or right

    def expression_and(self,tree):
        children = tree.children

        left = self.visit(children[0])
        right = self.visit(children[1])

        return left and right

    def operation_equals(self,tree):
        children = tree.children

        left = self.visit(children[0])
        right = self.visit(children[1])

        return left == right

    def operation_not_equals(self,tree):
        children = tree.children

        left = self.visit(children[0])
        right = self.visit(children[1])

        return left != right

    def expression_not(self,tree):
        children = tree.children

        child = self.visit(children[0])

        return not child

    def operation_less_than_equal(self,tree):
        children = tree.children

        left = self.visit(children[0])
        right = self.visit(children[1])

        return left <= right

    def operation_less_than(self,tree):
        children = tree.children

        left = self.visit(children[0])
        right = self.visit(children[1])

        return left < right

    def operation_greater_than_equal(self,tree):
        children = tree.children

        left = self.visit(children[0])
        right = self.visit(children[1])

        return left >= right

    def operation_greater_than(self,tree):
        children = tree.children

        left = self.visit(children[0])
        right = self.visit(children[1])

        return left > right

    # ========== Basic ==========

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