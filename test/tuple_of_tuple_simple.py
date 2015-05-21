def main(x):
    (a, b) = ((10,x-1), (x, x+1))
    (i,j) = b
    if j == 3:
        return 1
    elif i == 1:
        return 15
    else:
        return 20

def expected_result():
    return [1, 15, 20]
