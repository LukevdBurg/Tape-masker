'''looks to find the circle, returning true or false'''
from rplidar import RPLidar
import matplotlib.pyplot as plt
import numpy as np

def find_circle():
    scan = []
    lidar = RPLidar(COM3)
    fig = plt.figure()
    ax = plt.subplot(111, projection='polar')
    iterator = lidar.iter_scans()
    for i in range (0,5):
        scan += next(iterator)
    measurements = np.array(scan)
    angles = measurements[:,1]
    distances = measurements[:,2]
    meandistance = np.mean(distances)
    mediandistance = np.median(distances)
    maxdistance = np.max(distances)
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
    if meandistance < 900 and meandistance > 600 and maxdistance <130:
        return True
    else:
        return False