"""CLI entry: files share one global environment, otherwise read stdin."""
import sys
from pathlib import Path
from reader import parse
from evaluator import evaluate
from primitives import initial_env
from printer import format_value
def main():
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    env=initial_env()
    sources=(Path(p).read_text(encoding='utf-8-sig') for p in sys.argv[1:]) if len(sys.argv)>1 else [sys.stdin.read()]
    for source in sources:
        for expr in parse(source):
            result=evaluate(expr,env)
            if result is not None: print(format_value(result))
if __name__=='__main__':
    try: main()
    except (SyntaxError,NameError,TypeError,ValueError,ZeroDivisionError,RecursionError,OSError) as error:
        print(f'Error: {error}',file=sys.stderr)
        sys.exit(1)
