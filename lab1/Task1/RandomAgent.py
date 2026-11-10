import random
import Lab1_Agents_Task1_World as World


def RandomAgent():
    '''
    A random agent, that rotates its wheels using random inputs for
    a random amount of time (bounded between 1_000 and 10_000)
    '''
    robot = World.init()
    while robot:
        speedLeft = random.randint(0, 5)
        speedRight = random.randint(0, 5)
        speed = dict(speedLeft=speedLeft, speedRight = speedRight)
        simulationTime = random.randint(1_000, 10_000)
        World.execute(speed, simulationTime, -1)
        World.setMotorSpeeds(dict(speedLeft=0, speedRight=0))
        print(World.collectNearestBlock())


if __name__ == '__main__':
    RandomAgent()
