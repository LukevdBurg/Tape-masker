'''Animates distances and measurment quality'''
from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

PORT_NAME = 'COM3'
DMAX = 500 #was 4000
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
        angle = measurements[minimumindex, 1] - 180
    else:
        angle = measurements[minimumindex, 1] + 180
    xdist = np.sin(angle) * (meandistance-measurements[minimumindex,2])
    zdist = np.cos(angle) * (meandistance-measurements[minimumindex,2])
    #print("distance to center:", round(meandistance - measurements[minimumindex, 2], 1), "angle", round(angle, 1))
    if abs(xdist) > 1 and abs(zdist) > 1:
        print("x distance: ", round(xdist, 2),"z distance: ",round(zdist,2))
    elif abs(xdist) > 1:
        print("x distance: ",round(xdist,2))
    elif abs(zdist) > 1:
        print("z distance: ",round(zdist,2))
    return line,

def run():
    # lidar = RPLidar(PORT_NAME)
    fig = plt.figure()
    ax = plt.subplot(111, projection='polar')
    line = ax.scatter([0, 0], [0, 0], s=5, c=[IMIN, IMAX],
                           cmap=plt.cm.Greys_r, lw=0)
    ax.set_rmax(DMAX)
    ax.grid(True)
    ax.set_theta_zero_location('N', offset=0)
    ax.set_theta_direction("clockwise")
    #ax.set_thetamin(-45)
    #ax.set_thetamax(45)
    iterator = lidar.iter_scans()
    #lidar.set_pwm(1000)
    ani = animation.FuncAnimation(fig, update_line,
        fargs=(iterator, line), interval=50)
    plt.show()
    lidar.stop()
    lidar.disconnect()

if __name__ == '__main__':
    run()
