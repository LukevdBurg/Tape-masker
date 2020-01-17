# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 15:08:28 2019

@author: David
"""
import logging
import math
import time

import lidar as lidar
import numpy as np
import urx


class MyRobot(urx.Robot):
    #TODO Make it optional to start with the safe pose
    def __init__(self, host, port):
        super().__init__(host)
        self.mylidar = lidar.MyRPLidar(port)
        self.safe_pos = ([0.283, -0.416, -2.305, 1.152, 1.571, -0.283])
        self.acc = 0.3
        self.vel = 0.1
        #self.startup()

    def startup(self):
        # Start position with all joints within limits
        print("Going to startup pose! \n")
        self.movej(self.safe_pos, acc=a, vel=v)

    def calibrateCenter(self):
        # Calibrate to the center of the rotor
        print("Calibrating Center!")
        # Rotate EOAT 90 degrees for LIDAR
        pose = self.getl()
        self.movel([pose[0], pose[1], pose[2], -1.21, 1.21, -1.21], acc=a, vel=v / 2)
        pose = self.getl()
        lidarCheck = False

        # Move 50mm forward till LIDAR is within motor.
        for i in range(20):
            #        if i == 5: lidarCheck = True
            lidarCheck = self.mylidar.find_circle()
            if (lidarCheck == True): break
            pose[2] += 0.05
            self.movel(pose, acc=a / 2, vel=v)

        # Move LIDAR to center of motor
        deltaX, deltaY = lidar.find_middle()
        pose[0] += deltaX
        pose[1] += deltaY
        self.movel(pose, acc=a, vel=v)

        # Second measurement with the lidar to check.
        deltaX, deltaY = lidar.find_middle()
        pose[0] += deltaX  # deltaX + offset of lidar
        pose[1] += deltaY  # deltaY + offset of lidar

        # rotate so that tip EOAT is in LIDAR pose
        pose = [pose[0], pose[1], pose[2], 0, 0, -1.57]
        self.movel(pose, acc=a, vel=v)
        print("Done calibrating center! \n")

    def tapeStation(self):
        # Go to tapestation and grab tape
        print("Going to tapestation!")
        v = 0.2
        a = 0.2

        # Hardcoded poses of the station
        #    stationPose = [-0.161,  0.153,  0.912,  1.027,  1.392, -1.026]
        stationJPose = [-1.488, -0.328, -1.828, -1.041, 1.746, 1.519]  # starting J pose
        grabTapePose = [-0.135, 0.108, 0.912, 1.027, 1.392, -1.026]  # Grabbing pose
        forwardTapePose = [-0.135, 0.03, 0.912, 1.16, 1.322, -1.146]  # move forward and flatten

        # Movements
        self.moveToMiddle()  # Go to middle of motor at start and end
        self.movej(stationJPose, acc=a, vel=v * 2)
        self.movel(grabTapePose, acc=a, vel=v)
        #    closeGripper()
        time.sleep(1.5)  # Remove when gripper connected

        self.movel(forwardTapePose, acc=a, vel=v)
        forwardTapePose[1] -= 0.01
        self.translate_tool((0, 0, 0.02), acc=a, vel=v)
        #    closeServo()
        time.sleep(1.5)  # Remove when servo connected

        #    rob.movel(middleStatorPose, acc=a, vel=v)
        self.moveToMiddle()  # Go to middle of motor at start and end
        print("Tapestation done \n")

    def moveToMiddle(self):
        # Simple function to go to middle of rotor everytime
        self.movej(middleStatorJPose, acc=a, vel=v * 2)

    def tapeMovement(self):
        # Taping movement
        # TODO REMOVE SLEEPS!
        # print("Tape movement!")
        deltaHorizontal = 0.02  # Forward distance
        deltaVertical = 0.00  # Pushing down distance
        ogvAngle = np.deg2rad(8)  # Horizontal angle of the OGV's

        pose = self.getl()

        # Get correction distances from LIDAR
        correctionX, correctionZ = self.mylidar.find_vane()
        # print("X = ", correctionX, "\nZ = ", correctionZ)
        time.sleep(3)
        #   correctionX = -correctionX
        correctionX -= 0.00  # 0.0225  # offset of lidar
        correctionZ -= (0.1825 + 0.02)  # -0.25 offset of lidar - dist EOAT + clearance
        # print("X = ", correctionX, "\nZ = ", correctionZ)

        self.translate_tool((correctionX, 0, correctionZ), acc=a, vel=v)

        # Rotate the EOAT horizontal in line with the OGV's
        time.sleep(3)
        rotateDistance = math.tan(np.deg2rad(12)) * 0.258  # 0.252 + distEOAT + clearance
        self.translate_tool((rotateDistance, 0, 0), acc=a, vel=v)

        t = self.get_pose()
        t.orient.rotate_yt(-ogvAngle)
        self.set_pose(t, vel=v, acc=a)

        # Go forward, Down, Up, and Back
        time.sleep(2)
        self.translate_tool((0, 0, deltaHorizontal), acc=a, vel=v)
        time.sleep(2)
        self.translate_tool((0, deltaVertical, 0), acc=a, vel=v)
        time.sleep(2)
        self.translate_tool((0, -deltaVertical, 0), acc=a, vel=v)
        self.translate_tool((0, 0, -deltaHorizontal), acc=a, vel=v)

        # Rotate EOAT back
        t = self.get_pose()
        t.orient.rotate_yt(ogvAngle)
        self.set_pose(t, vel=v, acc=a)

        self.movel([pose[0], pose[1], pose[2], pose[3], pose[4], pose[5]], acc=a, vel=v / 2)

        # print("Tape movement done! \n")
        return correctionX, correctionZ


if __name__ == "__main__":
    # Configure Robot
    logging.basicConfig(level=logging.WARN)
    # rob = urx.Robot("192.168.1.102", True)

    myrobot = MyRobot("192.168.1.102", 'COM3')

    v = 0.1
    a = 0.3
    diameter = 1.015 + 0.1  # + 0.1 for clearance
    radius = diameter / 2
    invert = False
    #
    #    x, z = lidar.find_vane()
    #    print("X = ",x, "\nZ = ", z)

    #    calibrateCenter()  #Get center with LIDAR

    #    middleStatorPose = rob.getl()
    middleStatorPose = [-0.219, -0.242, 0.83, 0.0, -0.0, -1.57]  # remove when using LIDAR
    middleStatorJPose = myrobot.getj()
    #    moveToMiddle()
    #    moveToMiddle()
    toolpose = myrobot.getl()
    print("Current Toolpose : ", toolpose)

    try:
        for i in range(0, 5):
            print(i, ": ", myrobot.tapeMovement())
        '''
        i = 0 #2 # Start at 3nd OGV because woodenbeam
#        rob.movej(middleStatorJPose, acc=a, vel=v*2)
        for i in range(76): #35
#            if not (18 <= i <21): # not on 18, 19 and 20. Because of woodenbeam
#                tapeStation()
            print(i, "th tape motion of the 76." )
            toolpose = rob.getl()
#                print("Current Toolpose : ", toolpose)
            x = -math.sin(np.deg2rad(360/76* i))*radius + middleStatorPose[0]
            y = -math.cos(np.deg2rad(360/76* i))*radius + middleStatorPose[1]
            z = middleStatorPose[2] -0.05 #-0.2
            rz = - np.deg2rad(360/76 * i)
            
            # Necessary with rotvectors. Past pi it needs to start at 0 again. 
            if rz >= pi :
                invert = True
            if invert == True:
                rz =-rz
            
            # Pose between OGV's
            pose = [x,y,z,0,0,rz] #x-0.345
            rob.movel(pose, acc=a, vel=v)
            tapeMovement()

#        '''
    finally:
        print("Program finished!")
        myrobot.close()
