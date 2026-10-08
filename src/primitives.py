"""Spec-defined builtins; integer division truncates toward zero exactly."""
import math
import operator
from model import Symbol, Pair, Closure, NIL, Env, make_list, list_items, number, truth, eq, equal
from printer import format_value
def numeric(xs):
    if not all(number(x) for x in xs): raise TypeError('expected numbers')
    return xs
def trunc_div(a,b):
    if b == 0: raise ZeroDivisionError('division by zero')
    return (-1 if (a<0)!=(b<0) else 1)*(abs(a)//abs(b))
def add(*xs): return sum(numeric(xs))
def mul(*xs): return math.prod(numeric(xs))
def sub(a,*xs):
    numeric((a,)+xs)
    return a-sum(xs) if xs else -a
def div(a,*xs):
    numeric((a,)+xs)
    if not xs: return 1/a
    for b in xs: a = trunc_div(a,b) if type(a) is int and type(b) is int else a/b
    return a
def quotient(a,b):
    if type(a) is not int or type(b) is not int: raise TypeError('expected integers')
    return trunc_div(a,b)
def numeric_fn(fn):
    def call(*xs): return fn(*numeric(xs))
    return call
def compare(fn):
    def call(*xs):
        if any(type(x) is bool for x in xs): raise TypeError('boolean is not numeric')
        return all(fn(a,b) for a,b in zip(xs,xs[1:]))
    return call
def pair(x):
    if not isinstance(x,Pair): raise TypeError('expected pair')
    return x
def proper(x):
    while isinstance(x,Pair): x = x.rest
    return x is NIL
def append(*xs):
    if not xs: return NIL
    result = xs[-1]
    for x in reversed(xs[:-1]): result = make_list(list_items(x),result)
    return result
def display(x): print(x if type(x) is str else format_value(x),end='')
def newline(): print()
def initial_env():
    values = {'+':add,'-':sub,'*':mul,'/':div,'quotient':quotient,
      'modulo':numeric_fn(operator.mod),'expt':numeric_fn(operator.pow),'abs':numeric_fn(abs),
      'not':lambda x:not truth(x),'cons':Pair,'car':lambda x:pair(x).first,'cdr':lambda x:pair(x).rest,
      'list':lambda *xs:make_list(xs),'length':lambda x:len(list_items(x)),'append':append,
      'null?':lambda x:x is NIL,'pair?':lambda x:isinstance(x,Pair),'list?':proper,
      'number?':number,'boolean?':lambda x:type(x) is bool,'symbol?':lambda x:isinstance(x,Symbol),
      'string?':lambda x:type(x) is str,'procedure?':lambda x:isinstance(x,Closure) or callable(x),
      'zero?':numeric_fn(lambda x:x==0),'even?':numeric_fn(lambda x:x%2==0),'odd?':numeric_fn(lambda x:x%2!=0),
      'eq?':eq,'equal?':equal,'display':display,'newline':newline}
    for name,fn in [('=',operator.eq),('<',operator.lt),('>',operator.gt),('<=',operator.le),('>=',operator.ge)]: values[name]=compare(fn)
    return Env(values)
