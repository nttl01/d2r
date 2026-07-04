def print_color():
    for i in range(11):
        for j in range(10):
            n = 10 * i + j
            if n > 108:
                break
            print("\033["+str(n)+"m "+str(n)+"\033[m", end=' ')
        print()
 
print_color()