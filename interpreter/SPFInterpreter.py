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
    def declare(self,tree):
        children = tree.children

        var_type = children[0].value
        var_name = children[1].value

        self.symbol_table.declare(var_type, var_name)

        if len(children) == 3:
            value = self.visit(children[2])
            self.symbol_table.set(var_name, value)

    @trace
    def assign(self, tree):
        children = tree.children

        var_name = children[0].value
        value = self.visit(children[1])

        self.symbol_table.set(var_name, value)

    def print_exp(self, tree):
        children = tree.children
        result = []

        for child in children:
            value = self.visit(child)
            result.append(str(value))

        printed = " ".join(result)
        print(printed)

    # ========== Bool ==========

    def exp_or(self,tree):
        children = tree.children

        left = self.visit(children[0])
        right = self.visit(children[1])

        return left or right

    def exp_and(self,tree):
        children = tree.children

        left = self.visit(children[0])
        right = self.visit(children[1])

        return left and right

    def exp_not(self,tree):
        children = tree.children

        child = self.visit(children[0])

        return not child

    def operation_comparator(self, tree):
        children = tree.children

        left = self.visit(children[0])
        operator = children[1].value
        right = self.visit(children[2])

        return (left == right) if operator == "==" else (left != right)

    def operation_math_comparator(self,tree):
        children = tree.children

        left = self.visit(children[0])
        operator = children[1].value
        right = self.visit(children[2])

        match operator:
            case "<":
                return left < right
            case ">":
                return left > right
            case "<=":
                return left <= right
            case ">=":
                return left >= right

    # ========== Math ==========

    def exp_additive(self,tree):
        children = tree.children

        left = self.visit(children[0])
        operator = children[1].value
        right = self.visit(children[2])

        return (left + right) if operator == "+" else (left - right)

    def exp_multiplicative(self,tree):
        children = tree.children

        left = self.visit(children[0])
        operator = children[1].value
        right = self.visit(children[2])

        if not (isinstance(left, int) & isinstance(right, int)): #TODO : raise exception incompatible type
            return

        return (left * right) if operator == "*" else (int(left / right))

    def exp_neg(self,tree):
        children = tree.children

        child = self.visit(children[0])

        return -child

    # ========== Basic ==========

    def variable_value(self,tree):
        children = tree.children
        var_name = children[0].value

        # Throw exception if variable is not declared or initialized
        var = self.symbol_table.get(var_name)
        value = var.get_value()

        return value

    def number_value(self, tree):
        children = tree.children
        return int(children[0])

    def string_value(self,tree):
        children = tree.children
        return children[0].value[1:-1]

    def boolean_value(self, tree):
        children = tree.children
        return children[0].value == 'vrai'

    def liste(self,tree):
        children = tree.children
        list = []
        for child in children:
            list.append(self.visit(child))
        return list