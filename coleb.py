import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as Anim
import json
import time
from os import path

Z = 1# модуль кручения маятника
I = 1# момент инерции маятника

k = 000.89
rho = 1000

r1 = 0.5
r2 = 1
phi_0 = 0.5

dt = 0.001
N = 200


def main():
    starttime = time.time()
    state = State()

    fig = plt.figure()

    ax = plt.axes(xlim=(0, 2), ylim=(0, 100))

    N = 4
    lines = [plt.plot([], [], lw=1, marker='o')[0] for _ in range(N)]  # lines to animate

    patches = lines  # things to animate

    def init():
        # init lines
        lines[0].set_data([], [])

        lines[1].set_data([], [])

        lines[2].set_data([], [])

        lines[3].set_data([], [])

        return patches  # return everything that must be updated

    def animate(i):
        x = np.linspace(r1, r2, N+1)
        state.step()
        # animate lines
        lines[0].set_data([x], [state.phi])
        lines[1].set_data([x], [state.omega])
        lines[2].set_data([x], [state.omega1])
        lines[3].set_data([x], [state.omega2])

        return patches  # return everything that must be updated

    anim = Anim.FuncAnimation(fig, animate, init_func=init, frames=100, interval=20, blit=True)
    anim.save('phi.gif')
    print(time.time()-starttime)



class State():

    def __init__(self):
        self.rad = [self.calc_r(n) for n in range(N + 1)]
        self.phi = [0] * (N+1)
        self.omega = [0] * (N+1)
        self.omega1 = [0] * (N+1)
        self.omega2 = [0] * (N+1)

        self.omega0 = phi_0 * np.sqrt(Z/I)
        self.gamma = np.sqrt(Z/I)
        self.dr = (r2-r1)/N
        self.T = 0

    @staticmethod
    def calc_r(n):
        return r1 + (r2 - r1) * (n / N)

    def step(self):
        for i in range(1, N):
            self.phi[i] = self.phi[i]+self.omega[i]*dt
            self.omega2[i] = (self.omega1[i+1]-self.omega1[i-1])/2/self.dr
            self.omega1[i] = (self.omega[i+1] - self.omega[i - 1]) / 2 / self.dr
            self.omega[i] = self.omega[i] + dt*(k/rho)*(self.omega2[i]+3*self.omega1[i]/self.rad[i])

        self.phi[0] = self.phi[0]+self.omega[0]*dt
        self.T += dt
        self.omega[0] = self.omega0*np.cos(self.gamma * self.T)

main()