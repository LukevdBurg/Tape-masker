import numpy as np
from rplidar import RPLidar


class MyRPLidar(RPLidar):
    def __init__(self, port):
        super().__init__(port)
        info = self.get_info()
        print(info)
        health = self.get_health()
        print(health)
        self.reset()
        self.port = port

    def scanner(self):
        scan = []

        iterator = self.iter_scans()
        for i in range(0, 10):
            scan += next(iterator)
        self.stop()
        self.stop_motor()
        # lidar.disconnect()
        return scan

    def find_circle(self):
        measurements = np.array(self.scanner())
        distances = measurements[:, 2]
        mean_distance = np.mean(distances)
        max_distance = np.max(distances)

        if 900 > mean_distance > 600 and max_distance < 1400:
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

        return xdist, zdist

    def find_middle_offsets(self):
        measurements = np.array(self.scanner())
        west_points = []
        north_points = []
        east_points = []
        south_points = []
        for row in measurements:
            if row[1] > 358 or row[1] < 2:
                west_points.append(row[2])
            if 88 < row[1] < 92:
                north_points.append(row[2])
            if 178 < row[1] < 182:
                east_points.append(row[2])
            if 268 < row[1] < 272:
                south_points.append(row[2])
        avg_west = np.mean(west_points)
        avg_north = np.mean(north_points)
        avg_east = np.mean(east_points)
        avg_south = np.mean(south_points)
        print("W:", avg_west)
        print("N:", avg_north)
        print("E:", avg_east)
        print("S:", avg_south)
        return (avg_north - avg_south) / 1000 / 2, (avg_west - avg_east) / 1000 / 2

    def find_exact_vanes(self, lower_angle_L, lower_angle_R, upper_angle_L, upper_angle_R, lower_distance_L,
                         lower_distance_R,
                         upper_distance_L, upper_distance_R):
        # Removed due to bugfixing
        # mylidar = RPLidar("COM3", baudrate=115200)
        mylidar_scan = []
        total_average_left_vane = []
        total_average_right_vane = []
        total_average_angle_left_vane = []
        total_average_angle_right_vane = []

        for y in range(0, 20):

            for i, scan in enumerate(self.iter_scans(scan_type='normal',
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
                    elif lower_angle_R < my_list[1] < upper_angle_R and lower_distance_R < my_list[
                        2] < upper_distance_R:
                        right_vane.append(my_list)

            # print("arr_avg: ", arr_avg)
            if left_vane:
                left_vane = np.array(left_vane)
                average_left_vane = np.mean(left_vane[:, 2])
                average_angle_left_vane = np.mean(left_vane[:, 1])

                total_average_left_vane.append(average_left_vane)
                total_average_angle_left_vane.append(average_angle_left_vane)
                print("Average left", average_left_vane)

            if right_vane:
                right_vane = np.array(right_vane)
                average_right_vane = np.mean(right_vane[:, 2])
                average_angle_right_vane = np.mean(right_vane[:, 1])

                total_average_right_vane.append(average_right_vane)
                total_average_angle_right_vane.append(average_angle_right_vane)
                print("Average right", average_right_vane)

            self.clean_input()
        grand_total_left = np.mean(total_average_left_vane)
        grand_total_right = np.mean(total_average_right_vane)
        grand_total_left_angle = np.mean(total_average_angle_left_vane)
        grand_total_right_angle = np.mean(total_average_angle_right_vane)
        print("totaal links:", grand_total_left)
        print("totaal rechts:", grand_total_right)
        print("totaal hoek links:", grand_total_left_angle)
        print("totaal hoek rechts:", grand_total_right_angle)
        self.stop()
        self.stop_motor()
        # mylidar.disconnect()
        return grand_total_left, grand_total_right, grand_total_left_angle, grand_total_right_angle

    def find_vanes(self):
        scan = self.scanner()
        vane = []
        for row in scan:
            if 78 < row[1] < 102 and row[2] < 500:
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

# lidar = MyRPLidar('COM3')
# lidar.find_middle()
