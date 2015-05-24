def main(x):
    if(x == 1):
        return x * x # =1
    elif(x == 2):
        return x * 3 # =6
    elif(x == 3):
        return 2 * (3+1) # =8
    elif(x == 4):
        return (x-1) * x - 2 # =10
    else:
        return -1

def expected_result():
    return [1,6,8,10,-1]

