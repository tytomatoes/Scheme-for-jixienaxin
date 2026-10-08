"""Lexer and recursive reader, including strings, comments and dotted pairs."""
import re
from model import Symbol, make_list
TOKEN = re.compile(r';[^\n]*|"(?:\\.|[^"\\])*"|[()\']|[^\s()\'";]+')
def parse(source):
    tokens = [t for t in TOKEN.findall(source) if not t.startswith(';')]
    i = 0
    def read():
        nonlocal i
        if i >= len(tokens): raise SyntaxError("unexpected end")
        t = tokens[i]; i += 1
        if t == "'": return make_list([Symbol('quote'),read()])
        if t == '(':
            values = []
            while i < len(tokens) and tokens[i] != ')':
                if tokens[i] == '.':
                    if not values: raise SyntaxError("invalid dotted pair")
                    i += 1; tail = read()
                    if i >= len(tokens) or tokens[i] != ')': raise SyntaxError("invalid dotted pair")
                    i += 1
                    return make_list(values,tail)
                values.append(read())
            if i >= len(tokens): raise SyntaxError("unclosed list")
            i += 1
            return make_list(values)
        if t == ')': raise SyntaxError("unexpected closing parenthesis")
        if t.startswith('"'):
            escapes = {'n':'\n','t':'\t','"':'"','\\':'\\'}
            return re.sub(r'\\(.)',lambda m: escapes[m[1]],t[1:-1])
        if t == '#t': return True
        if t == '#f': return False
        if re.fullmatch(r'[+-]?[0-9]+',t): return int(t)
        if re.fullmatch(r'[+-]?(?:[0-9]+\.[0-9]*|\.[0-9]+)(?:[eE][+-]?[0-9]+)?',t): return float(t)
        return Symbol(t)
    while i < len(tokens): yield read()
