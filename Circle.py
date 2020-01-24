# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 15:08:28 2019
update
@author: David
"""
import urx
import logging
import numpy as np
import time

from math import pi, cos, sin, acos
import math 
import lidar_circle as lidar

class MyRobot(urx.Robot):
    # TODO Make it optional to start with the safe pose
    def __init__(self, host, port):
        super().__init__(host)
        self.mylidar = lidar.MyRPLidar(port)
        self.safe_jpos = ([0.283, -0.416, -2.305, 1.152, 1.571, -0.283])
        self.acc = 0.3
        self.vel = 0.1

            
    def __del__(self):
        print ("Deleted")
        
    def on_startup(self):
        # Start position with all joints within limits
        print("Going to startup pose! \n")
        self.movel((0, 0, -0.15, 0, 0, 0), acc=self.acc, vel=self.vel, relative=True)
        self.movej(self.safe_jpos, acc=self.acc, vel=self.vel)
        
        
    def calibrate_to_center(self):
        # Calibrate to the center of the rotor
        print("Calibrating Center!")
        # Rotate EOAT 90 degrees for LIDAR
        pose = self.getl()
        self.movel([pose[0], pose[1], pose[2], -1.21, 1.21, -1.21], acc=self.acc, vel=self.vel / 2)
        pose = self.getl()
        lidar_check = False
        
        # Move 50mm forward till LIDAR is within motor. 
        for i in range(20):
            #        if i == 5: lidarCheck = True
            lidar_check = self.mylidar.find_circle()
            if lidar_check: break
            pose[2] += 0.05
            self.movel(pose, acc=self.acc / 2, vel=self.vel)
        
        # Move LIDAR to center of motor
#        for i in range(1):
        delta_x, delta_y = self.mylidar.find_middle()
        pose[0] += delta_x
        pose[1] += delta_y# 
        self.movel(pose, acc=self.acc, vel=self.vel) 
        print("Delta X = ", delta_x)
        print("Delta Y = ", delta_y)
#        delta_x, delta_y = self.mylidar.find_middle()
#        pose[0] += delta_x
#        pose[1] += delta_y# 
#        self.movel(pose, acc=self.acc, vel=self.vel) 

        #Second measurement with the lidar to check. 
        for i in range(2):
            delta_x, delta_y = self.mylidar.find_middle_offsets()
            print("Delta X = ", delta_x)
            print("Delta Y = ", delta_y)
            pose[0] += delta_x #+ 0.061#+0.02 #+ 0.061 # deltaX + offset of lidar
            pose[1] += delta_y #+0.02# + 0.0185 # deltaY + offset of lidar
            self.movel(pose, acc=self.acc/2, vel=self.vel)
#        pose[1] -=0.001
#        pose[0] +=0.061-0.0229
        #rotate so that tip EOAT is in LIDAR pose    
#        pose = [pose[0], pose[1], pose[2], 0, 0, -1.57]
#        self.movel(pose, acc=self.acc, vel=self.vel)
        print("Done calibrating center! \n")
       
    
    def tape_station(self):
        # Go to tapestation and grab tape
        print("Going to tapestation!")
        v = 0.05
        a = 0.03
        self.movel((0, 0, -0.15, 0, 0, 0), acc=a, vel=v, relative=True)
        #Hardcoded poses of the station
    #    stationPose = [-0.161,  0.153,  0.912,  1.027,  1.392, -1.026]
        stationJPose = [1.906 , -1.154 , -2.172 , -1.388 , 1.571 , -1.234] #starting J pose
        grabTapePose = [ 0.058 , 0.457 , 0.216 , 2.222 , 2.219 , -0.001] #Grabbing pose
        forwardTapePose = [0.065 , 0.457 , 0.072 , 2.222 , 2.219 , -0.001] #move forward and flatten 0.062
        gripper_pin = 0
        servo_pin = 1
        
        # Movements
    #    self.move_to_middle() # Go to middle of motor at start and end
        self.movej(stationJPose, acc=a,vel=v*2) #JPose near the station
        self.movel(grabTapePose, acc=a,vel=v)  #Go to grab tape
        time.sleep(2) #Remove when gripper connected
    #    closeGripper()
        self.set_digital_out(gripper_pin, True) #Gripper closed
        time.sleep(2) #Remove when gripper connected
        
        self.movel(forwardTapePose, acc=a,vel=v)   #Pull tapeforward
    
        forwardTapePose[0] -= 0.05 #dont know check!
#        Closepusher
    #    self.translate_tool((0, 0, 0.02), acc=a, vel=v) #move forward for 
        self.set_digital_out(servo_pin, True) #Close servo
        self.movel(forwardTapePose, acc=a,vel=v)
        time.sleep(1.5) #Remove when servo connected
        self.movej(stationJPose, acc=a,vel=v*2) #JPose near the station
        self.movej(middleStatorJPose, acc=self.acc, vel=self.vel * 2)
        print("Tapestation done \n")
    
    
    def move_to_middle(self):
        print("Going to middle")
        #Simple function to go to middle of rotor everytime
#        self.movej(middleStatorJPose, acc=self.acc, vel=self.vel * 2)
        self.movel(middleStatorPose, acc=self.acc, vel=self.vel)
        
    def tape_movement(self):
        # Taping movement
        print("Tape movement!")
        d_horizontal = 0.14#0.14 #Forward distance
        d_vertical = 0.02 #Pushing down distance
        ogvAngle = np.deg2rad(9) #Horizontal angle of the OGV's

#             #Get correction distances from LIDAR
        correctionX, correctionZ = self.mylidar.find_vanes()
        print("X = ",correctionX, "\nZ = ", correctionZ)
        time.sleep(0.5)
#       correctionX = -correctionX
        correctionX += 0.006 #0.025 #0.0225  # offset of lidar
        correctionZ -= (0.17 + 0.05)  #0.1825 Lidar offset
        print("X = ",correctionX, "\nZ = ", correctionZ)
       
        self.translate_tool((correctionX, 0, correctionZ), acc=self.acc, vel=self.vel)
    
    #    Rotate the EOAT horizontal in line with the OGV's
        time.sleep(0.5)
        rotateDistance = math.tan(ogvAngle) * 0.258 #0.252 + distEOAT + clearance 
        self.translate_tool((rotateDistance, 0, 0), acc=self.acc, vel=self.vel)
    
        t = self.get_pose()
        t.orient.rotate_yt(-ogvAngle)
        self.set_pose(t, vel=self.vel, acc=self.acc)
        

        # Go forward, Down, Up, and Back
        time.sleep(2)
        self.translate_tool((0, 0, d_horizontal), acc=self.acc, vel=self.vel)
        time.sleep(2)
        self.translate_tool((0, d_vertical, 0), acc=self.acc, vel=self.vel)
        time.sleep(2)
        self.translate_tool((0, -d_vertical, 0), acc=self.acc, vel=self.vel)
        self.translate_tool((0, 0, -d_horizontal), acc=self.acc, vel=self.vel)

        
        #Rotate EOAT back
        time.sleep(5)
        t = self.get_pose()
        t.orient.rotate_yt(ogvAngle)
        self.set_pose(t,  acc=self.acc, vel=self.vel)
        self.translate_tool((-rotateDistance, 0, 0),  acc=self.acc, vel=self.vel)
    #    '''
        myrobot.mylidar.disconnect()
        print("Tape movement done! \n")

    
    
if __name__ == "__main__":
    #Configure Robot
    logging.basicConfig(level=logging.WARN)
#    rob = urx.Robot("192.168.1.102", True)
    myrobot = MyRobot("192.168.1.102", 'COM3')
    myrobot.mylidar.disconnect()
    time.sleep(1)
    v = 0.1
    a = 0.3
    diameter = 0.975 + 2*0.017 + 0.03#  #Was:1.015+0.1
    radius = diameter / 2
    invert = False
#
#    x, z = lidar.find_vane()
#    print("X = ",x, "\nZ = ", z)
    
    myrobot.on_startup() #Joint move in middle of joint limits UR10
    myrobot.calibrate_to_center() #Get center with LIDAR
    middleStatorPose = myrobot.getl()
    middleStatorJPose = myrobot.getj()
    print("Current Toolpose : ", middleStatorPose[0],",",middleStatorPose[1],
          ",",middleStatorPose[2],",",middleStatorPose[3],",",middleStatorPose[4],
          ",",middleStatorPose[5])
#    middleStatorPose = [-0.22125550777766975 , -0.2216703085172856 , 0.9501686433671546 , 0.0001417514385128543 , -2.918742915754314e-05 , -1.5700249372510269] #remove when using LIDAR

#    myrobot.tapeStation()
#    myrobot.tape_movement()
#    myrobot.move_to_middle()
    try:
#            print(i, ": ", myrobot.tape_movement())
#        myrobot.tape_movement()



#        rob.movej(middleStatorJPose, acc=a, vel=v*2)
        for i in range(1, 76): #35
#            if (18 > i => 20 ):
            if not (17 <= i <20): # not on 18, 19 and 20. Because of woodenbeam
                #myrobot.tape_station()
                print(i, "th tape motion of the 76." )
#                toolpose = myrobot.getl()
    #            print("Current Toolpose : ", toolpose)
                x = -math.sin(np.deg2rad(360/76* i))*radius + middleStatorPose[0]
                y = -math.cos(np.deg2rad(360/76* i))*radius + middleStatorPose[1]
                z = middleStatorPose[2] -0.03 #-0.2
                rz = - np.deg2rad(360/76 * i)

                # Necessary with rotvectors. Past pi it needs to start at 0 again. 
                if rz >= pi :
                    invert = True
                if invert == True:
                    rz =-rz
                
                # Pose between OGV's
                pose = [x,y,z,0,0,rz] #x-0.345
                myrobot.movel(pose, acc=a, vel=v)
                #myrobot.tape_movement()

#   '''
    finally:
        print("Program finished!")
        myrobot.close()