def main(x): 
    if(x == 0):
        return 11/10 # =1
    elif(x == 1):
        return x - 20 / 4 + 8 # =4
    elif(x == 2):
        return -10 / -x # =5
    elif(x == 3):
        return 15/-x #=-5
    elif(x == 4):
        return x / (x-(x/2)) * 2 + 2 #= 6
    else:
        return -1

def expected_result():
    return [1,4,5,-5,6,-1]