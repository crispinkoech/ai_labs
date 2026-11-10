import Lab1_Agents_Task1_World as World

def ReflexAgent():
    '''
    A reflex agent that:
    - Perceives the distance and angle to the nearest energy block
    - Reasons about the ideal motor speed based on distance/angle:
      * Inverse left/right speed if absolute angle difference > 0.001pi
      * Same left/right speed if absolute angle difference <= 0.001pi
        but distance is > 0.3
      * 0 speed on left/right otherwise
    - Acts based on the derived motor speeds.
    '''
    robot = World.init()
    while robot:
        ####################
        # Perception phase #
        ####################
        timeElapsed = World.getSimulationTime()
        print(f"Time elapsed: {timeElapsed}")
        block = World.getSensorReading("energySensor")
        
        ###################
        # Reasoning phase #
        ###################
        if abs(block.direction) > 0.001:
            # Rotate wheels in opposite directions to align with the angle
            # of the nearest energy block
            yawSpeed = block.direction
            simulationTime = 500
            motorSpeed = dict(speedLeft=yawSpeed, speedRight=-yawSpeed)
        elif block.distance > 0.3:
            # Rotate wheels in the same direction towards the nearest
            # energy block
            longSpeed = 1.5
            simulationTime = 5000
            motorSpeed = dict(speedLeft=longSpeed, speedRight=longSpeed)
        else:
            # Do not move/rotate.
            motorSpeed = None
            
        ################
        # Action phase #
        ################
        if motorSpeed:
            # Move robot
            World.execute(motorSpeed, simulationTime, -1)
        else:
            # Try to collect energy block
            World.setMotorSpeeds(dict(speedLeft=0, speedRight=0))
            result = World.collectNearestBlock()
            print(result)


if __name__ == '__main__':
    ReflexAgent()
        