def main(x):
    if(x > 0):
        if(x > 4):
            if(x > 6):
                if(x > 7):
                    return 8
                else:
                    return 7
            else:
                if(x > 5):
                    return 6
                else:
                    return 5
        else:
            if(x > 2):
                if(x > 3):
                    return 4
                else:
                    return 3
            else:
                if(x > 1):
                    return 2
                else:
                    return 1
    else:
        return -1
        

def expected_result():
    return [1,2,3,4,5,6,7,8, -1]

