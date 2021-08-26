#***********************************************************************
# @file
#
# Visualizing Matrices as Part of Matrix Template Library Preps
#
# @note None
#
# @warning  None
#
#  Created: August 25, 2021
#   Author: Nuertey Odzeyem
#**********************************************************************/
#!/usr/bin/env python

import math
import numpy as np
import matplotlib.pyplot as plot
import mpl_toolkits.mplot3d.axes3d as axes3d

#from mayavi import mlab

# =========
# Option 1:
# =========
plot.imshow(np.random.random((50,50)))
plot.colorbar()
plot.show()

# =========
# Option 2:
# =========  
plot.matshow(np.random.random((5,5)));
plot.colorbar()
plot.show()

# ================
# 3D Matrix Plots:
# ================
def cube_marginals(cube, normalize=False):
    c_fcn = np.mean if normalize else np.sum
    xy = c_fcn(cube, axis=0)
    xz = c_fcn(cube, axis=1)
    yz = c_fcn(cube, axis=2)
    return(xy,xz,yz)

def plotcube(cube,x=None,y=None,z=None,normalize=False,plot_front=False):
    """Use contourf to plot cube marginals"""
    (Z,Y,X) = cube.shape
    (xy,xz,yz) = cube_marginals(cube,normalize=normalize)
    # Returns evenly spaced values between start and stop (ndarray), spaced by step.
    if x is None: x = np.arange(0, X, 1)
    if y is None: y = np.arange(0, Y, 1)
    if z is None: z = np.arange(0, Z, 1)

    fig = plot.figure()
    # MatplotlibDeprecationWarning: Calling gca() with keyword arguments
    # was deprecated in Matplotlib 3.4. Starting two minor releases later,
    # gca() will take no keyword arguments. The gca() function should 
    # only be used to get the current axes, or if no axes exist, create 
    # new axes with default keyword arguments. To create a new axes with
    # non-default arguments, use plt.axes() or plt.subplot().

    # ax = fig.gca(projection='3d')
    ax = fig.add_subplot(projection='3d')

    # draw edge marginal surfaces
    offsets = (Z-1,0,X-1) if plot_front else (0, Y-1, 0)
    cset = ax.contourf(x[None,:].repeat(Y,axis=0), y[:,None].repeat(X,axis=1), xy, zdir='z', offset=offsets[0], cmap=plot.cm.coolwarm, alpha=0.75)
    cset = ax.contourf(x[None,:].repeat(Z,axis=0), xz, z[:,None].repeat(X,axis=1), zdir='y', offset=offsets[1], cmap=plot.cm.coolwarm, alpha=0.75)
    cset = ax.contourf(yz, y[None,:].repeat(Z,axis=0), z[:,None].repeat(Y,axis=1), zdir='x', offset=offsets[2], cmap=plot.cm.coolwarm, alpha=0.75)

    # draw wire cube to aid visualization
    ax.plot([0,X-1,X-1,0,0],[0,0,Y-1,Y-1,0],[0,0,0,0,0],'k-')
    ax.plot([0,X-1,X-1,0,0],[0,0,Y-1,Y-1,0],[Z-1,Z-1,Z-1,Z-1,Z-1],'k-')
    ax.plot([0,0],[0,0],[0,Z-1],'k-')
    ax.plot([X-1,X-1],[0,0],[0,Z-1],'k-')
    ax.plot([X-1,X-1],[Y-1,Y-1],[0,Z-1],'k-')
    ax.plot([0,0],[Y-1,Y-1],[0,Z-1],'k-')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plot.show()

(x,y,z) = np.mgrid[0:10,0:10, 0:10]
data = np.exp(-((x-3)**2 + (y-5)**2 + (z-7)**2)**(0.5))

print('data:')
print(data)
print()

print('data.shape:')
print(data.shape)
print()

plotcube(cube=data,x=None,y=None,z=None,normalize=False,plot_front=True)
plotcube(cube=data,x=None,y=None,z=None,normalize=False,plot_front=False)

# =========================
# 3D Matrix Plots Option 2:
# ========================= 
#x, y, z = np.ogrid[-2:2:25j, -2:2:25j, -2:2:25j]
#s = np.power(x, 10) + np.power(y, 10) + np.power(z, 10) - 100

#mlab.figure(bgcolor=(1,1,1))
#mlab.contour3d(s, contours=[2], color=(.5,.5,.5), transparent=True, opacity=.5)

#ax = mlab.axes(nb_labels=5, ranges=(-2,2,-2,2,-2,2))
#ax.axes.property.color = (0,0,0)
#ax.axes.axis_title_text_property.color = (0,0,0)
#ax.axes.axis_label_text_property.color = (0,0,0)
#ax.axes.label_format='%.0f'

#mlab.show()
