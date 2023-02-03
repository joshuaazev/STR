import time
import sys
from object_handle import ObjectHandle

try:
    import sim
except:
    print('--------------------------------------------------------------')
    print('"sim.py" could not be imported. This means very probably that')
    print('either "sim.py" or the remoteApi library could not be found.')
    print('Make sure both are in the same folder as this file,')
    print('or appropriately adjust the file "sim.py"')
    print('--------------------------------------------------------------')
    print('')

sim.simxFinish(-1)  # just in case, close all opened connections
global clientID
clientID = sim.simxStart('127.0.0.1', 19999, True, True, 5000, 5)
robotname = "youBot"
targetname = 'Target1'


if clientID != -1:
    sim.simxStartSimulation(clientID, sim.simx_opmode_oneshot_wait)
    print('Connected to remote API server')
    sim.simxAddStatusbarMessage(clientID, 'Funcionando...', sim.simx_opmode_oneshot_wait)
    time.sleep(0.02)
    robozinho = ObjectHandle(clientID, robotname) #instancia objeto


    def show_position(object):
        error, [x,y,z] = sim.simxGetObjectPosition(object.clientID, object.robot, -1, sim.simx_opmode_buffer)
        print('Position in x:' + str(x) + ' Position in y:' + str(y) +' Position in z:' + str(z))

    def move_forward(object, v):
        sim.simxPauseCommunication(object.clientID, True)
        sim.simxSetJointTargetVelocity(
            object.clientID, object.rolling_joint_fr, v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(
            object.clientID, object.rolling_joint_rr, v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(
            object.clientID, object.rolling_joint_fl, -v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(
            object.clientID, object.rolling_joint_rl, -v, sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(object.clientID, False)

   
    erro, robozinho.position_robot = sim.simxGetObjectPosition(robozinho.clientID, robozinho.robot, -1, sim.simx_opmode_streaming)
    time.sleep(2)

    while True:
        show_position(robozinho)
        time.sleep(1)
        move_forward(robozinho, 500)
        

else:
    print('Failed connecting to remote API server')
    sys.exit()