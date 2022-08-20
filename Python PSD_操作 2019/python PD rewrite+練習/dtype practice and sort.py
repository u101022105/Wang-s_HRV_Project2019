# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 16:07:04 2019

@author: Harry
"""

import numpy as np
a = np.array([1,2,3,4,5,6,7,8,9,10])
b = np.array(2*np.arange(10, 0, -1))
dtype1 = [('x', float), ('y', float)]
#c = np.array(np.vstack((a,b)).T, dtype = dtype1)
#c_intermediate = [(i[0],i[1]) for i in np.array([a,b]).T]
#c = np.array(c_intermediate, dtype = dtype1)

c = np.array( [(i[0],i[1]) for i in np.array([a,b]).T] , dtype = dtype1)
#print(c_intermediate)
print(c)
d = np.sort(c, order = 'y')
print(d)