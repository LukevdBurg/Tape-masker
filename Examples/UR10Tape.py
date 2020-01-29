
import urx
import logging
import numpy as np
import time


import math
import numpy as np

def rpy2rotvec(roll, pitch, yaw):
    print ("roll = ", roll)
    print ("pitch = ", pitch)
    print ("yaw = ", yaw)
    print ("")
    
    yawMatrix = np.matrix([
    [math.cos(yaw), -math.sin(yaw), 0],
    [math.sin(yaw), math.cos(yaw), 0],
    [0, 0, 1]])
    
    pitchMatrix = np.matrix([
    [math.cos(pitch), 0, math.sin(pitch)],
    [0, 1, 0],
    [-math.sin(pitch), 0, math.cos(pitch)]])
    
    rollMatrix = np.matrix([
    [1, 0, 0],
    [0, math.cos(roll), -math.sin(roll)],
    [0, math.sin(roll), math.cos(roll)]])
    
    R = yawMatrix * pitchMatrix * rollMatrix
    
    theta = math.acos(((R[0, 0] + R[1, 1] + R[2, 2]) - 1) / 2)
    multi = 1 / (2 * math.sin(theta))
    
    rx = multi * (R[2, 1] - R[1, 2]) * theta
    ry = multi * (R[0, 2] - R[2, 0]) * theta
    rz = multi * (R[1, 0] - R[0, 1]) * theta
#    rpy2rotvec(tpose[3],tpose[4],tpose[5])        
#    rpy2rotvec(0, 0, 20)
    print (rx, ry, rz)
    return rx,ry,rz




if __name__ == "__main__":
    logging.basicConfig(level=logging.WARN)

    rob = urx.Robot("192.168.1.102", True)
    pi = 3.141592
#    rob = urx.Robot("localhost")
#    rob.set_tcp((0,0,0,0,0,0))
#    rob.set_payload(0.5, (0,0,0))
    

    try:

        toolpose = rob.getl()
        print("get l : ", toolpose)
        l = 0.05
        v = 0.05
        a = 0.03
        time.sleep(1.0)

#        pose = rob.getl()
#        print("robot tcp  is at: ", pose)
##
        t = get_actual.tcp_pose
        t = rob.get_pose()
        print("get_pose : ", t)
        tpose = rob.getl()
        
#        rx,ry,rz = rpy2rotvec(0,pi,pi)
        
        tpose = [tpose[0], tpose[1], tpose[2],0,0 ,0]
#        rob.movel(tpose, acc=a, vel=v)
        print("Robot moved")
        pose = rob.getl()
        print("robot tcp  is at: ", pose)
#        tposehome = tpose
#        tapepose = [pose[0],pose[1],pose[2],-3.14,0,0]
#        rob.movel(tpose, acc=a, vel=v)
#        time.sleep(0.2)  
#        tapepose[0] += 0.10
#        rob.movel(tapepose, acc=a, vel=v)
#        time.sleep(0.2)  
#        tapepose[2] += 0.2
#        rob.movel(tapepose, acc=a, vel=v)
#        time.sleep(0.2)        
#        pose = rob.getl()
#        print("robot tcp  is at: ", pose)
#        
        
#        tpose[2] += 0.05
#        rob.movel(tposehome, acc=a, vel=v)
#        time.sleep(0.2)        
#        tpose = tposehome
#        rob.movel(tpose, acc=a, vel=v)
#        time.sleep(0.2)        
#        tpose[0] += 0.2
#        rob.movel(tpose, acc=a, vel=v)
#        time.sleep(0.2)
#        tpose[2] += 0.05
#        rob.movel(tpose, acc=a, vel=v)    
#        time.sleep(0.2)
#        tpose[4] += 1.5708
#        rob.movel(tpose, acc=a, vel=v)            
        
        
#        time.sleep(0.2) 
#        tape_pose1 = (1.03666170207329, -0.17172660009261717, 0.11550836647039069, -0.44432891976097505, 1.139893918215399, -0.7616990679526947)
#        rob.movel(tape_pose1, acc=a, vel=v)
#        time.sleep(0.2) 
#        tape_pose2 = (1.0078263970242933, -0.17052762873999108, 0.09053428308442371, -0.4098681363008715, 1.0632073462383589, -0.7717274389078442)
#        rob.movel(tape_pose2, acc=a, vel=v)
#        time.sleep(0.2) 
#        tape_pose21 = (1.0363173946446946, -0.17035568803450224, 0.08992995549397724, -0.4171223884164084, 1.0790293021424637, -0.7694530374732225)
#        rob.movel(tape_pose21, acc=a, vel=v)        
#        time.sleep(0.2) 
#        tape_pose3 = (0.8858126696200318, -0.18275409741214899, 0.08945171333729662, -0.40731050489460213, 1.07496214001156, -0.782192373678935)
#        rob.movel(tape_pose3, acc=a, vel=v)
#        time.sleep(0.2)
#        tape_pose4 = (0.9020686931764448, -0.1822938590193269, 0.06107965004521791, -0.8083578297668593, 1.9457457746843965, -0.5769271274622322)
#        rob.movel(tape_pose4, acc=a, vel=v)
#        time.sleep(0.2)
#        tape_pose5 = (0.8017662630831749, -0.18167518041220385, 0.05694629821812141, -0.8091184423592992, 1.9474450422504677, -0.576346906759511)
#        rob.movel(tape_pose5, acc=a, vel=v)
#        time.sleep(0.2)    
#        tape_pose6 = (0.7864152530766773, -0.1815534767433731, 0.168173610307256, -0.7830399450935406, 1.8916822719472686, -0.5948086154553289)
#        rob.movel(tape_pose6, acc=a, vel=v)
        
        
#        pose[2] += 0.05
#        rob.movel(old_pose, acc=a, vel=v)
#        print("relative move in base coordinate ")
#        rob.translate((0, 0, -l), acc=a, vel=v)
#        print("relative move back and forth in tool coordinate")
#        rob.translate_tool((0, 0, -0.1), acc=a, vel=v)
#        rob.translate_tool((0, 0, l), acc=a, vel=v)
        
    finally:
        print("Movements Done!")
        rob.close()