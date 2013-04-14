""" 
Pfactory 0.1.1 -  a crappy implementation of Factor (http://factorcode.org)
                    as a Python DSL
"""
from StringIO import StringIO
import tokenize
import inspect

DEBUG = False

ignored_tokens = {
    tokenize.NL,
    tokenize.COMMENT,
    tokenize.ENDMARKER
}

FN_OPEN = object()
FN_CLOSE = object()

# all are assumed to take one arg unless specified here
BUILTIN_FN_ARG_COUNTS = {
    'filter': 2
}

class QuotedFn(object):
    def __init__(self, fn):
        self.fn = fn
        
    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)

def parse(src):
    tokens = tokenize.generate_tokens(StringIO(src).readline)
    program = []
    for (t_type, t_str, _, _, _) in tokens:
        if t_type in ignored_tokens: continue
        
        if DEBUG:
            print "PARSING TOKEN", "type:", t_type, "| token str:", t_str
        
        if t_type == tokenize.OP and t_str == "[":
            obj = FN_OPEN
        elif t_type == tokenize.OP and t_str == "]":
            obj = FN_CLOSE
        
        # Operators are really functions with infix notation
        elif t_type == tokenize.OP:
            obj = operator_to_fn(t_str)

        else:
            frame = inspect.currentframe().f_back
            obj = eval(t_str, frame.f_globals, frame.f_locals)
            
        program.append(obj)

    while last_index_of(program, FN_OPEN) is not None:
        start = last_index_of(program, FN_OPEN)
        end = program.index(FN_CLOSE, start)
        
        sub_prog = program_to_fn(program[start+1:end])
        
        program = program[:start] + [QuotedFn(sub_prog)] + program[end+1:]
        
    return program_to_fn(program)
        
def program_to_fn(program):
    if DEBUG:
        print "COMPILING:", program
        
    def prog(*args):
        stack = list(args)
        for token in program:
            if DEBUG:
                print "STACK:", stack
            if isinstance(token, QuotedFn):
                stack.append(token.fn)
            elif callable(token):
                if getattr(token, "_pfractory_fn", False):
                    args_count = len(stack)
                else:
                    args_count = args_accepted(token)
    
                to_push = token(*stack[-args_count:])
            
                if to_push is None: 
                    to_push = ()
                elif not isinstance(to_push, tuple): 
                    to_push = (to_push,)
            
                stack = stack[:-args_count] + list(to_push)
            else:
                stack.append(token)
        
        if len(stack) == 0: return None
        elif len(stack) == 1: return stack[0]
        else: return tuple(stack)
        
    prog._pfactory_fn = True
    return prog
    
def args_accepted(fn):
    if inspect.isbuiltin(fn):
        return BUILTIN_FN_ARG_COUNTS.get(fn.__name__, 1)
    else:
        return len(inspect.getargspec(fn).args)
            
def operator_to_fn(operator):
    return lambda a, b: eval("a {} b".format(operator))

def last_index_of(lst, val):
    try:
        return (len(lst) - 1) - lst[::-1].index(val)
    except ValueError:
        return None
        
if __name__ == "__main__":   
    assert parse("3 2 -")() == 1
    assert parse("2 -")(3) == 1
    assert parse("3 2 *")() == 6
    assert parse("2 3 * 4 5 * +")() == 26
    
    countWhere = parse("filter len")
    assert countWhere(lambda x: x < 3, range(5)) == 3
    
    # python's filter kind of sucks for use in factor because the data is not
    # the first argument
    fltr = lambda data, fn: filter(fn, data)
    countWhere = parse("fltr len")
    assert parse("[2 >] countWhere")([1,2,3,4,5,]) == 3