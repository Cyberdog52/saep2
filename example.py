from z3 import *

x = Real('x')
y = Real('y')
s = Solver()
s.add(x + y > 5, x > 3, y > 3)
print(s.check())
if (s.check() == sat):
	print(s.model())
