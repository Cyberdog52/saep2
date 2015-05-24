# Checks Arithmetic operations and complex function calls

def main(x):
    if(x == 0):
        return x + 2
    elif(x == 1):
        return x + 0 - 1 + x #=1
    elif(x == 2):
        return x * 10 - 18 #=2
    elif(x == 3):
        a = foo(foo(x, 1, -1), foo(bar(foo(bar(0),1,-1)),0, 0), foo(x,x,0))
        return ((((((a))))))/3 #=3
    elif(x == 4):
        return ((x%3)*x)%5 #=4
    else:
        return -1
def expected_result():
    return [1,2,3,4,-1]

def foo(x, y, z):
    return x + y + z

def bar(bara):
    return bara

