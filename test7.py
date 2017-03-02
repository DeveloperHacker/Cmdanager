from multiprocessing import Manager, Pool


def foo():
    return str(i)


manager = Manager()
a = manager.dict()
for i in range(3):
    a[i] = foo

pool = Pool()

for i in range(3, 6):
    a[i] = foo

print("\n".join((ai() for ai in a.values())))
