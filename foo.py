import math
import random
import time

import numpy as np
avg = np.zeros(100)
for i in range(100):
    start = time.time()
    rand_list = [math.log(random.randint(0, 1000000)) for _ in range(1000)]
    rand_sum = sum(rand_list)
    python = time.time()-start
    print("Python", python)
    start = time.time()
    rand_arr = np.array([random.randint(0, 1000000) for _ in range(1000)])
    rand_arr = np.log(rand_arr).sum()
    numpy = time.time()-start
    print("Numpy", numpy)
    avg[i] = numpy-python
print(avg.mean())
