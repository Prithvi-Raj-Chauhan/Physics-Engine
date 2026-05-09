from .vectors import Vector
from .bodies import Body
from .constants import *

class Engine:
    def __init__(self):
        self.bodies : list[Body]=[]

    def addBody(self, body: Body):
        self.bodies.append(body)

    def applyGravity(self):
        for body in self.bodies:
            body.applyforce(gr*body.mass)            
            
    def update(self, dt):
        for body in self.bodies:
            body.update(dt)

if __name__ == "__main__":
    VELOCITY = Vector(30,40,0)
    ball = Body(10, Vector(), VELOCITY) # the ball
    
    ENGINE = Engine()
    Engine.addBody(ball)
    Engine.applyGravity()
    
    for body in ENGINE.bodies:
        print(body.pos)