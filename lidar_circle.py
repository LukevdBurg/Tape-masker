'''looks to find the circle, returning true or false'''
from rplidar import RPLidar
import numpy as np

def find_circle():
    scan = []
    lidar = RPLidar("COM3")
    iterator = lidar.iter_scans()
    for i in range (0,5):
        scan += next(iterator)
    measurements = np.array(scan)
    angles = measurements[:,1]
    distances = measurements[:,2]
    meandistance = np.mean(distances)
    maxdistance = np.max(distances)
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
    print(meandistance,maxdistance)
    if meandistance < 900 and meandistance > 600 and maxdistance <1400:
        return True
    else:
        return False

def find_middle():
    scan = []
    lidar = RPLidar("COM3")
    iterator = lidar.iter_scans()
    for i in range (0,5):
        scan += next(iterator)
    measurements = np.array(scan)
    angles = measurements[:,1]

    distances = measurements[:,2]
    meandistance = np.mean(distances)
    minimumindex = np.argmin(measurements[:, 2])
    if (angles[minimumindex] > 180):
        angle = angles[minimumindex] - 180
    else:
        angle = angles[minimumindex] + 180
    xdist = np.sin(angle) * (meandistance-measurements[minimumindex,2])
    zdist = np.cos(angle) * (meandistance-measurements[minimumindex,2])
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
    return round(xdist, 2), round(zdist,2)