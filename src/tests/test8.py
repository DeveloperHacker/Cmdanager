from multiprocessing import Manager
from multiprocessing import Pool

manager = Manager()
d = manager.dict()
for i in range(3):
    d[i] = i


def foo(elem: int):
    d[elem] = elem * 5
    return elem * 5


pool = Pool(2)

res = pool.map(foo, range(3, 7))

print(res)
print(d)
