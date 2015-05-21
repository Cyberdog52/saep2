def main(x):
    return f( g(f(2,x)), g(f(2,1)) )

def f(x, y):
    return x*y

def g(x): 
    return x + 2;
