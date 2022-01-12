import json
import numpy as np
import matplotlib.pyplot as plt
with open('data.json') as f:
    data = json.load(f)

from mpl_toolkits.mplot3d import Axes3D
'''
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

number = data['runs'].copy()

j=0
for i in range(len(number)):
    number[i] = j
    j %= (N + 1)
    j+=1

number = np.array(number)


ax.scatter(number, data['runs'], data['speeds'])
'''
N = 200
for v in data['speeds']:
    v = np.array(v)
    plt.plot(v)
plt.show()