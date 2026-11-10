import Lab1_Agents_Task1_World as World


def FixedAgent(simulationTime = 10_000):
    '''
    A fixed agent that moves forward for a fixed time, tries to
    collect an energy, and repeats the above steps
    '''
    robot = World.init()
    while robot:
        print(f"Time elapsed: {World.getSimulationTime()}")
        longSpeed = dict(speedLeft=1.5, speedRight=1.5)
        World.execute(longSpeed, simulationTime, -1)
        World.setMotorSpeeds(dict(speedLeft=0, speedRight=0))
        print(World.collectNearestBlock())


if __name__ == '__main__':
    FixedAgent()