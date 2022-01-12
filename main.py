import matplotlib.pyplot as plt
import numpy
import numpy as np
from matplotlib import pyplot
import json
import time
from os import path

# Settings
Omega = 0  # угловая скорость внешних стенок
Omega0 = 5  # угловая скорость внутренних стенок
R = 1  # метр
K = 000.89  # Па * с
T = 100000  # кол-во тиков времени
Pi = 3.1415926  # число пи
Rho = 1000  # плотность жидкости
G = 9.82  # константа g
Height = 1  # средняя высота жидкости, м
dt = 0.00001
N = 400  # кол-во симлирующихся кусков
width = 0


def area(n, heights):
    return 2 * Pi * (n * R / N) * heights[n]


def step(heights, speeds):
    new_heights = heights.copy()
    new_speeds = speeds.copy()
    # calculate speeds
    for n in range(N):
        if n <= width:
            new_speeds[n] = Omega0
            continue
        Fplus = (speeds[n + 1] - speeds[n]) * (area(n + 1, heights) + area(n, heights)) * (n + 0.5)
        Fminus = (speeds[n - 1] - speeds[n]) * (area(n - 1, heights) + area(n, heights)) * (n - 0.5)
        new_speeds[n] = speeds[n] + (Fplus + Fminus) / (area(n, heights) * (R / N) * Rho) /(R/N * n) * dt

    volume = 0
    '''
    # calculate heights gradient
    for n in range(N + 1):
        if n <=width:
            new_heights[n] = 0
        else:
            new_heights[n] = (R / N) * (R / N) * speeds[n] * speeds[n] * n / G + new_heights[n - 1]

    # calculate volume
    for n in range(N + 1):
        volume += new_heights[n] * (R / N) * 2 * Pi * (R / N) * n
    delta = Height*(Pi*R*R - Pi*(R*width/N * R*width/N)) - volume

    # add volume to heights
    for n in range(width, N + 1):
        new_heights[n] += delta / (Pi*R*R - Pi*(R*width/N * R*width/N))
    '''
    return heights, new_speeds




def main():
    heights = [Height] * (N + 1)
    speeds = [(R / N * (n * Omega + (N-n) * Omega0)) for n in range(N + 1)]
    speeds[N] = Omega * R
    printedheights, printedspeeds = [], []
    printedruns = []


    for i in range(T):
        heights, speeds = step(heights, speeds)
        if i % (T // 10) == 0:
            printedspeeds.append(speeds)
            printedheights.append(heights)
            printedruns.append(i)
            #pyplot.plot(speeds, 'o')
    #pyplot.show()

    dump = {
        'heights': printedheights,
        'speeds': printedspeeds,
        'runs': printedruns
    }

    plt.figure(1)
    plt.plot(np.arange(0.0, 1.0001, (1/N)), speeds, 'o')
    plt.savefig(path.join('newdata', str(width/N) + '-speeds'+'.svg'), format='svg')
    plt.show()
    plt.figure(2)
    plt.plot(np.arange(0.0, 1.0001, (1/N)), heights, 'o')
    plt.savefig(path.join('newdata', str(width/N) + '-heights' + '.svg'), format='svg')
    plt.show()
    with open(path.join('newdata', str(width/N) + '-data'+'.json'), 'w') as f:
        f.write(json.dumps(dump))
    return speeds, heights


time1 = time.time()
width = 100
main()
print(time.time()-time1)
"""
pyplot.plot(sv, 'r-')
pyplot.plot([(R/N*n*Omega) for n in range(N+1)], 'y-')
pyplot.show()
pyplot.plot(hv, 'r-')
height_zero = Volume/(Pi*R*R)
pyplot.plot([height_zero]*(N+1), 'y-')
pyplot.show()
"""
