import numpy as np
import matplotlib.pyplot as plt
from math import pi, cos, sin
from functools import reduce

"""Developed by Agustin M. Picard for a neural networks course"""
"""Solution of the Traveling Salesman Problem using a Kohonen neural network / Self Organizing Map"""


class KohonenNN(object):
    """Square Kohonen neural network with N neurons"""
    def __init__(self, N, r=None, init=None):
        """
        Kohonen neural network initializer. One initialization parameter is required, be it the radius for
        a circle or the init array.
        :param N: Amount of neurons
        :param r: radius for initialization in a circle centered around (0,0) (optional)
        :param init: initialization configuration (optional)
        """
        self.N = N
        if init is None and r is not None:
            self.r = r * np.random.rand()
            self.w = self.r * np.array(list(map(lambda theta: (cos(2 * pi * theta) + 0.5, sin(2 * pi * theta) + 0.5),
                                                np.linspace(0, 2 * pi, N))))
        elif init is not None:
            assert r is None
            self.w = init
        else:
            self.r = np.random.rand()  # I assume r == 1.
            self.w = self.r * np.array(list(map(lambda theta: (cos(2 * pi * theta) + 0.5, sin(2 * pi * theta) + 0.5),
                                                np.linspace(0, 2 * pi, N))))

    def optimize(self, C, d, eta, Nk, sigma):
        """
        Optimizes the network for the Traveling Salesman problem for a set of C city positions, d distance metric,
        eta learning constant, sigma initial parameter for the distance metric and Nk runs
        :param C: array with the city positions
        :param d: distance metric in the neural network space (neighborhood function)
        :param eta: learning coefficient
        :param Nk: amount of times the optimization method is run
        :param sigma: initial distance metric parameter
        :return: optimized neural network array
        """
        for k in range(Nk):
            sigma -= (0.3 * self.N - 0.001 * self.N) / Nk
            for j in np.random.permutation(int(self.N / 2)):
                r_min = np.argmin(np.linalg.norm(self.w - C[j], axis=1))
                for i in range(self.N):
                    self.w[i] += eta * d(i, r_min, sigma) * (C[j] - self.w[i])
        return self.w


def plot_solution(cities, sol):
    """Plots the solution to the Traveling Salesman problem optimized through a Kohonen neural network"""
    plt.figure('Traveling Salesman Problem')
    plt.plot(cities[:, 0], cities[:, 1], 'b*')
    plt.plot(sol[:, 0], sol[:, 1], '-rx')
    plt.title('Traveling Salesman Problem')
    plt.grid()
    plt.show()


def somyx_main():
    # Definition of the problem's parameters
    N_side = 10
    N = N_side**2
    eta = 0.2
    C = np.random.randn(int(N / 2), 2)
    Nk = 100
    sigma = 0.3 * N

    # Definition of the neighborhood function
    dist = lambda r, r_min, s: np.exp(-(np.abs(r - r_min)**2) / (2 * s**2))

    # Definition of the Kohonen network and optimization
    KohNN = KohonenNN(N, r=1.0)
    KohNN.optimize(C, dist, eta, Nk, sigma)
    sol = np.vstack((KohNN.w, KohNN.w[0, :]))

    # Plot the result
    plot_solution(C, sol)

