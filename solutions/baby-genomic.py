import numpy as np
from multiprocessing import Pool


def editDistance(seqA, seqB):
    # Sequence A is vertical (k < M)
    # Sequence B is horizontal (l < N)
    M = len(seqA)
    N = len(seqB)

    allAs = np.tile(np.array(list(seqA)), (N, 1)).T
    allBs = np.tile(np.array(list(seqB)), (M, 1))
    diffs = (allAs != allBs)

    # Dynamic algorithm
    mat = np.tile(0, (M + 1, N + 1))
    mat[:,0] = np.arange(M + 1)
    mat[0,:] = np.arange(N + 1)

    for k in xrange(0, M):
        for l in xrange(0, N):
            mat[k + 1, l + 1] = min(
                mat[k    , l    ] + (1 if diffs[k, l] else 0),
                mat[k    , l + 1] + 1,
                mat[k + 1, l    ] + 1)

    return 'Edit_Dist(%s..., %s...) = %s'%(seqA[:24], seqB[:24], mat[-1,-1])


def edProxy(twoSeq):
    return editDistance(twoSeq[0], twoSeq[1])


def printRes(results):
    for result in results:
        print(result)


def main():
    N = 500
    base = ['a','c','g','t']
    seqPairs = []

    np.random.seed(1234)

    for i in xrange(8):
        seqA = ''.join([base[np.random.randint(0, 4)] for i in xrange(N)])
        seqB = ''.join([base[np.random.randint(0, 4)] for i in xrange(N)])
        seqPairs.append([seqA, seqB])

    # Use edProxy for an easy asynchronous map call
    # Use printRes as a callback function
    workers = Pool(processes=2)
    workers.map_async(edProxy, seqPairs, callback=printRes)
    workers.close()
    workers.join()


if __name__ == '__main__':
    main()
