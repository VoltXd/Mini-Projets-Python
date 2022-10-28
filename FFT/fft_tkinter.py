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

figStep = Figure(figsize=(5,5), dpi=100)
plot1 = figStep.add_subplot(211)
plot2 = figStep.add_subplot(212)



def onNChanged(var_N):
    global N
    N = 2**int(var_N)
    M = N
    MSlider.set(var_N)
    updatePlot(N, M, f, A)
    return

def onMChanged(var_M):
    global M
    M = 2**int(var_M)
    updatePlot(N, M, f, A)
    return

def onFChanged(var_f):
    global f
    f = float(var_f)
    updatePlot(N, M, f, A)
    return

def onAChanged(var_A):
    global A
    A = float(var_A)
    updatePlot(N, M, f, A)
    return

def updatePlot(_N, _M, _f, _A):
    t = np.linspace(0, _N-1, num=N)
    x = _A * np.sin(2 * np.pi * _f * t)
    
    X = np.fft.fft(x, _M) * 2 / _N
    f_red = np.linspace(0, float(_M-1) / _M, _M)
    
    plot1.cla()
    plot1.grid()
    plot1.plot(t, x)
    
    plot2.cla()
    plot2.grid()
    plot2.plot(f_red, np.abs(X))
    
    
    canvasStep.draw()
    return


window = Tk()

# Settings
window.title("Simulation systeme lineaire invariant")

width = 1000
height = 500
window.geometry(str(width) + "x" + str(height))

# Frames 
slidersframe = LabelFrame(window, text="Paramètres", borderwidth=2, relief=GROOVE)
slidersframe.pack(side=LEFT, padx=10, fill="y")
plotFrame = LabelFrame(window, text="Plot", borderwidth=2, relief=GROOVE)
plotFrame.pack(side=RIGHT, padx=10, expand='yes', fill="both")

# Sliders
Label(slidersframe, text="N (2^N)").pack(anchor="c", side=TOP)
NSlider = Scale(slidersframe, orient=HORIZONTAL, command=onNChanged, from_=4, to_=10, resolution=1)
NSlider.set(8)
NSlider.pack(anchor="e", side=TOP)

Label(slidersframe, text="M (2^M)").pack(anchor="c", side=TOP)
MSlider = Scale(slidersframe, orient=HORIZONTAL, command=onMChanged, from_=4, to_=12, resolution=1)
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

# Canvas
canvasStep = FigureCanvasTkAgg(figStep, master=plotFrame)
canvasStep.get_tk_widget().pack(fill="both", expand="true") 

# Run window 
window.mainloop()

