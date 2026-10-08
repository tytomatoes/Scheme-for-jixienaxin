from model import Symbol, Pair, NIL, Closure
def format_value(x):
    if x is True: return '#t'
    if x is False: return '#f'
    if x is NIL: return '()'
    if isinstance(x,Symbol): return str(x)
    if type(x) is str:
        x = x.replace('\\','\\\\').replace('"','\\"').replace('\n','\\n').replace('\t','\\t')
        return '"' + x + '"'
    if isinstance(x,Pair):
        parts = []
        while isinstance(x,Pair):
            parts.append(format_value(x.first)); x = x.rest
        if x is not NIL: parts.extend(['.',format_value(x)])
        return '(' + ' '.join(parts) + ')'
    if isinstance(x,Closure) or callable(x): return '#<procedure>'
    return str(x)
