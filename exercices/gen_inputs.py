import random
random.seed(1234)
with open("inputs.dat", "w") as fp:
    for _ in xrange(5000):
        for _ in xrange(5000):
            fp.write("{0},".format(random.random()))
        fp.write("\n")
