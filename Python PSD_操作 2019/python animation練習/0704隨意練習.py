# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 09:56:11 2019

@author: Harry
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation as anim
from matplotlib.animation import FuncAnimation as fani

#####example1----------------------------------------------------------------
#fig, ax = plt.subplots()
#xdata, ydata = [], []
#ln, = plt.plot([], [], 'ro')
#
#def init():
#    ax.set_xlim(0, 2*np.pi)
#    ax.set_ylim(-1, 1)
#    return ln,
#
#def update(frame):
#    xdata.append(frame)
#    ydata.append(np.sin(frame))
#    ln.set_data(xdata, ydata)
#    return ln,
#
#ani = fani(fig, update, frames=np.linspace(0, 2*np.pi, 128),
#                    init_func=init, blit=True)
#plt.show()
#####example2----------------------------------------------------------------