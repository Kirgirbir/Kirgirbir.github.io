import asyncio
import math
import random
import matplotlib.pyplot as plt
import traceback


###async def graph (a, b):
###    c = 0
###    while c <= 10:
###        await print(randint(a, b))
###        a = a+1
###        asyncio.sleep(2000)

numbers = []

def makestack (amount, initial, st, ed, list):
    c = 0
    while c <= amount:
        list.append(initial)
        initial = math.ceil(initial*(1+0.01*(random.randint(st, ed))))
        c = c+1

makestack(1000, 100, -0.5, 1, numbers)

plt.plot(numbers)
plt.ylim(0,300)
plt.title('Курс Валют')
plt.ylabel('Цена')
plt.savefig('my_plot.png')
