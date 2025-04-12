from lark import Transformer

# décorateur trace / dump
def trace_and_dump(func):
    def wrapper(self, *args, **kwargs):
        name = func.__name__
        if self.tracing_mode:
            print(f"[TRACE] Appel de {name} avec args={args}")
        result = func(self, *args, **kwargs)
        if self.dumping_mode:
            print(f"[DUMP] Résultat de {name}: {result}")
        return result
    return wrapper


class SPFTransformer(Transformer):

    def __init__(self, dumping_mode=False, tracing_mode=False):
        self.dumping_mode = dumping_mode
        self.tracing_mode = tracing_mode
        self.variables = {}