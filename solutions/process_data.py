from __future__ import division

import numpy

def read_data():
    data = None

    with open("inputs.dat", "r") as fp:
        lines = fp.readlines()
        n = len(lines)
        data = numpy.zeros((n,n),)

        for i in range(n):
            data[i] = numpy.array(map(lambda n: float(n), lines[i][:-2].split(',')))

    return data

def process_A(data):
    """
    Return a new matrix of the same shape as data, with each original
    element squared by it's transposition equivalent.

    result[i][j] = data[i][j] ** data[j][i]
    """
    return data ** data.transpose()

def process_B(m1, m2):
    """
    Return the sum of the difference between each corresponding
    elements of two square matrices.

    diff = (m2[0][0] - m1[0][0]) + (m2[0][1] - m1[0][1]) + ...
    """
    return numpy.sum(m2-m1)

if __name__ == "__main__":
    data = read_data()
    result_1 = process_A(data)
    print "Difference is: ", process_B(data, result_1)
