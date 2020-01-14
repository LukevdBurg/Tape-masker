'''Animates distances and measurment quality'''
from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

PORT_NAME = 'COM3'
DMAX = 1000 #was 4000
IMIN = 0
IMAX = 500

def update_line(num, iterator, line):
    scan = next(iterator)
    offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
    line.set_offsets(offsets)
    intens = np.array([meas[0] for meas in scan])
    line.set_array(intens)
    measurements = np.array(scan)
    meandistance = np.mean(measurements[:,2])
    minimumindex = np.argmin(measurements[:,2])
    if (measurements[minimumindex, 1] > 180):
        minangle = measurements[minimumindex, 1] - 180
    else:
        minangle = measurements[minimumindex, 1] + 180

    print("distance to center:",round(meandistance-measurements[minimumindex,2],1),"angle",round(minangle,1))
    return line,

def run():
    lidar = RPLidar(PORT_NAME)
    fig = plt.figure()
    ax = plt.subplot(111, projection='polar')
    line = ax.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX],
                           cmap=plt.cm.Greys_r, lw=0)
    line2 = ax.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX],
                           cmap=plt.cm.Greys_r, lw=0)
    ax.set_rmax(DMAX)
    ax.grid(True)
    ax.set_theta_zero_location('N', offset=0)
    ax.set_theta_direction("clockwise")

    iterator = lidar.iter_scans()
    ani = animation.FuncAnimation(fig, update_line,
        fargs=(iterator, line), interval=50)
    plt.show()
    lidar.stop()
    lidar.disconnect()

if __name__ == '__main__':
    run()
