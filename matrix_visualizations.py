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
    if x == None: x = np.arange(X)
    if y == None: y = np.arange(Y)
    if z == None: z = np.arange(Z)

    fig = plot.figure()
    ax = fig.gca(projection='3d')

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
#edge_yz = np.sum(data,axis=0)
#edge_xz = np.sum(data,axis=1)
#edge_xy = np.sum(data,axis=2)

print('data.shape:')
print(data.shape)
print()

print('data:')
print(data)
print()

plotcube(cube=data,x=x,y=y,z=z,normalize=False,plot_front=True)
plotcube(cube=data,x=x,y=y,z=z,normalize=False,plot_front=False)
