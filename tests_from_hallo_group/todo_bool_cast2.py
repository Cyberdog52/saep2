def main(x):
    if(x == 1):
        return 0 + (x == 1) # = 1
    elif(x == 2):
        return 2 + False # = 2
    elif(x == 3):
        z = 1 + True + (2 == 2) # = 3
        return z
    elif(x == 4):
        z = -False + 4 # = 4
        return z
    elif(x == 5):
        z = -True * -5 # = 5
        return z
    elif(x == 6):
        z = (not True)+3*2 # = 6
        return z
    elif(x == 7):
        z = (((-True)<4)==1)+6 # = 7
        return z    
    else:
        return (x == 2) # = 0

def expected_result():
    return [1, 2, 3, 4, 5, 6, 7, 0]