# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 09:27:21 2022

@author: Pierre-Alexandre
"""

import numpy as np
import matplotlib.pyplot as plt
import imageio
import os

Fe = 10**3
n = 2**12
t = np.arange(0, (n-1)/Fe, 1/Fe)
f = np.arange(0, Fe, Fe/(n-1))
stringName = "fft"
images = []

for i in range(0, Fe):
    x = np.sin(2 * np.pi * i * t)
    X = np.fft.fft(x) * 2 / n
    plt.figure(figsize=(10, 8))
    plt.subplot(5, 1, 1)
    plt.plot(t, x, 'b')
    plt.plot(t, x, 'bo')
    plt.subplot(5, 1, 2)
    plt.ylim([0, 1.2])
    plt.plot(f, np.abs(X), "b")
    plt.plot(f, np.abs(X), "bo")
    plt.subplot(5, 1, 3)
    plt.ylim([-3.5, 3.5])
    plt.plot(f, np.angle(X), "b")
    plt.plot(f, np.angle(X), "bo")
    plt.subplot(5, 1, 4)
    plt.ylim([-1.2, 1.2])
    plt.plot(f, np.real(X), "b")
    plt.plot(f, np.real(X), "bo")
    plt.subplot(5, 1, 5)
    plt.ylim([-1.2, 1.2])
    plt.plot(f, np.imag(X), "b")
    plt.plot(f, np.imag(X), "bo")
    
    
    plt.savefig(stringName+"{}.png".format(i))
    plt.close()
    images.append(imageio.imread(stringName+"{}.png".format(i)))
    os.remove(stringName+"{}.png".format(i))
imageio.mimsave('fft.gif', images)
