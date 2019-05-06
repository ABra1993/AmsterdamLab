import numpy as np
import math
from matplotlib import pylab as plt
import matplotlib.patches as mpatches


class IntraLaminar:

    def __init__(self, dt, iterations, I_ext):

        self.dt = dt
        self.iterations = iterations

        self.t = np.arange(0, self.iterations) * self.dt
        self.r = np.ones((2, self.iterations)) * 0.5

        self.tau_E_2 = 6
        self.tau_I_2 = 15
        self.tau_E_5 = 30
        self.tau_I_5 = 75

        self.sigma_2 = 0.3
        self.sigma_5 = 0.45

        self.J_EE = 1.5
        self.J_IE = 3.5
        self.J_EI = -3.25
        self.J_II = -2.5

        self.I_net = []
        self.I_ext = I_ext

        self.input = []

        self.noise = 0

    def net_input(self, r_E, r_I):

        I_net_E = self.J_EE * r_E + self.J_EI * r_I
        I_net_I = self.J_IE * r_E + self.J_II * r_I

        self.I_net = [I_net_E, I_net_I]

    def transduction_net_input(self):

        I_ext_matrix = np.ones(2) * self.I_ext
        self.input = (self.I_net + I_ext_matrix) / (1.1 - np.exp(-(self.I_net + I_ext_matrix)))

    def noise_input(self, sigma):

        mean = 0
        self.noise = np.random.normal(mean, sigma, 1)

    def run(self, layer):

        tau = np.zeros(2)
        sigma = 0

        if layer == 2:
            tau = [self.tau_E_2, self.tau_I_2]
            sigma = self.sigma_2
        elif layer == 5:
            tau = [self.tau_E_5, self.tau_I_5]
            sigma = self.sigma_5

        tau_sqr = [math.sqrt(x) for x in tau]
        tau_div = [1/x for x in tau]

        for t in range(1, self.iterations):

            self.net_input(self.r[0, t - 1], self.r[1, t - 1])
            self.transduction_net_input()
            self.noise_input(sigma)

            drdt = np.multiply(- self.r[:, t - 1] + self.input + tau_sqr * self.noise, tau_div)
            self.r[:, t] = self.r[:, t - 1] + self.dt * drdt

    def visualize(self, title):

        plt.subplots(1, 2, figsize=(12, 4))

        plt.subplot(1, 2, 1)
        plt.title(title, size=15)
        plt.plot(self.r[0, :], 'red', label='exc')
        plt.ylabel('Firing rate')
        plt.xlabel('time')

        plt.subplot(1, 2, 2)
        plt.plot(self.r[1, :], 'blue', label='exc')
        plt.xlabel('time')

        exc_patch = mpatches.Patch(color='red', label='exc')
        inh_patch = mpatches.Patch(color='blue', label='inh')
        plt.legend(handles=[exc_patch, inh_patch], loc='center left', bbox_to_anchor=(1, 0.5))

        plt.show()


