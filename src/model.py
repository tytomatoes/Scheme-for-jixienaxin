from dataclasses import dataclass
class Symbol(str):
    """A name, distinct from a Scheme string."""
class Empty: pass
NIL = Empty()
@dataclass(eq=False)
class Pair:
    first: object
    rest: object
@dataclass(eq=False)
class Closure:
    params: list
    body: list
    env: object
class Env(dict):
    def __init__(self, values=(), outer=None):
        super().__init__(values)
        self.outer = outer
    def lookup(self, name):
        if name in self: return self[name]
        if self.outer is not None: return self.outer.lookup(name)
        raise NameError(f"unbound symbol: {name}")
def truth(x): return x is not False
def number(x): return type(x) in (int, float)
def make_list(items, tail=NIL):
    for x in reversed(items): tail = Pair(x, tail)
    return tail
def list_items(x):
    result = []
    while isinstance(x, Pair):
        result.append(x.first)
        x = x.rest
    if x is not NIL: raise TypeError("expected proper list")
    return result
def eq(a,b):
    if number(a) and number(b): return a == b
    if type(a) is not type(b): return False
    if type(a) in (Symbol, bool): return a == b
    return a is b
def equal(a,b):
    if isinstance(a,Pair) and isinstance(b,Pair):
        return equal(a.first,b.first) and equal(a.rest,b.rest)
    if type(a) is str and type(b) is str: return a == b
    return eq(a,b)
