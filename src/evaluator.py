"""Special forms control evaluation; closures capture their defining environment."""
from model import Symbol, Pair, Closure, NIL, Env, make_list, list_items, number, truth, eq, equal
def sequence(xs,env):
    result = None
    for x in xs: result = evaluate(x,env)
    return result
def parameters(x):
    names = list_items(x)
    if not all(isinstance(n,Symbol) for n in names) or len(set(names))!=len(names): raise SyntaxError('invalid parameters')
    return names
def apply(proc,args):
    if isinstance(proc,Closure):
        if len(args)!=len(proc.params): raise TypeError('wrong argument count')
        return sequence(proc.body,Env(zip(proc.params,args),proc.env))
    if callable(proc): return proc(*args)
    raise TypeError('operator is not a procedure')
def evaluate(x,env):
    if isinstance(x,Symbol): return env.lookup(x)
    if not isinstance(x,Pair): return x
    items = list_items(x); op,args=items[0],items[1:]
    if isinstance(op,Symbol):
        if op=='quote':
            if len(args)!=1: raise SyntaxError('quote needs one argument')
            return args[0]
        if op=='if':
            if len(args) not in (2,3): raise SyntaxError('invalid if')
            if truth(evaluate(args[0],env)): return evaluate(args[1],env)
            return evaluate(args[2],env) if len(args)==3 else None
        if op=='cond':
            for clause in args:
                parts=list_items(clause)
                test=True if isinstance(parts[0],Symbol) and parts[0]=='else' else evaluate(parts[0],env)
                if truth(test): return sequence(parts[1:],env) if len(parts)>1 else test
            return None
        if op=='and':
            value=True
            for arg in args:
                value=evaluate(arg,env)
                if value is False: break
            return value
        if op=='or':
            for arg in args:
                value=evaluate(arg,env)
                if truth(value): return value
            return False
        if op=='define':
            target=args[0]
            if isinstance(target,Pair): name,value=target.first,Closure(parameters(target.rest),args[1:],env)
            else:
                if len(args)!=2: raise SyntaxError('invalid define')
                name,value=target,evaluate(args[1],env)
            if not isinstance(name,Symbol): raise SyntaxError('invalid definition name')
            env[name]=value
            return name
        if op=='lambda': return Closure(parameters(args[0]),args[1:],env)
        if op=='let':
            bindings=[]
            for binding in list_items(args[0]):
                name,expression=list_items(binding)
                if not isinstance(name,Symbol): raise SyntaxError('invalid let binding')
                bindings.append((name,evaluate(expression,env)))
            return sequence(args[1:],Env(bindings,env))
        if op=='begin': return sequence(args,env)
    proc=evaluate(op,env)
    return apply(proc,[evaluate(arg,env) for arg in args])
