# Animates distances and measurment quality
import numpy as np
from rplidar import RPLidar

PORT_NAME = 'COM3'
DMAX = 500  # was 4000
IMIN = 0
IMAX = 500
som = 0


def run(lower_angle_L, lower_angle_R, upper_angle_L, upper_angle_R, lower_distance_L, lower_distance_R,
        upper_distance_L, upper_distance_R):
    mylidar = RPLidar(PORT_NAME, baudrate=115200)
    total = 0
    arr_avg_L = []
    arr_avg_R = []
    avg_angle_L = []
    avg_angle_R = []
    mylidar_scan = []
    angle_L = 0
    angle_R = 0
    dist_L = 0
    dist_R = 0

    for y in range(0, 15):

        for i, scan in enumerate(mylidar.iter_scans(scan_type='normal', max_buf_meas=60000)):
            # print('%d: Got %d measures' % (i, len(scan)))
            #
            mylidar_scan.append(scan)
            if i > 10:
                break

        for i in range(len(mylidar_scan)):  # aantal rondes

            # print("Len lidarscan i : ", len(mylidar_scan[i]))
            for j in range(len(mylidar_scan[i])):  # aantal metingen in het rondje
                mylist = mylidar_scan[i][j]
                # print(mylist[2])

                if lower_angle_L < mylist[1] < upper_angle_L and lower_distance_L < mylist[2] < upper_distance_L:
                    dist_L = mylist[2]
                    angle_L = mylist[1]
                    total = 1
                elif lower_angle_R < mylist[1] < upper_angle_R and lower_distance_R < mylist[2] < upper_distance_R:
                    dist_R = mylist[2]
                    angle_R = mylist[1]
                    total = 1

                if total == 1:
                    # aver = som / total
                    avg_angle_L.append(angle_L)
                    avg_angle_R.append(angle_R)
                    arr_avg_L.append(dist_L)
                    arr_avg_R.append(dist_R)
                    total = 0

            # print("arr_avg: ", arr_avg)
            arr_mean_L = np.mean(arr_avg_L)
            arr_mean_R = np.mean(arr_avg_R)
            arr_avg_angle_L = np.mean(avg_angle_L)
            arr_avg_angle_R = np.mean(avg_angle_R)
            print("Average Left: ", arr_mean_L)
            print("Average Right: ", arr_mean_R)

        mylidar.clean_input()

    mylidar.stop()
    mylidar.stop_motor()
    mylidar.disconnect()
    return arr_mean_L, arr_mean_R, arr_avg_angle_L, arr_avg_angle_R


if __name__ == '__main__':
    run()
