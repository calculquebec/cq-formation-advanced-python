import sys
import math
import time
import numpy

from numba.pycc import CC

cc = CC('approx_pi')

@cc.export('approx_pi', 'f8(i4)')
def approx_pi(intervals):
    pi1 = 4/numpy.arange(1, intervals, 4)
    pi2 = -4/numpy.arange(3, intervals, 4)
    return numpy.sum(pi1) + numpy.sum(pi2)

if __name__ == "__main__":
    cc.compile()
