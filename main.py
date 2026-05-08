from engine.bodies import Body
from engine.constants import *
from engine.vectors import Vector

if __name__ == "__main__":
    pos = Vector(3,4,0)
    force = Vector(1,0,0)
    BODY = Body(1, pos)
    
    print("Initial: ", BODY.vel)
    BODY.impulse(force, 2)
    print("AFTER: ", BODY.vel)