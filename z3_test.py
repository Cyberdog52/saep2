#!/usr/bin/python

from z3 import *

x = Int('x')
y = Int('y')
dummy_variable = Int('d')
s = Solver()
#s.add(x > 0)
s.add(x > 2)
print s

#s.add(y == x + 1)

print(s.check())
if (s.check() == sat):
    print(s.model())

# Extracts variables used from a Z3 expression
# Taken from http://z3.codeplex.com/SourceControl/changeset/view/fbce8160252d#src/api/python/z3util.py
def get_vars(f):
    r = set()
    def collect(f):
        if is_const(f):
            if f.decl().kind() == Z3_OP_UNINTERPRETED and not askey(f) in r:
                r.add(askey(f))
        else:
            for c in f.children():
                collect(c)
    collect(f)
    return [str(var.n) for var in r]

# Wrapper for allowing Z3 ASTs to be stored into Python Hashtables.
class AstRefKey:
    def __init__(self, n):
        self.n = n
    def __hash__(self):
        return self.n.hash()
    def __eq__(self, other):
        return self.n.eq(other.n)
    def __repr__(self):
        return str(self.n)

def askey(n):
    assert isinstance(n, AstRef)
    return AstRefKey(n)


x,y = Ints('x y')
a,b = Bools('a b')
print (get_vars(Implies(And(x + y == 0, x*2 == 10),Or(a, Implies(a, b == False)))))