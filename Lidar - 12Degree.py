# Animates distances and measurment quality
from rplidar import RPLidar
import time
import numpy as np
PORT_NAME = 'COM3'
DMAX = 500  # was 4000
IMIN = 0
IMAX = 500
som = 0


def run():
    mylidar = RPLidar(PORT_NAME, baudrate=115200)
    # info = mylidar.get_info()
    # print(info)
    som = 0.0
    total = 0
    aver = 0.0
    arr_avg = []


    # health = mylidar.get_health()
    # print(health)
    aver2 = 0
    mylidar_scan = []



    for y in range(0,15):

        for i, scan in enumerate(mylidar.iter_scans(scan_type='normal', max_buf_meas=60000)):
            #print('%d: Got %d measures' % (i, len(scan)))
            #
            mylidar_scan.append(scan)
            if i > 10:
                break

        for i in range(len(mylidar_scan)): #aantal rondes


            #print("Len lidarscan i : ", len(mylidar_scan[i]))
            for j in range(len(mylidar_scan[i])): #aantal metingen in het rondje
                mylist = mylidar_scan[i][j]
                # print(mylist[2])

                if 86.5 < mylist[1] < 89 and 150 < mylist[2] < 300:
                    # total = total + 1
                    som = mylist[2]
                    total = 1
                    #print(mylist)
                if total == 1:
                    # aver = som / total
                    arr_avg.append(som)
                    som = 0.0
                    total = 0

            #print("arr_avg: ", arr_avg)
            arr_mean = np.mean(arr_avg)
            print("arr_mean: ", arr_mean)



        '''
        total2 = len(mylidar_scan)
        aver2 = aver + aver2
        aver2 = aver2/ total2
        print("total aver: ",aver2)'''
        mylidar.clean_input()


    mylidar.stop()
    mylidar.stop_motor()
    mylidar.disconnect()


if __name__ == '__main__':
    run()
