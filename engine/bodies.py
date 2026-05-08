from .vectors import Vector

class Body:
    def __init__(self, mass: float, pos: Vector, vel=Vector()):
        """
        mass -> Mass of the body in kgs
        Position and velocity as a vector
        """
        
        self.pos = pos 
        self.mass = mass
        self.acc = Vector()
        self.vel = vel
        self.momentum = self.mass*self.vel
    
    def __repr__(self):
        return f"Mass: {self.mass}\nPosition: {self.pos}\nAcceleration: {self.acc}\nVelocity: {self.vel}"
    
    def applyforce(self, force: Vector):
        self.acc = self.acc+(force*(1/self.mass))
        
    def releaseForce(self):
        self.applyforce(Vector())
        
    def impulse(self,force: Vector, time):
        self.applyforce(force)
        self.update(time)
        self.releaseForce()
        
    def update(self, time):
        """
        JAAN of the BODIES. Updates all the the attributes of the body..
        """
        time = time
        self.pos+=((self.vel*time)+0.5*(self.acc)*time*time)
        self.vel+=(self.acc*time)
        self.momentum = self.mass*self.vel
        
if __name__ == '__main__':
    F = Vector(x=10)
    
    print("Before Force: ")
    A = Body(10, Vector(1,1))
    print(A)
    
    A.applyforce(F)
    A.update(1)
    
    print("\nAfter Force")
    print(A)