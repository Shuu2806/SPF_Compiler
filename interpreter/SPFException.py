class SPFException(Exception):
    pass

class SPFSyntaxError(SPFException):
    pass

class SPFUnknownVariable(SPFException):
    pass

class SPFUninitializedVariable(SPFException):
    pass

class SPFAlreadyDefined(SPFException):
    pass

class SPFIncompatibleType(SPFException):
    pass

class SPFIndexError(SPFException):
    pass