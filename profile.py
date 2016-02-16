import sys
import time
import random

random.seed(1234)

def gen_data(n):
    numbers = []
    for i in range(n):
        numbers.append(random.random())
    return numbers

def sum_nexts(numbers):
    sums = []
    for i in range(len(numbers)):
        for j in range(i+1, len(numbers)):
            if len(sums) < i+1:
                sums.append(0.)
            sums[i] = sums[i] + numbers[j]
    return sums

def main(n):
    numbers = gen_data(n)
    sums = sum_nexts(numbers)
    return sums

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: {0} <n>\n".format(sys.argv[0]))
        sys.exit(1)

    n = int(sys.argv[1])
    main(n)
