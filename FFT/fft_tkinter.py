# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 08:28:54 2022

@author: Pierre-Alexandre
"""

from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Global variables
N = 2**8
M = N
f = 0.1
A = 1
phi = 0

M_MAX = 2**12

figStep = Figure(dpi=100)
plot1 = figStep.add_subplot(311)
plot2 = figStep.add_subplot(312)
plot3 = figStep.add_subplot(313)



def onNChanged(var_N):
    global N
    N = 2**int(var_N)
    updatePlot(N, M, f, A, phi)
    return

def onMChanged(var_M):
    global M
    M = 2**int(var_M)
    updatePlot(N, M, f, A, phi)
    return

def onFChanged(var_f):
    global f
    f = float(var_f)
    updatePlot(N, M, f, A, phi)
    return

def onAChanged(var_A):
    global A
    A = float(var_A)
    updatePlot(N, M, f, A, phi)
    return

def onPhiChanged(var_phi):
    global phi
    phi = float(var_phi)
    updatePlot(N, M, f, A, phi)
    return

def updatePlot(_N, _M, _f, _A, _phi):
    t = np.linspace(0, _N-1, num=N)
    x = _A * np.sin(2 * np.pi * _f * t + _phi)
    t_cont = np.linspace(0, _N-1, M_MAX)
    x_cont = _A * np.sin(2 * np.pi * _f * t_cont + _phi)
    
    X = np.fft.fft(x, _M) * 2 / _N
    f_red = np.linspace(0, float(_M-1) / _M, _M)
    
    X_MAX = np.fft.fft(x, M_MAX) * 2 / _N
    f_red_MAX = np.linspace(0, float(M_MAX-1) / M_MAX, M_MAX)
    
    plot1.cla()
    plot1.grid()
    plot1.set(xlabel=f"$n$", ylabel=r"$x(t)$")
    plot1.plot(t_cont, x_cont, '-b')
    plot1.plot(t, x, '+r')
    
    plot2.cla()
    plot2.grid()
    plot2.set(xlabel=r"$\nu$", ylabel=r"$|X(\nu)|$", xlim=[-0.02, 1.02], ylim=[-A-0.02, A+0.02])
    plot2.plot(f_red_MAX, np.abs(X_MAX), '-b')
    plot2.plot(f_red, np.abs(X), '+r')
    
    plot3.cla()
    plot3.grid()
    plot3.set(xlabel=r"$\nu$", ylabel=r"$\mathrm{arg}(X(\nu))$", xlim=[-0.02, 1.02], ylim=[-np.pi-0.02, np.pi+0.02])
    plot3.plot(f_red_MAX, np.angle(X_MAX), '-b')
    plot3.plot(f_red, np.angle(X), '+r')
    
    canvasStep.draw()
    return


window = Tk()

# Settings
window.title("Simulation Transformée de Fourier")

width = 1280
height = 720
window.geometry(str(width) + "x" + str(height))

# Frames 
slidersframe = LabelFrame(window, text="Paramètres", borderwidth=2, relief=GROOVE)
slidersframe.pack(side=LEFT, padx=10, fill="y")
plotFrame = LabelFrame(window, text="Plot", borderwidth=2, relief=GROOVE)
plotFrame.pack(side=RIGHT, padx=10, expand='yes', fill="both")

# Sliders
Label(slidersframe, text="2^N time samples").pack(anchor="c", side=TOP)
NSlider = Scale(slidersframe, orient=HORIZONTAL, command=onNChanged, from_=4, to_=10, resolution=1)
NSlider.set(8)
NSlider.pack(anchor="e", side=TOP)

Label(slidersframe, text="2^M frequency samples" ).pack(anchor="c", side=TOP)
MSlider = Scale(slidersframe, orient=HORIZONTAL, command=onMChanged, from_=4, to_=np.log2(M_MAX), resolution=1)
MSlider.set(8)
MSlider.pack(anchor="e", side=TOP)

Label(slidersframe, text="f").pack(anchor="c", side=TOP)
fSlider = Scale(slidersframe, orient=HORIZONTAL, command=onFChanged, from_=0, to_=0.5, resolution=0.001)
fSlider.set(f)
fSlider.pack(anchor="e", side=TOP)

Label(slidersframe, text="A").pack(anchor="c", side=TOP)
ASlider = Scale(slidersframe, orient=HORIZONTAL, command=onAChanged, from_=0, to_=2, resolution=0.1)
ASlider.set(A)
ASlider.pack(anchor="e", side=TOP)

Label(slidersframe, text="Phi").pack(anchor="c", side=TOP)
ASlider = Scale(slidersframe, orient=HORIZONTAL, command=onPhiChanged, from_=0, to_=2*np.pi, resolution=0.01)
ASlider.set(phi)
ASlider.pack(anchor="e", side=TOP)

# Canvas
canvasStep = FigureCanvasTkAgg(figStep, master=plotFrame)
canvasStep.get_tk_widget().pack(fill="both", expand="true") 

# Run window 
window.mainloop()

