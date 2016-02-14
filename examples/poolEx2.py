from multiprocessing import Pool
import time

def prod(values):
    time.sleep(1)
    return values[0] * values[1]

if __name__ == '__main__':
    N = 10
    values = [(i + 1, N - i)
              for i in range(0, N)]
    print(values)

    workers = Pool(processes=2)
    results = workers.map_async(prod, values)
    print('Waiting...')
    print(results.get(timeout=10))
