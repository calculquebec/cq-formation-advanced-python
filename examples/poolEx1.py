from multiprocessing import Pool

def prod(values):
    return values[0] * values[1]

if __name__ == '__main__':
    N = 10
    values = [(i + 1, N - i)
              for i in range(0, N)]
    print(values)

    workers = Pool(processes=2)
    results = workers.map(prod, values)
    print(results)
