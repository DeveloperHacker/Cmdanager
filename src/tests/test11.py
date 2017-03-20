from multiprocessing import Manager

from multiprocessing import Process

import time

manager = Manager()
d = manager.dict()


def handle():
    for i in range(10):
        print(i)
        d[i] = "lel{}".format(i)
        time.sleep(0.8)


process = Process(target=handle)
# process.start()
#
# for i in range(100):
#     print(i)
#     k = i // 10
#     if k in d:
#         print("------>", d[k])
#         del d[k]
#         print(d)
#     time.sleep(0.1)
#
# process.join()

l = manager.list()
l.append(1)
print(l.pop())
print(len(l))
