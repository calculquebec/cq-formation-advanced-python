import sys
import time
import numpy

numpy.random.seed(int(time.time()))

def gen_data(n):
    return numpy.random.random(n)

def sum_nexts(numbers):
    sums = numpy.zeros(len(numbers))
    for i in range(len(numbers)):
        sums[i] = numbers[i+1:].sum()
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
