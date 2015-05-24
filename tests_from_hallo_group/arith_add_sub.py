def main(x):
    assert(x == x + 1 -1)
    if(x == 0):
        return x + 0 #=0
    elif(x == 1):
        return x + 15 + x # 17
    elif(x == 2):
        return x + x - x + 3 - 2 - 1 #=2
    else:
        return -1

def expected_result():
    return [0, 17, 2, -1]

