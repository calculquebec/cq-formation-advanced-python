def approx_pi(int intervals):
    cdef double pi
    cdef int i
    pi = 0.0
    for i in range(intervals):
        pi += (4 - 8 * (i % 2)) / (float)(2 * i + 1)
    return pi
