from __future__ import division

def read_data():
    data = []
    fp = open("inputs.dat", "r")

    line = 1
    while line:
        line = fp.readline()
        if line:
            row = []
            for elem in line.split(','):
                elem = elem.strip()
                if elem:
                    row.append(float(elem))
            data.append(row)
        
    fp.close()
    return data

def process_A(data):
    """
    Return a new matrix of the same shape as data, with each original
    element squared by it's transposition equivalent.

    result[i][j] = data[i][j] ** data[j][i]
    """
    result = []
    for i in range(len(data)):
        row = []
        for j in range(len(data[i])):
            row.append(data[i][j] ** data[j][i])
        result.append(row)
    return result

def process_B(m1, m2):
    """
    Return the sum of the difference between each corresponding
    elements of two square matrices.

    diff = (m2[0][0] - m1[0][0]) + (m2[0][1] - m1[0][1]) + ...
    """

    diff = 0.
    for i in range(len(data)):
        for j in range(len(data[i])):
            diff += result_1[i][j] - data[i][j]
    return diff

def main():
    data = read_data()
    result_1 = process_A(data)
    print "Difference is: ", process_B(data, result_1)


if __name__ == "__main__":
    main()
