def main(x,y):
    
    if(y != 0):

        assert(y%y == 0)
        assert((y*x)%y == 0)
        assert(0%y == 0)

        if(x == 2):
            return x%3 # = 2
        elif(x == 3):
            return x%2 # = 1
        elif(x == 4):
            return -1%x # = 3
        elif(x == 5):
            return -(-(4%x)) # = 4
            
    return -1


def expected_result():
    return [1,2,3,4,-1]

