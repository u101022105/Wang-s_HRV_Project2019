# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 15:19:38 2019

@author: Harry
"""

import numpy as np
import matplotlib.pyplot as plt

def read_PeriodSeq(file_name):
    hdl = np.genfromtxt(file_name)
    return hdl
