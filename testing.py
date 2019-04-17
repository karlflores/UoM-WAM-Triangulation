import math
import argparse
import matplotlib.pyplot as plt
import numpy as np 
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D
# subject codes [1..5]

def wam_change(before,after):
    results = []  
    for skip in range(1,5):
        for i in range(101):
            for num_subs in range(1,14):
                if math.fabs(after - (before*num_subs+i*skip)/(num_subs+skip)) < 1e-2:
                    # print(skip, i,num_subs)

                    # skip --> number of subjects whose wam have change 
                    # i -> calculated grade 
                    # num subs - number of subjects a student has taken so far 
                    results.append((skip,num_subs,i))
    return results

# PROCESS THE ARGUMENTS
parser = argparse.ArgumentParser(description='Musician Multhreaded Testing')
parser.add_argument('-b', '--before',
                        help='Dataset name',
                        choices=range(0,101),
                        required=True,
                        type=int)

parser.add_argument('-a', '--after',
                        help='Dataset name',
                        choices=range(0,101),
                        required=True,
                        type=int)
args = parser.parse_args()

a = wam_change(args.before,args.after)
x,y,z = zip(*a)
grid_x, grid_y = np.mgrid[min(x):max(x):100j,min(y):max(y):100j]
grid_z = griddata((x,y),z,(grid_x,grid_y),method='cubic')

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_surface(grid_x,grid_y,grid_z,cmap=plt.cm.Spectral)
ax.set_title("BEFORE: {} | AFTER: {}".format(args.before,args.after))
ax.set_xlabel("NUM SUBS CHANGED / WEIGHTING")
ax.set_ylabel("NUM SUBS COMPLETED")
ax.set_zlabel("SCORE")
plt.show()
