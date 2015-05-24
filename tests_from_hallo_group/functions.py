def main(x):
    # main(0) = 8
    return f( g(f(2,x)), g(f(2,1)) )

def f(x, y):
    return x*y

def g(x): 
    return x + 2;
