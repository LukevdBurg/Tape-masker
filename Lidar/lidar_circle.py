'''looks to find the circle, returning true or false'''
from rplidar import RPLidar
import numpy as np

def scanner():
    scan = []
    lidar = RPLidar("COM3")
    iterator = lidar.iter_scans()
    for i in range(0,5):
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

def find_vane():
    scan = scanner()
    vane = []
    for row in scan:
        if row[1] > 75 and row[1] < 105:
            if row[2] < 500:
                vane.append(row)
    vane = np.array(vane)
    minimumindex = np.argmin(vane[:,2])
    firstvane = vane[minimumindex]
    newvanes = []
    for row in vane:
        if row[1] < firstvane[1]-2.5 or row[1] > firstvane[1]+2.5:
            newvanes.append(row)
    newvanes = np.array(newvanes)
    minimumindextwo = np.argmin(newvanes[:,2])
    secondvane = newvanes[minimumindextwo]
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
    return distancetocenter, meantraveldist
