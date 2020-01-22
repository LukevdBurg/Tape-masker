import numpy as np
from rplidar import RPLidar


class MyRPLidar(RPLidar):
    def __init__(self, port):
        super().__init__(port)

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
        mean_distance = np.mean(distances)
        max_distance = np.max(distances)

        if mean_distance < 900 and mean_distance > 600 and max_distance < 1400:
            return True
        else:
            return False

    def find_middle(self):
        measurements = np.array(self.scanner())
        angles = measurements[:, 1]
        distances = measurements[:, 2]
        mean_distance = np.mean(distances)
        minimum_index = np.argmin(measurements[:, 2])
        if (angles[minimum_index] > 180):
            angle = angles[minimum_index] - 180
        else:
            angle = angles[minimum_index] + 180
        xdist = (np.sin(np.radians(angle)) * (mean_distance - measurements[minimum_index, 2])) / 1000
        zdist = (np.cos(np.radians(angle)) * (mean_distance - measurements[minimum_index, 2])) / 1000
        return round(xdist, 2), round(zdist, 2)

    def find_exact_vanes(self, lower_angle_L, lower_angle_R, upper_angle_L, upper_angle_R, lower_distance_L, lower_distance_R,
                         upper_distance_L, upper_distance_R):
        mylidar = RPLidar("COM3", baudrate=115200)
        mylidar_scan = []
        total_average_left_vane = []
        total_average_right_vane = []
        total_average_angle_left_vane = []
        total_average_angle_right_vane = []

        for y in range(0, 20):

            for i, scan in enumerate(mylidar.iter_scans(scan_type='normal',
                                                        max_buf_meas=60000)):  # scan_type='normal', max_buf_meas=60000

                mylidar_scan.append(scan)
                if i > 10:
                    break

            for i in range(len(mylidar_scan)):  # aantal rondes
                left_vane = []
                right_vane = []

                for j in range(len(mylidar_scan[i])):  # aantal metingen in het rondje
                    my_list = mylidar_scan[i][j]

                    if lower_angle_L < my_list[1] < upper_angle_L and lower_distance_L < my_list[2] < upper_distance_L:
                        left_vane.append(my_list)
                    elif lower_angle_R < my_list[1] < upper_angle_R and lower_distance_R < my_list[2] < upper_distance_R:
                        right_vane.append(my_list)

            print("left", left_vane)
            print("right", right_vane)
            # print("arr_avg: ", arr_avg)
            if left_vane:
                left_vane = np.array(left_vane)
                average_left_vane = np.mean(left_vane[:, 2])
                average_angle_left_vane = np.mean(left_vane[:, 1])

                total_average_left_vane.append(average_left_vane)
                total_average_angle_left_vane.append(average_angle_left_vane)
                print("Average numpy left", average_left_vane)

            if right_vane:
                right_vane = np.array(right_vane)
                average_right_vane = np.mean(right_vane[:, 2])
                average_angle_right_vane = np.mean(right_vane[:, 1])

                total_average_right_vane.append(average_right_vane)
                total_average_angle_right_vane.append(average_angle_right_vane)
                print("Average numpy right", average_right_vane)

            mylidar.clean_input()
        grand_total_left = np.mean(total_average_left_vane)
        grand_total_right = np.mean(total_average_right_vane)
        grand_total_left_angle = np.mean(total_average_angle_left_vane)
        grand_total_right_angle = np.mean(total_average_angle_right_vane)
        print("totaal links:", grand_total_left)
        print("totaal rechts:", grand_total_right)
        print("totaal hoek links:", grand_total_left_angle)
        print("totaal hoek rechts:", grand_total_right_angle)
        mylidar.stop()
        mylidar.stop_motor()
        mylidar.disconnect()
        return grand_total_left, grand_total_right, grand_total_left_angle, grand_total_right_angle

    def find_vanes(self):
        scan = self.scanner()
        vane = []
        for row in scan:
            if 80 < row[1] < 100 and row[2] < 500:
                vane.append(row)
        vane = np.array(vane)
        minimum_index = np.argmin(vane[:, 2])
        first_vane = vane[minimum_index]
        print("first vane", first_vane)

        new_vanes = []
        for row in vane:
            if (row[1] < first_vane[1] - 5 or row[1] > first_vane[1] + 5) and row[2] < first_vane[2] + 20:
                new_vanes.append(row)
        new_vanes = np.array(new_vanes)
        minimum_index_two = np.argmin(new_vanes[:, 2])
        second_vane = new_vanes[minimum_index_two]
        print("second vane", second_vane)
        if first_vane[1] < second_vane[1]:
            arr_mean_L, arr_mean_R, arr_avg_angle_L, arr_avg_angle_R = self.find_exact_vanes(first_vane[1] - 3,
                                                                                             second_vane[1] - 3,
                                                                                             first_vane[1] + 3,
                                                                                             second_vane[1] + 3,
                                                                                             first_vane[2] - 10,
                                                                                             second_vane[2] - 10,
                                                                                             first_vane[2] + 20,
                                                                                             second_vane[2] + 20)
        else:
            arr_mean_L, arr_mean_R, arr_avg_angle_L, arr_avg_angle_R = self.find_exact_vanes(second_vane[1] - 3,
                                                                                             first_vane[1] - 3,
                                                                                             second_vane[1] + 3,
                                                                                             first_vane[1] + 3,
                                                                                             second_vane[2] - 10,
                                                                                             first_vane[2] - 10,
                                                                                             second_vane[2] + 20,
                                                                                             first_vane[2] + 20)
        x_distance_from_left_vane = np.sin(np.radians(arr_avg_angle_L - 90)) * arr_mean_L
        x_distance_from_right_vane = np.sin(np.radians(arr_avg_angle_R - 90)) * arr_mean_R

        z_distance_from_left_vane = np.cos(np.radians(arr_avg_angle_L - 90)) * arr_mean_L
        z_distance_from_right_vane = np.cos(np.radians(arr_avg_angle_R - 90)) * arr_mean_R

        mean_z_distance = (abs(z_distance_from_left_vane) + abs(z_distance_from_right_vane)) / 2
        x_distance_to_center = (x_distance_from_left_vane + x_distance_from_right_vane) / 2
        return x_distance_to_center / 1000, mean_z_distance / 1000


print(MyRPLidar.find_vanes())
