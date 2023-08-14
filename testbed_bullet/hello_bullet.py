import pybullet as p
import time
import pybullet_data
physicsClient = p.connect(p.GUI)#or p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally
p.setGravity(0,0,-10)
planeId = p.loadURDF("plane.urdf")
cubeStartPos = [0,0,0]
cubeStartOrientation = p.getQuaternionFromEuler([0,0,0])
robotId = p.loadURDF("testbed_bullet/testbed_bullet.urdf",cubeStartPos, cubeStartOrientation, 
                   # useMaximalCoordinates=1, ## New feature in Pybullet
                   flags=p.URDF_USE_INERTIA_FROM_FILE)

# Find the joint index for "Revolute_1"
jointIndex = -1
for i in range(p.getNumJoints(robotId)):
    if p.getJointInfo(robotId, i)[1].decode('UTF-8') == "Revolute_1":
        jointIndex = i
        break
if jointIndex == -1:
    print("Joint 'Revolute_1' not found!")

else:
    # Add a constraint to lock the base in place
    basePosition, baseOrientation = p.getBasePositionAndOrientation(robotId)
    p.setJointMotorControl2(robotId, jointIndex, p.VELOCITY_CONTROL, force=0)
    # Create a constraint to lock the base in place
    p.createConstraint(robotId, -1, -1, -1, p.JOINT_FIXED, [0, 0, 0], [0, 0, 0], basePosition, baseOrientation)

    targetTorque = 1# Experiment with this value
    for i in range(10000):
        # targetTorque += 100
        p.setJointMotorControl2(robotId, jointIndex, p.TORQUE_CONTROL, force=targetTorque)
        p.stepSimulation()
        time.sleep(1./400.)


cubePos, cubeOrn = p.getBasePositionAndOrientation(robotId)
print(cubePos,cubeOrn)
p.disconnect()

