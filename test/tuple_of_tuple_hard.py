def main(x):
    (a, b) = ((10,x-1), (x, x+1))
    if b == (0, 1):
        return 1
    elif b == (1, 3):
        return 15
    else:
        return 20

def expected_result():
    return [1, 20]
