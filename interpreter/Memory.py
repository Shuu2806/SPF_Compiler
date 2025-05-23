from interpreter.Value import Value
import sys
from functools import wraps
from interpreter.SPFException import *

def dump(func):
    @wraps(func)
    def wrapper(self,*args, **kwargs):
        result = func(self, *args, **kwargs)
        if self.dumping_mode:
            print("[DUMP] Memory :" ,file=sys.stderr)
            for level in self.vars:
                print(f"    [DUMP] Scope {level} :", file=sys.stderr)
                for var_name, var in self.vars[level].items():
                    print(f"        [DUMP]  {var.get_type()} {var_name} : {var.get_value()} ", file=sys.stderr)
        print(file=sys.stderr)
        return result
    return wrapper

class Memory:

    @dump
    def __init__(self,dumping_mode = False):
        self.dumping_mode = dumping_mode
        self.code_level = 1
        self.vars = {}
        self._ensure_scope_exists()

    def _ensure_scope_exists(self):
        if self.code_level not in self.vars:
            self.vars[self.code_level] = {}

    def enter_scope(self):
        self.code_level += 1
        self._ensure_scope_exists()

    def exit_scope(self):
        del self.vars[self.code_level]
        self.code_level -= 1

    @dump
    def declare(self, var_type, variable):
        new_var = Value()
        new_var.declare(var_type)

        if not variable in self.vars[self.code_level]:
            self.vars[self.code_level][variable] = new_var
            return self.vars[self.code_level][variable]
        else:
            raise SPFAlreadyDefined(f"Variable already defined {variable}")

    @dump
    def set(self, variable, value):
        current_var = self._get_var(variable)

        if current_var is None: # Si n'a pas trouver la variable, La variable n'a pas été déclarer
            raise SPFUnknownVariable(f"Variable not declared {variable}")
        else: # sinon set la variable avec la nouvelle valeur
            current_var.set(value)
            return current_var

    def get(self, variable):
        current_var = self._get_var(variable)
        if current_var is None: # Si n'a pas trouver la variable, La variable n'a pas été déclarer
            raise SPFUnknownVariable(f"Variable not declared {variable}")
        else: # sinon set la variable avec la nouvelle valeur
            if not current_var.is_initialized:
                raise SPFUninitializedVariable(f"Variable not initialized {variable}")
            else:
                return current_var

    # Check si il y a une variable du nom de la variable dans le scope le plus petit. si il ne trouve pas augmente le scope
    def _get_var(self,variable):
        current_level = self.code_level
        current_var = None

        while current_level > 0:
            if variable in self.vars[current_level]:
                current_var = self.vars[current_level][variable]
                break
            current_level -= 1

        return current_var