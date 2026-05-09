from engine.bodies import Body
from engine.constants import *
from engine.vectors import Vector

if __name__ == "__main__":
    VELOCITY = Vector()
    ball1 = Body(100, Vector(), VELOCITY)
    ball2 = Body(10, Vector(), Vector(10,0,0)) 
    
    ENGINE = Engine()
    ENGINE.addBody(ball1)
    ENGINE.addBody(ball2)
    ENGINE.applyGravity()
    
    for _ in range(1,10):
        ENGINE.update(1)
        for body in ENGINE.bodies:
            print(body.pos, end=" ")
        print()