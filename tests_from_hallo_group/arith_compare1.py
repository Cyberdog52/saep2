def main(x):

    if(x<2 and x>0):
        return x # = 1
    elif(x == 2):
        return x # = 2
    elif(x != 2 and x<4 and x > 1):
        return x # = 3
    elif((x == 3 or x == 4 or x == 5) and x != 5):
        return x # = 4
    else:
        return -1

def expected_result():
    return [1,2,3,4,-1]

