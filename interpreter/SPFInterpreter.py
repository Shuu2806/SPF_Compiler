from interpreter.SPFException import *
import sys
from interpreter.type import Type
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
            print(f"[TRACE] {func.__name__} a retourné {result!r}", file=sys.stderr)
        return result
    return wrapper

def exception_handler(func):
    @wraps(func)
    def wrapper(self,*args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            current_tree = args[0]

            print(f"[ERROR] Erreur d'exécution à la ligne {current_tree.meta.line} : {e}")

            raise Exception("Execution error")
    return wrapper

class SPFInterpreter(Interpreter):

    def __init__(self, dumping_mode=False, tracing_mode=False):
        super().__init__()
        self.tracing_mode = tracing_mode
        self.symbol_table = Memory(dumping_mode)

    @exception_handler
    def declare(self,tree):
        children = tree.children

        var_type = children[0].value
        var_name = children[1].value

        self.symbol_table.declare(var_type, var_name)

        if self.tracing_mode:
            if len(children) == 3:
                print(f"[TRACE] declare : {var_type} {var_name} = {self.visit(children[2])} \n", file=sys.stderr)
            else:
                print(f"[TRACE] declare : {var_type} {var_name} \n", file=sys.stderr)

        if len(children) == 3:
            value = self.visit(children[2])
            self.symbol_table.set(var_name, value)

    @exception_handler
    def assign(self, tree):
        children = tree.children

        var_name = children[0].value
        value = self.visit(children[1])

        if self.tracing_mode:
            print(f"[TRACE] modifie : {var_name} = {value} \n", file=sys.stderr)

        self.symbol_table.set(var_name, value)

    @exception_handler
    def print_exp(self, tree):
        children = tree.children
        result = []

        for child in children:
            value = self.visit(child)
            result.append(str(value))

        printed = " ".join(result)
        print(printed)

    # ========= for loop ==========

    @exception_handler
    def for_loop(self, tree):
        children = tree.children

        var_type = children[0].value
        var_name = children[1].value

        iterable = self.visit(children[2])

        if not isinstance(iterable, (list,str)):
            raise Exception(f"Invalid type for '{iterable}' is not a iterable")

        self.symbol_table.enter_scope()
        self.symbol_table.declare(var_type, var_name)

        for value in iterable:
            self.symbol_table.set(var_name, value)
            self.visit(children[3])

        self.symbol_table.exit_scope()

    # ========= while loop ==========

    @exception_handler
    def while_loop(self, tree):
        children = tree.children

        condition = self.visit(children[0])

        if not isinstance(condition, bool):
            raise Exception(f"Invalid type for while condition")

        self.symbol_table.enter_scope()

        while condition:
            self.visit(children[1])
            condition = self.visit(children[0])

        self.symbol_table.exit_scope()

    # ========= if statement ==========

    @exception_handler
    def if_else(self,tree):
        children = tree.children

        condition = self.visit(children[0])

        if not isinstance(condition, bool):
            raise Exception(f"Invalid type for if condition")

        self.symbol_table.enter_scope()
        if len(children) == 3: # if-else

            if condition:
                self.visit(children[1])
            else:
                self.visit(children[2])

        else: # if

            if condition:
                self.visit(children[1])

        self.symbol_table.exit_scope()

    # ========== Bool ==========

    @exception_handler
    def exp_or(self,tree):
        children = tree.children

        left = self.visit(children[0])
        right = self.visit(children[1])

        return left or right

    @exception_handler
    def exp_and(self,tree):
        children = tree.children

        left = self.visit(children[0])
        right = self.visit(children[1])

        return left and right

    @exception_handler
    def exp_not(self,tree):
        children = tree.children

        child = self.visit(children[0])

        if not (isinstance(child, bool)):
            return Exception(f"Invalid type for not operation")

        return not child

    @exception_handler
    def operation_comparator(self, tree):
        children = tree.children

        left = self.visit(children[0])
        operator = children[1].value
        right = self.visit(children[2])

        return (left == right) if operator in ("==","vaut") else (left != right)

    @exception_handler
    def operation_math_comparator(self,tree):
        children = tree.children

        left = self.visit(children[0])
        operator = children[1].value
        right = self.visit(children[2])

        if not (isinstance(left, int) & isinstance(right, int)):
            return Exception(f"Invalid type for {operator} operation")

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

    @exception_handler
    def exp_additive(self,tree):
        children = tree.children

        left = self.visit(children[0])
        operator = children[1].value
        right = self.visit(children[2])

        if type(left) != type(right):
            return Exception(f"Incompatible types for {operator} operation: {type(left)} + {type(right)}")

        if isinstance(left,bool) or isinstance(right,bool):
            return Exception(f"Invalid type for {operator} operation: {type(left)} + {type(right)}")

        return (left + right) if operator == "+" else (left - right)

    @exception_handler
    def exp_multiplicative(self,tree):
        children = tree.children

        left = self.visit(children[0])
        operator = children[1].value
        right = self.visit(children[2])

        if not (isinstance(left, int) & isinstance(right, int)):
            return Exception(f"Invalid type for {operator} operation")

        return (left * right) if operator == "*" else (int(left / right))

    @exception_handler
    def exp_neg(self,tree):
        children = tree.children

        child = self.visit(children[0])

        if not isinstance(child, int):
            raise Exception("Invalid type for negation")

        return -child

    # ========== List op ==========

    @exception_handler
    def list_value(self,tree):
        children = tree.children
        list = []
        for child in children:
            list.append(self.visit(child))
        return list

    @exception_handler
    def add_to_list(self,tree):
        children = tree.children

        value_to_add = self.visit(children[0])
        var_name = children[1].value

        # Throw exception if variable is not declared or initialized
        var = self.symbol_table.get(var_name)

        if var.get_type() != Type.liste:
            raise Exception(f"Variable '{var_name}' is not a list")

        new_list = var.get_value()
        new_list.append(value_to_add)

        self.symbol_table.set(var_name, new_list)

    @exception_handler
    def list_range(self,tree):
        children = tree.children

        start = self.visit(children[0])
        end = self.visit(children[1])

        if not (isinstance(start, int) & isinstance(end, int)):
            raise Exception("Invalid range")

        if start > end:
            raise Exception("Invalid range")

        return list(range(start, end + 1))

    @exception_handler
    def list_index(self,tree):
        children = tree.children

        var_name = children[0].value
        index = self.visit(children[1])

        if not isinstance(index, int):
            raise Exception(f"Invalid type for index '{index}' is not an int")

        index -= 1 # reduit l'index de 1 pour le faire correspondre à la liste

        # Throw exception if variable is not declared or initialized
        var = self.symbol_table.get(var_name)

        if var.get_type() != Type.liste:
            raise Exception(f"Variable '{var_name}' is not a list")

        new_list = var.get_value()

        if index < 0 or index >= len(new_list):
            raise Exception(f"Index {index} out of range for list '{var_name}'")

        return new_list[index]

    @exception_handler
    def list_size(self,tree):
        children = tree.children

        variable = self.visit(children[0])

        if not isinstance(variable, (list,str)):
            raise Exception(f"Invalid type for '{variable}' is not a list or string")

        return len(variable)

    # ========== Basic ==========

    @exception_handler
    def variable_value(self,tree):
        children = tree.children
        var_name = children[0].value

        # Throw exception if variable is not declared or initialized
        var = self.symbol_table.get(var_name)
        value = var.get_value()

        if self.tracing_mode:
            print(f"[TRACE] accède : {var_name} = {value} \n", file=sys.stderr)

        return value

    @exception_handler
    def number_value(self, tree):
        children = tree.children
        return int(children[0])

    @exception_handler
    def string_value(self,tree):
        children = tree.children
        return children[0].value[1:-1]

    @exception_handler
    def boolean_value(self, tree):
        children = tree.children
        return children[0].value == 'vrai'