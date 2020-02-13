import logging
import math
import time
from math import pi

import numpy as np
import urx

import lidar_circle as lidar


class MyRobot(urx.Robot):
    def __init__(self, host, port):
        super().__init__(host)
        self.mylidar = lidar.MyRPLidar(port)
        self.safe_jpos = ([0.283, -0.416, -2.305, 1.152, 1.571, -0.283])
        self.acc = 0.1
        self.vel = 0.2
        self.correctionX = 0.0
        self.correctionZ = 0.0
        self.diameter = 0.975 + 2 * 0.017 + 0.03 + 0.005 # #Was:1.015+0.1
        self.radius = self.diameter / 2
        self.stationJPose = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.middleStatorPose = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.middleStatorJPose = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.middlePose = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    def __del__(self):
        print("Deleted")

    def on_startup(self):
        gripper_pin = 0
        # Start position with all joints within limits
        print("Going to startup pose! \n")
        self.set_digital_out(gripper_pin, True)  # Gripper closed
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
        delta_x, delta_y = self.mylidar.find_middle()
        pose[0] += delta_x
        pose[1] += delta_y  #
        self.movel(pose, acc=self.acc, vel=self.vel)
        print("Delta X = ", delta_x)
        print("Delta Y = ", delta_y)


        # Second measurement with the lidar to check.
        for i in range(2):
            delta_x, delta_y = self.mylidar.find_middle_offsets()
            print("Delta X = ", delta_x)
            print("Delta Y = ", delta_y)
            pose[0] += delta_x  # + 0.061#+0.02 #+ 0.061 # deltaX + offset of lidar
            pose[1] += delta_y  # +0.02# + 0.0185 # deltaY + offset of lidar
            self.movel(pose, acc=self.acc / 2, vel=self.vel)
        pose[1] -= 0.001
        pose[0] += 0.061 - 0.0229
        pose[2] -= 0.1
        # rotate so that tip EOAT is in LIDAR pose
        pose = [pose[0], pose[1], pose[2], 0, 0, -1.57]
        self.movel(pose, acc=self.acc, vel=self.vel)
        print("Done calibrating center! \n")

    def tape_station(self):
        # Go to tapestation and grab tape
        print("Going to tapestation!")
        gripper_pin = 0
        servo_pin = 1
        hold_tape_pin = 2
        self.set_digital_out(servo_pin, False)  # Close servo
        self.set_digital_out(hold_tape_pin, False)  # Close servo
        v = 0.05
        a = 0.03

        stationJPose = [1.9059884629302861, -1.1397081872494461, -2.0799622606546024, -1.4943256110586116,
                        1.5710074217261376, -1.234022953675229]  # starting J pose
        grabTapePose = [0.065, 0.455, 0.221, 2.222, 2.219, 0]  # Grabbing pose y stond op 445
        forwardTapePose = [0.065, 0.457, 0.082, 2.222, 2.219, 0]  # move forward and flatten 0.062 old [0.065, 0.455, 0.082, 2.222, 2.219, -0.001]

        # Movements

        self.movel(self.middlePose, acc=a, vel=v * 2)  # LPose middle down
        self.movej(stationJPose, acc=a, vel=v * 4)  # JPose near the station
        self.set_digital_out(gripper_pin, False)  # Gripper closed

        self.movel(grabTapePose, acc=a, vel=v)  # Go to grab tape

        self.set_digital_out(gripper_pin, True)  # Gripper closed


        self.movel(forwardTapePose, acc=a, vel=v)  # Pull tapeforward
        self.set_digital_out(hold_tape_pin, True)  # Hold tape with cyllinder



        self.movel([forwardTapePose[0] + .004, forwardTapePose[1], forwardTapePose[2] - 0.005, forwardTapePose[3],
                    forwardTapePose[4], forwardTapePose[5]], acc=a, vel=v)

        self.set_digital_out(servo_pin, True)  # Close servo
        time.sleep(1)

        forwardTapePose[0] -= 0.1
        self.movel(forwardTapePose, acc=a, vel=v)


        self.movej(stationJPose, acc=a, vel=v * 2)  # JPose near the station

        self.movej(self.middleStatorJPose, acc=self.acc, vel=self.vel * 2)

        self.set_digital_out(hold_tape_pin, False)  # Hold tape pneuma
        print("Tapestation done \n")

    def move_to_middle(self):
        print("Going to middle")

        self.movel(self.middleStatorPose, acc=self.acc, vel=self.vel)

    def tape_movement(self, i):
        #move in front of two vanes, scans every third iteration and tapes in between vanes
        gripper_pin = 0
        servo_pin = 1
        # Taping movement
        print("Tape movement!")
        d_horizontal = 0.155  # 0.14 #Forward distance
        d_vertical = 0.013 + 0.0025# Pushing down distance
        ogvAngle = np.deg2rad(10)  # Horizontal angle of the OGV's
        if not i % 3:
            #             #Get correction distances from LIDAR
            self.correctionX, self.correctionZ = self.mylidar.find_vanes()
            print("X = ", self.correctionX, "\nZ = ", self.correctionZ)
            # time.sleep(0.5)
            #       correctionX = -correctionX
            self.correctionX += 0.006  # 0.025 #0.0225  # offset of lidar
            self.correctionZ -= (0.17 + 0.05)  # 0.1825 Lidar offset
            print("X = ", self.correctionX, "\nZ = ", self.correctionZ)

        self.translate_tool((self.correctionX, 0, self.correctionZ), acc=self.acc, vel=self.vel)

        #    Rotate the EOAT horizontal in line with the OGV's
        time.sleep(1)
        rotateDistance = math.tan(ogvAngle) * 0.22  # 0.252 + distEOAT + clearance
        self.translate_tool((rotateDistance, 0, 0), acc=self.acc, vel=self.vel)

        t = self.get_pose()
        t.orient.rotate_xt(np.deg2rad(-2))
        t.orient.rotate_yt(-ogvAngle)
        self.set_pose(t, vel=self.vel, acc=self.acc)

        # Go forward, Down, Up, and Back
        time.sleep(1)
        self.translate_tool((0, 0, d_horizontal), acc=self.acc, vel=self.vel)

        self.translate_tool((0, d_vertical, 0), acc=self.acc, vel=self.vel)

        self.set_digital_out(gripper_pin, False)  # Hold tape pneuma
        self.set_digital_out(servo_pin, False)  # Close servo
        time.sleep(0.5)

        self.translate_tool((0, -(d_vertical + .02), 0), acc=self.acc, vel=self.vel)
        self.translate_tool((0, 0, -d_horizontal), acc=self.acc, vel=self.vel)
        self.set_digital_out(gripper_pin, True)  # Hold tape pneuma
        time.sleep(0.5)
        # Rotate EOAT back

        t = self.get_pose()
        t.orient.rotate_yt(ogvAngle)
        t.orient.rotate_xt(np.deg2rad(2))
        self.set_pose(t, acc=self.acc, vel=self.vel)
        self.translate_tool((-rotateDistance, 0, -.05), acc=self.acc, vel=self.vel)

        print("Tape movement done! \n")

    def demo(self, thread_queue=None):
        #scans every iteration and doesn't go to tape station
        print("Demo mode started!")

        v = 0.1
        a = 0.1
        invert = False

        self.on_startup()  # Joint move in middle of joint limits UR10
        self.calibrate_to_center()  # Get center with LIDAR
        self.middleStatorPose = self.getl()
        print("Current Toolpose : ", self.middleStatorPose[0],",",self.middleStatorPose[1],
              ",",self.middleStatorPose[2],",",self.middleStatorPose[3],",",self.middleStatorPose[4],
                ",",self.middleStatorPose[5])

        try:
            for i in range(2, 17):  # 35
                print(i, "th tape motion of the 76.")
                x = -math.sin(np.deg2rad(360 / 76 * i)) * self.radius + self.middleStatorPose[0]
                y = -math.cos(np.deg2rad(360 / 76 * i)) * self.radius + self.middleStatorPose[1]
                z = self.middleStatorPose[2] - 0.03  # -0.2
                rz = - np.deg2rad(360 / 76 * i)

                # Necessary with rotvectors. Past pi it needs to start at 0 again.
                if rz >= pi:
                    invert = True
                if invert == True:
                    rz = -rz

                # Pose between OGV's
                pose = [x, y, z, 0, 0, rz]  # x-0.345
                self.movel(pose, acc=a, vel=v)
                self.tape_movement(0)
        finally:
            print("Demo finished!")
            self.close()

    def run(self, thread_queue=None):
        # Configure Robot
        logging.basicConfig(level=logging.WARN)
        time.sleep(1)
        v = 0.2
        a = 0.1
        invert = False

        self.on_startup()  # Joint move in middle of joint limits UR10
        self.calibrate_to_center()  # Get center with LIDAR

        self.middleStatorPose = self.getl()
        self.middleStatorJPose = self.getj()
        print("Current Toolpose : ", self.middleStatorPose[0],",",self.middleStatorPose[1],
              ",",self.middleStatorPose[2],",",self.middleStatorPose[3],",",self.middleStatorPose[4],
                ",",self.middleStatorPose[5])

        self.stationJPose = [1.9059884629302861, -1.1397081872494461, -2.0799622606546024, -1.4943256110586116,
                             1.5710074217261376, -1.234022953675229]  # starting J pose
        # self.middleStatorPose = [-0.20425021588029 , -0.16873647189096627 , 0.800126526162701 , 0.00023370321567888587 , -3.243348589822535e-05 , -1.5699666275861346] #remove when using LIDAR
        self.middlePose = [self.middleStatorPose[0] + 0.2, self.middleStatorPose[1], self.middleStatorPose[2] - 0.15,
                           -1.208, 1.208, -1.208]

        self.movel(self.middleStatorPose, acc=a, vel=v)

        try:
            for i in range(2, 17):  # 35
                self.tape_station()
                print(i, "th tape motion of the 76.")

                x = -math.sin(np.deg2rad(360 / 76 * i)) * self.radius + self.middleStatorPose[0]
                y = -math.cos(np.deg2rad(360 / 76 * i)) * self.radius + self.middleStatorPose[1]
                z = self.middleStatorPose[2] - 0.03  # -0.2
                rz = - np.deg2rad(360 / 76 * i)

                # Necessary with rotvectors. Past pi it needs to start at 0 again.
                if rz >= pi:
                    invert = True
                if invert == True:
                    rz = -rz

                # Pose between OGV's
                pose = [x, y, z, 0, 0, rz]  # x-0.345
                self.movel(pose, acc=a, vel=v)
                self.tape_movement(i - 2)
            self.movel(self.middleStatorPose, acc=a, vel=v)

        finally:
            print("Program finished!")
            self.close()



myrobot = MyRobot("192.168.1.102", 'COM3')
#myrobot.demo() #runs demo program
myrobot.run() #runs normal program
