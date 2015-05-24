def main(x, y):
    if(x > y):
        assert(x-1 >= y)
    elif(x < y):
        assert(x <= y-1)
    return -1