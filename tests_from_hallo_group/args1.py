def main(x):
    if (x == 1):
        b = arg(x + 2, x * simple(1), -(simple(x)%5)) # = 3
        return b
    elif(x == 2):
        a = 1
        b = 2
        c = 3
        return arg(a, b, c) # = 6
    else:
        return -1
        

def expected_result():
    return [3,6, -1]

def arg(a, b, c):
    return a + b + c

def simple(z):
    return z * 2