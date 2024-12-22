#!/usr/bin/python
 
# calculate factorial of n
def fact(n):

    # no work required
    if n == 1 or n == 0:
        return 1

    # minimum amount of work
    return n * fact(n - 1)

n = 5

# calculate factorial
factorial = fact(n)
print(f"{n}! = {factorial}")