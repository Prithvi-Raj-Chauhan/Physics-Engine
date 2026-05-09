import math

class Vector:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x,y,z

    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y, self.z+other.z)

    def dot(self, other):
        return (self.x*other.x)+(self.y*other.y)+(self.z*other.z)
    
    def mag(self):
        return math.sqrt(self.x**2+self.y**2+self.z**2)
    
    def __mul__(self, scalar: int|float):
        return Vector(self.x*scalar, self.y*scalar, self.z*scalar)
    
    def __rmul__(self, scalar: int|float):
        return Vector(self.x*scalar, self.y*scalar, self.z*scalar)

    def __repr__(self):
        return f"{(self.x, self.y, self.z)}"


if __name__=="__main__":
    A = Vector(2,3)
    B = Vector(1,0,2)
    print(A+B)
    print(A*3)
    print(-1*A)