from interpreter.SPFException import *
from interpreter.type import Type,get_type

class Value:
    def __init__(self):
        self.var_type = None
        self.var_value = None
        self.is_declared = False
        self.is_initialized = False

    def declare(self, var_type):
        self.var_type = Type(var_type)
        self.is_declared = True

    def set(self, var_value):
        if not self.is_declared:
            raise SPFUnknownVariable()

        if get_type(var_value) != self.var_type:
            raise SPFIncompatibleType()

        self.var_value = var_value
        self.is_initialized = True

    def get_value(self):
        return self.var_value

    def get_type(self):
        return self.var_type

    def __repr__(self):
        if not self.is_declared:
            return "<(Undeclared)>"
        if not self.is_initialized:
            return f"<(uninitialized) type={self.var_type}>"
        return f"<type={self.var_type},value={self.var_value}>"