# Animates distances and measurment quality
from rplidar import RPLidar
import time
import numpy as np
from scipy import stats
PORT_NAME = 'COM3'
DMAX = 500  # was 4000
IMIN = 0
IMAX = 500



def run():
    mylidar = RPLidar(PORT_NAME, baudrate=115200)
    # info = mylidar.get_info()
    # print(info)

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

            som = []
            #print("Len lidarscan i : ", len(mylidar_scan[i]))
            for row in mylidar_scan[i]: #aantal metingen in het rondje
                #mylist = mylidar_scan[i][j]
                # print(mylist[2])
                if 86.5 < row[1] < 89 and 150 < row[2] < 300:
                    som.append(row[2])
                    #print(row)
        som = np.array(som)
        print('som: ',som)
        aver = np.mean(som)
        # stats.mode()
        print("avg: ",aver)



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
