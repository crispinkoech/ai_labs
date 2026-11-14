import Lab1_Agents_Task1_World as World


def MemoryAgent():
    '''
    A memory agent that build on top of the reflex agent. It first
    stores a queue with all the energy blocks (sorted by distance)
    and tracks all the steps it takes in a stack.
    It loops in the following manner:
    - Perceives the distance and angle of the energy block that is
      at the front of the queue
    - Reasons about the distance covered towards this block in the
      previous loop:
      * If the distance covered is less that the desired goal (0.2),
        then add this handle to the back of the queue and backtrack
        to the last point where we collected an energy block
      * Otherwise, if the absolute angle difference between the agent
        and the current energy block > 0.01, then invert left & right
        wheel speeds.
      * Otherwise, if the absolute angle difference is <= 0.01 but
        the distance to the energy block is > 0.5, then set the left
        and right wheel speeds to the same value.
      * Otherwise, set the motor speeds to zero, collect the energy
        block, and remove this block from the queue.
    - Stores the forward step decided (i.e. non-enqueue/rewind steps)
      in memory.
      
    The idea behind this memory design is that, sometimes, the agent
    traps itself in an enclosed maze when going towards a specific
    energy block. If it can walk backwards to a previous arbitrary
    point, then it might be possible for it to move outside of this
    maze and can thus reach otherwise unreachable blocks.
    '''
    robot = World.init()

    # Pre-initialize queue of energy block handles
    blockHandles = getBlockHandles()
    blockHandle = blockHandles.popleft()

    # Memorize each step taken, so that the agent can backtrack in
    # case it determines it is not making progress
    steps = []

    # Track distance of the current energy block to determine if
    # the agent is making progress
    previousDistance = None

    while robot:
        ####################
        # Perception phase #
        ####################
        print(f"Time: {World.getSimulationTime()}")

        if not blockHandle:
            # Nothing more to collect - success?
            print("No more energy blockHandles to collect, shutting down")
            break

        block = findBlock(blockHandle)

        ###################
        # Reasoning phase #
        ###################
        if previousDistance and (previousDistance - block.distance) < 0.2:
            # Not making progress; add to the back of block handles
            # to tackle later
            decision = ("ENQUEUE", blockHandle)
        elif abs(block.direction) > 0.01:
           # Rotate wheels in opposite directions to align with the angle
            # of the nearest energy block
            yawSpeed = block.direction
            motorSpeed = dict(speedLeft=yawSpeed, speedRight=-yawSpeed)
            simulationTime = 500
            decision = ("ROTATE", (motorSpeed, simulationTime))
        elif block.distance > 0.5:
            # Rotate wheels in the same direction towards the nearest
            # energy block
            longSpeed = 1.5
            motorSpeed = dict(speedLeft=longSpeed, speedRight=longSpeed)
            simulationTime = 5_000
            decision = ("MOVE", (motorSpeed, simulationTime))
        else:
            # Likely close to a block; attempt to pick up
            decision = ("COLLECT", blockHandle)

        ################
        # Action phase #
        ################
        action, argument = decision
        match action:
            case "COLLECT":
                World.setMotorSpeeds(dict(speedLeft=0, speedRight=0))
                result = World.collectNearestBlock()
                print(f"Attempt to collect block {blockHandle}: {result}")
                blockHandle = blockHandles.popleft()
                previousDistance = None
            case "ENQUEUE":
                print(f"Not making progress with block {blockHandle}; enqueuing it for later")
                backtrack(steps)
                blockHandles.append(argument)
                blockHandle = blockHandles.popleft()
                previousDistance = None
            case "MOVE":
                print(f"Moving towards block #{blockHandle}")
                previousDistance = block.distance
                World.execute(argument[0], argument[1], -1)
            case "ROTATE":
                print(f"Rotating to face block #{blockHandle}")
                World.execute(argument[0], argument[1], -1)
        if action in ("COLLECT", "MOVE" , "ROTATE"):
            # Store step taken in memory.
            steps.append(decision)


def backtrack(steps):
    print("Backtracking...")
    count = 0
    while steps:
        action, arg = steps.pop()
        if action == "COLLECT":
            print(f"Backtracked {count} steps up to when we collected block #{arg}")
            break
        speed, time = arg
        # Invert the speed direction so as to "rewind" action
        speed = dict(speedLeft=-speed['speedLeft'], speedRight=-speed['speedRight'])
        World.execute(speed, time, -1)
        count += 1


def getBlockHandles():
    from collections import deque
    queue = deque(blockHandles[0] for blockHandles in World.findEnergyBlocks())
    return queue


def findBlock(blockHandle):
    from Lab1_Agents_Task1_World import EasyDict
    for b in World.findEnergyBlocks():
        if b[0] == blockHandle:
            return EasyDict(blockHandle=blockHandle, name=b[1], distance=b[2], direction=b[3])
    return None


if __name__ == '__main__':
    MemoryAgent()