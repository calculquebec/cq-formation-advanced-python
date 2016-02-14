import sys
import math
import time

from numba import jit

@jit
def approx_pi(intervals):
    pi = 0.0
    for i in range(intervals):
        pi += (4 - 8 * (i % 2)) / (float)(2 * i + 1)
    return pi

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print >> sys.stderr, "usage: {0} <intervals>".format(sys.argv[0])
        sys.exit(1)

    t1 = time.clock()
    pi = approx_pi(int(sys.argv[1]))
    t2 = time.clock()
    print("PI is approximately %.16f, Error is %.16f"%(pi, abs(pi - math.pi)))
    print("Time = %.16f sec\n"%(t2 - t1))
