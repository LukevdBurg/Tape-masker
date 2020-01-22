
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 13:23:30 2020

@author: David
"""

'''looks to find the circle, returning true or false'''
import numpy as np
from rplidar import RPLidar


class MyRPLidar(RPLidar):
    def __init__(self, port):
        super().__init__(port)
        self.scan = []

    def scanner(self):
        scan = []
        lidar = RPLidar("COM3")

        iterator = lidar.iter_scans()
        for i in range(0, 10):
            scan += next(iterator)
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()
        return scan

    def find_circle(self):
        measurements = np.array(self.scanner())
        distances = measurements[:, 2]
        meandistance = np.mean(distances)
        maxdistance = np.max(distances)

        if meandistance < 900 and meandistance > 600 and maxdistance < 1400:
            return True
        else:
            return False

    def find_middle(self):
        measurements = np.array(self.scanner())
        angles = measurements[:, 1]
        distances = measurements[:, 2]
        meandistance = np.mean(distances)
        minimumindex = np.argmin(measurements[:, 2])
        if (angles[minimumindex] > 180):
            angle = angles[minimumindex] - 180
        else:
            angle = angles[minimumindex] + 180
        xdist = (np.sin(np.radians(angle)) * (meandistance - measurements[minimumindex, 2])) / 1000
        zdist = (np.cos(np.radians(angle)) * (meandistance - measurements[minimumindex, 2])) / 1000
        return round(xdist, 2), round(zdist, 2)

    def findexactvanes(self,lower_angle_L, lower_angle_R, upper_angle_L, upper_angle_R, lower_distance_L, lower_distance_R,
                       upper_distance_L, upper_distance_R):
        mylidar = RPLidar("COM3", baudrate=115200)
        mylidar_scan = []
        totalaverageleftvane = []
        totalaveragerightvane = []
        totalaverageangleleftvane = []
        totalaverageanglerightvane = []

        for y in range(0, 20):

            for i, scan in enumerate(mylidar.iter_scans(scan_type='normal',
                                                        max_buf_meas=60000)):  # scan_type='normal', max_buf_meas=60000
                # print('%d: Got %d measures' % (i, len(scan)))
                #
                mylidar_scan.append(scan)
                if i > 10:
                    break

            for i in range(len(mylidar_scan)):  # aantal rondes
                leftvane = []
                rightvane = []
                # print("Len lidarscan i : ", len(mylidar_scan[i]))
                for j in range(len(mylidar_scan[i])):  # aantal metingen in het rondje
                    mylist = mylidar_scan[i][j]

                    if lower_angle_L < mylist[1] < upper_angle_L and lower_distance_L < mylist[2] < upper_distance_L:
                        leftvane.append(mylist)
                    elif lower_angle_R < mylist[1] < upper_angle_R and lower_distance_R < mylist[2] < upper_distance_R:
                        rightvane.append(mylist)

            print("left", leftvane)
            print("right", rightvane)
            # print("arr_avg: ", arr_avg)
            if leftvane:
                leftvane = np.array(leftvane)
                averageleftvane = np.mean(leftvane[:, 2])
                averageangleleftvane = np.mean(leftvane[:, 1])

                totalaverageleftvane.append(averageleftvane)
                totalaverageangleleftvane.append(averageangleleftvane)
                print("Average numpy left", averageleftvane)

            if rightvane:
                rightvane = np.array(rightvane)
                averagerightvane = np.mean(rightvane[:, 2])
                averageanglerightvane = np.mean(rightvane[:, 1])

                totalaveragerightvane.append(averagerightvane)
                totalaverageanglerightvane.append(averageanglerightvane)
                print("Average numpy right", averagerightvane)

            # mylidar.clean_input()
        grandtotalleft = np.mean(totalaverageleftvane)
        grandtotalright = np.mean(totalaveragerightvane)
        grandtotalleftangle = np.mean(totalaverageangleleftvane)
        grandtotalrightangle = np.mean(totalaverageanglerightvane)
        print("totaal links:", grandtotalleft)
        print("totaal rechts:", grandtotalright)
        print("totaal hoek links:", grandtotalleftangle)
        print("totaal hoek rechts:", grandtotalrightangle)
        mylidar.stop()
        mylidar.stop_motor()
        mylidar.disconnect()
        return grandtotalleft, grandtotalright, grandtotalleftangle, grandtotalrightangle

    def findvanes(self):
        scan = self.scanner()
        vane = []
        for row in scan:
            if row[1] > 80 and row[1] < 100:
                if row[2] < 500:
                    vane.append(row)
        vane = np.array(vane)
        minimumindex = np.argmin(vane[:, 2])
        firstvane = vane[minimumindex]
        print("first vane", firstvane)

        newvanes = []
        for row in vane:
            if row[1] < firstvane[1] - 5 or row[1] > firstvane[1] + 5:
                if row[2] < firstvane[2] + 20:
                    newvanes.append(row)
        newvanes = np.array(newvanes)
        minimumindextwo = np.argmin(newvanes[:, 2])
        secondvane = newvanes[minimumindextwo]
        print("second vane", secondvane)
        if firstvane[1] < secondvane[1]:
            arr_mean_L, arr_mean_R, arr_avg_angle_L, arr_avg_angle_R = self.findexactvanes(firstvane[1] - 3,
                                                                                      secondvane[1] - 3,
                                                                                      firstvane[1] + 3,
                                                                                      secondvane[1] + 3,
                                                                                      firstvane[2] - 10,
                                                                                      secondvane[2] - 10,
                                                                                      firstvane[2] + 20,
                                                                                      secondvane[2] + 20)
        else:
            arr_mean_L, arr_mean_R, arr_avg_angle_L, arr_avg_angle_R = self.findexactvanes(secondvane[1] - 3,
                                                                                      firstvane[1] - 3,
                                                                                      secondvane[1] + 3,
                                                                                      firstvane[1] + 3,
                                                                                      secondvane[2] - 10,
                                                                                      firstvane[2] - 10,
                                                                                      secondvane[2] + 20,
                                                                                      firstvane[2] + 20)
        xdistancefromleftvane = np.sin(np.radians(arr_avg_angle_L - 90)) * arr_mean_L
        xdistancefromrightvane = np.sin(np.radians(arr_avg_angle_R - 90)) * arr_mean_R

        zdistancefromleftvane = np.cos(np.radians(arr_avg_angle_L - 90)) * arr_mean_L
        zdistancefromrightvane = np.cos(np.radians(arr_avg_angle_R - 90)) * arr_mean_R

        meanzdistance = (abs(zdistancefromleftvane) + abs(zdistancefromrightvane)) / 2
        xdistancetocenter = (xdistancefromleftvane + xdistancefromrightvane) / 2
        return xdistancetocenter / 1000, meanzdistance / 1000

    print(findvanes())
'''looks to find the circle, returning true or false'''
