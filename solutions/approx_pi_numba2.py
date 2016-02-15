from __future__ import division

import sys
import math
import time
import numpy

from numba import jit

@jit
def approx_pi(intervals):
    pi1 = 4/numpy.arange(1, intervals, 4)
    pi2 = -4/numpy.arange(3, intervals, 4)
    return numpy.sum(pi1) + numpy.sum(pi2)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print >> sys.stderr, "usage: {0} <intervals>".format(sys.argv[0])
        sys.exit(1)

    t1 = time.clock()
    pi = approx_pi(int(sys.argv[1]))
    t2 = time.clock()
    print("PI is approximately %.16f, Error is %.16f"%(pi, abs(pi - math.pi)))
    print("Time = %.16f sec\n"%(t2 - t1))
