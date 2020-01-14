'''looks to find the circle, returning true or false'''
from rplidar import RPLidar
import numpy as np

def scanner():
    scan = []
    lidar = RPLidar("COM3")
    iterator = lidar.iter_scans()
    for i in range (0,5):
        scan += next(iterator)
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
    return scan

def find_circle():
    measurements = np.array(scanner())
    distances = measurements[:,2]
    meandistance = np.mean(distances)
    maxdistance = np.max(distances)

    print(meandistance,maxdistance)
    if meandistance < 900 and meandistance > 600 and maxdistance <1400:
        return True
    else:
        return False

def find_middle():
    measurements = np.array(scanner())
    angles = measurements[:,1]
    distances = measurements[:,2]
    meandistance = np.mean(distances)
    minimumindex = np.argmin(measurements[:, 2])
    if (angles[minimumindex] > 180):
        angle = angles[minimumindex] - 180
    else:
        angle = angles[minimumindex] + 180
    xdist = np.sin(np.radians(angle)) * (meandistance-measurements[minimumindex,2])
    zdist = np.cos(np.radians(angle)) * (meandistance-measurements[minimumindex,2])
    return round(xdist, 2), round(zdist,2)

def run():
    scan = scanner()
    vane = []
    for row in scan:
        if row[1] < 20 or row[1] > 340:
            if row[2] < 500:
                vane.append(row)
    vane = np.array(vane)
    minimumindex = np.argmin(vane[:,2])
    firstvane = vane[minimumindex]
    print(firstvane)
    newvane = []
    for row in vane:
        if row[1] < firstvane[1]-3 or row[1] > firstvane[1]+3:
            newvane.append(row)
    newvane = np.array(newvane)
    minimumindextwo = np.argmin(newvane[:,2])
    print(newvane[minimumindextwo])