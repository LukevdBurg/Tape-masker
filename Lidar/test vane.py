'''Animates distances and measurment quality'''
from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

PORT_NAME = 'COM3'
DMAX = 500 #was 4000
IMIN = 0
IMAX = 500

scan = []

def update_line(num, iterator, line):
    global scan
    scan += next(iterator)
    offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
    line.set_offsets(offsets)
    intens = np.array([meas[0] for meas in scan])
    line.set_array(intens)
    return line,

def run():
    lidar = RPLidar(PORT_NAME)
    fig = plt.figure()
    ax = plt.subplot(111, projection='polar')
    #print("distance to center:", round(meandistance - measurements[minimumindex, 2], 1), "angle", round(angle, 1))

    line = ax.scatter([0,0], [0,0], s=5, c=[IMIN, IMAX],
                           cmap=plt.cm.Greys_r, lw=0)
    ax.set_rmax(DMAX)
    ax.grid(True)
    ax.set_theta_zero_location('N', offset=270)
    ax.set_theta_direction("clockwise")

    ax.set_thetamin(75)
    ax.set_thetamax(105)

    iterator = lidar.iter_scans()
    ani = animation.FuncAnimation(fig, update_line,
        fargs=(iterator, line), interval=50)
    plt.show()
    vane = []
    for row in scan:
        if row[1] > 75 and row[1] < 105:
            if row[2] < 500:
                vane.append(row)
    vane = np.array(vane)
    minimumindex = np.argmin(vane[:,2])
    firstvane = vane[minimumindex]
    print(firstvane)
    newvanes = []
    for row in vane:
        if row[1] < firstvane[1]-2.5 or row[1] > firstvane[1]+2.5:
            newvanes.append(row)
    newvanes = np.array(newvanes)
    minimumindextwo = np.argmin(newvanes[:,2])
    secondvane = newvanes[minimumindextwo]
    print(secondvane)
    distfromfirstvane = np.sin(np.radians(firstvane[1]-90)) * firstvane[2]
    distfromsecondvane = np.sin(np.radians(secondvane[1]-90)) * secondvane[2]
    traveldist = np.cos(np.radians(firstvane[1]-90)) * firstvane[2]
    traveldistsecond = np.cos(np.radians(secondvane[1] - 90)) * secondvane[2]
    meantraveldist = (abs(traveldist) + abs(traveldistsecond)) / 2
    meandistance = (abs(distfromsecondvane) + abs(distfromfirstvane)) / 2
    if firstvane[1] < secondvane[1]:
        distancetocenter = meandistance - distfromfirstvane
    else:
        distancetocenter = distfromfirstvane - meandistance
    print(distancetocenter, meantraveldist)
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()


if __name__ == '__main__':
    run()
