#!/usr/bin/env python
# Kalman filter example demo in Python

# A Python implementation of the example given in pages 11-15 of "An
# Introduction to the Kalman Filter" by Greg Welch and Gary Bishop,
# University of North Carolina at Chapel Hill, Department of Computer
# Science, TR 95-041,
# http://www.cs.unc.edu/~welch/kalman/kalmanIntro.html

# by Andrew D. Straw

import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

plt.rcParams['figure.figsize'] = (10, 8)

# intial parameters
n_iter = 50
sz = (n_iter,) # size of array
x = -0.37727 # truth value (typo in example at top of p. 13 calls this z)
z = np.random.normal(x,0.1,size=sz) # observations (normal about x, sigma=0.1)

Q = 1e-5               # process variance

# allocate space for arrays
xhat=np.zeros(sz)      # a posteriori estimate of x
P=np.zeros(sz)         # a posteriori error estimate
xhatminus=np.zeros(sz) # a priori estimate of x
Pminus=np.zeros(sz)    # a priori error estimate
K=np.zeros(sz)         # gain or blending factor

R = 0.1**2 # estimate of measurement variance, change to see effect

hist_data = [z]
group_labels = ['Random Normal Observations (z)'] # name of the dataset
colors = ['rgb(0, 200, 200)']

figure_1 = ff.create_distplot(hist_data, 
                              group_labels,
                              curve_type='normal', # override default 'kde'
                              colors=colors
                             )
figure_1.update_layout(title_text='<b>Distplot with Numpy Normal Distribution</b>')
figure_1.show()

print('sz:')
print(sz)
print()

print('z:')
print(z)
print()

#print('xhat:')
#print(xhat)
#print()

# intial guesses
xhat[0] = 0.0
P[0] = 1.0

for k in range(1,n_iter):
    # time update
    xhatminus[k] = xhat[k-1]
    Pminus[k] = P[k-1]+Q

    # measurement update
    K[k] = Pminus[k]/( Pminus[k]+R )
    xhat[k] = xhatminus[k]+K[k]*(z[k]-xhatminus[k])
    P[k] = (1-K[k])*Pminus[k]

plt.figure()
plt.plot(z, 'k+', label='noisy measurements (z)')
plt.plot(xhat, 'b-', label='a posteriori estimate (xhat)')
plt.axhline(x, color='g', label='truth value (x)')
plt.legend()
plt.title('Estimate vs. iteration step', fontweight='bold')
plt.xlabel('Iteration')
plt.ylabel('Voltage')

plt.figure()
valid_iter = range(1, n_iter) # P not valid at step 0
plt.plot(valid_iter, P[valid_iter], label='a posteriori error estimate (Pminus)')
plt.title('Estimated $\it{\mathbf{a \ posteriori}}$ error vs. iteration step', fontweight='bold')
plt.xlabel('Iteration')
plt.ylabel('$(Voltage)^2$') # LaTeX strings
plt.setp(plt.gca(),'ylim', [0, .01])
plt.show()
