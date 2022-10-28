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

def flattop(_N):
    a0 = 0.21557895
    a1 = 0.41663158
    a2 = 0.277263158
    a3 = 0.083578947
    a4 = 0.006947368
    
    n = np.linspace(0, _N-1, _N)
    w = a0 - a1 * np.cos(2*np.pi*n/_N) + a2 * np.cos(4*np.pi*n/_N) - a3 * np.cos(6*np.pi*n/_N) + a4 * np.cos(8*np.pi*n/_N)
    
    return w

# Global variables
N = 2**8
M = N
f1 = 0.1
A1 = 1
f2 = 0.15
A2 = 0.1
phi1 = 0
phi2 = 0

M_MAX = 2**12

figStep = Figure(dpi=100)
plot1 = figStep.add_subplot(311)
plot2 = figStep.add_subplot(312)
plot3 = figStep.add_subplot(313)



def onNChanged(var_N):
    global N
    N = 2**int(var_N)
    updatePlot(N, M, f1, A1, f2, A2, phi1, phi2)
    return

def onMChanged(var_M):
    global M
    M = 2**int(var_M)
    updatePlot(N, M, f1, A1, f2, A2, phi1, phi2)
    return

def onF1Changed(var_f1):
    global f1
    f1 = float(var_f1)
    updatePlot(N, M, f1, A1, f2, A2, phi1, phi2)
    return

def onA1Changed(var_A1):
    global A1
    A1 = float(var_A1)
    updatePlot(N, M, f1, A1, f2, A2, phi1, phi2)
    return

def onF2Changed(var_f2):
    global f2
    f2 = float(var_f2)
    updatePlot(N, M, f1, A1, f2, A2, phi1, phi2)
    return

def onA2Changed(var_A2):
    global A2
    A2 = float(var_A2)
    updatePlot(N, M, f1, A1, f2, A2, phi1, phi2)
    return

def onPhi1Changed(var_phi1):
    global phi1
    phi1 = float(var_phi1)
    updatePlot(N, M, f1, A1, f2, A2, phi1, phi2)
    return

def onPhi2Changed(var_phi2):
    global phi2
    phi2 = float(var_phi2)
    updatePlot(N, M, f1, A1, f2, A2, phi1, phi2)
    return

def onWindowChanged():
    updatePlot(N, M, f1, A1, f2, A2, phi1, phi2)
    return

def updatePlot(_N, _M, _f1, _A1, _f2, _A2, _phi1, _phi2):
    t = np.linspace(0, _N-1, num=N)
    x = _A1 * np.sin(2 * np.pi * _f1 * t + _phi1) + _A2 * np.sin(2 * np.pi * _f2 * t + _phi2)
    t_cont = np.linspace(0, _N-1, M_MAX)
    x_cont = _A1 * np.sin(2 * np.pi * _f1 * t_cont + _phi1) + + _A2 * np.sin(2 * np.pi * _f2 * t_cont + _phi2)
    
    if (window_string.get() == "hann"):
        x = np.multiply(x, np.hanning(N))
        x_cont = np.multiply(x_cont, np.hanning(M_MAX))
    elif (window_string.get() == "ft"):
        x = np.multiply(x, flattop(N))
        x_cont = np.multiply(x_cont, flattop(M_MAX))
        
    
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
    plot2.set(xlabel=r"$\nu$", ylabel=r"$|X(\nu)|$", xlim=[-0.02, 1.02], ylim=[-0.02, max(_A1, _A2)+0.02])
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
slidersSamplesFrame = LabelFrame(slidersframe, text="Échantillons", borderwidth=2, relief=GROOVE)
slidersSamplesFrame.pack(side=TOP, padx=10, fill="y")
slidersSin1Frame = LabelFrame(slidersframe, text="Sinus 1", borderwidth=2, relief=GROOVE)
slidersSin1Frame.pack(side=TOP, padx=10, fill="y")
slidersSin2Frame = LabelFrame(slidersframe, text="Sinus 2", borderwidth=2, relief=GROOVE)
slidersSin2Frame.pack(side=TOP, padx=10, fill="y")
windowsFrame = LabelFrame(slidersframe, text="Fenêtres d'apodisation", borderwidth=2, relief=GROOVE)
windowsFrame.pack(side=TOP, padx=10, fill="y")
plotFrame = LabelFrame(window, text="Plot", borderwidth=2, relief=GROOVE)
plotFrame.pack(side=RIGHT, padx=10, expand='yes', fill="both")

# Sliders
Label(slidersSamplesFrame, text="2^N time samples").pack(anchor="c", side=TOP)
NSlider = Scale(slidersSamplesFrame, orient=HORIZONTAL, command=onNChanged, from_=4, to_=10, resolution=1)
NSlider.set(8)
NSlider.pack(anchor="e", side=TOP)

Label(slidersSamplesFrame, text="2^M frequency samples" ).pack(anchor="c", side=TOP)
MSlider = Scale(slidersSamplesFrame, orient=HORIZONTAL, command=onMChanged, from_=4, to_=np.log2(M_MAX), resolution=1)
MSlider.set(8)
MSlider.pack(anchor="e", side=TOP)

Label(slidersSin1Frame, text="f1").pack(anchor="c", side=TOP)
f1Slider = Scale(slidersSin1Frame, orient=HORIZONTAL, command=onF1Changed, from_=0, to_=0.5, resolution=0.001)
f1Slider.set(f1)
f1Slider.pack(anchor="e", side=TOP)

Label(slidersSin1Frame, text="A1").pack(anchor="c", side=TOP)
A1Slider = Scale(slidersSin1Frame, orient=HORIZONTAL, command=onA1Changed, from_=0, to_=2, resolution=0.1)
A1Slider.set(A1)
A1Slider.pack(anchor="e", side=TOP)

Label(slidersSin1Frame, text="Phi1").pack(anchor="c", side=TOP)
phi1Slider = Scale(slidersSin1Frame, orient=HORIZONTAL, command=onPhi1Changed, from_=0, to_=2*np.pi, resolution=0.01)
phi1Slider.set(phi1)
phi1Slider.pack(anchor="e", side=TOP)

Label(slidersSin2Frame, text="f2").pack(anchor="c", side=TOP)
f2Slider = Scale(slidersSin2Frame, orient=HORIZONTAL, command=onF2Changed, from_=0, to_=0.5, resolution=0.001)
f2Slider.set(f2)
f2Slider.pack(anchor="e", side=TOP)

Label(slidersSin2Frame, text="A2").pack(anchor="c", side=TOP)
A2Slider = Scale(slidersSin2Frame, orient=HORIZONTAL, command=onA2Changed, from_=0, to_=2, resolution=0.1)
A2Slider.set(A2)
A2Slider.pack(anchor="e", side=TOP)

Label(slidersSin2Frame, text="Phi2").pack(anchor="c", side=TOP)
phi2Slider = Scale(slidersSin2Frame, orient=HORIZONTAL, command=onPhi2Changed, from_=0, to_=2*np.pi, resolution=0.01)
phi2Slider.set(phi2)
phi2Slider.pack(anchor="e", side=TOP)

window_string = StringVar()
window_string.set("rect")

radioRect = Radiobutton(windowsFrame, text="Rect", variable=window_string, value="rect", command=onWindowChanged)
radioRect.pack(anchor=W)

radioHann = Radiobutton(windowsFrame, text="Hann", variable=window_string, value="hann", command=onWindowChanged)
radioHann.pack(anchor=W)

radioFT = Radiobutton(windowsFrame, text="Flat top", variable=window_string, value="ft", command=onWindowChanged)
radioFT.pack(anchor=W)


# Canvas
canvasStep = FigureCanvasTkAgg(figStep, master=plotFrame)
canvasStep.get_tk_widget().pack(fill="both", expand="true") 

# Run window 
window.mainloop()

