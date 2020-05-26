"""PhiPy module - physics calculation functions

Users can calculate basic classic mechanical and electromagnetism calculations
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import constants 
import space   

def VectorAddition(v,u):
    """Add two vectors each other.

    Returns a Vector 
    
    Attributes
    ----------
    v: Vector
        First vector for addition
    u: Vector
        Second vector for addition
    """
    return List2Vector(u.xyz()+v.xyz())
def RelativeVector(v,u):
    """Return a Vector which vector u relative to vector v (u-x)

    Attrributes
    -----------
    v: Vector
        First vector 
    u: Vector
        Second vector 
    """
    return List2Vector(u.xyz()-v.xyz())
def MultiVectorAddition(VectorList):
    """Sum all vectors in a list and return a vector

    Attrributes
    -----------
    VectorList: list
        A list that contains Vectors
    """
    m = []
    for mva in range(len(VectorList)):
        m.append(VectorList[mva].xyz())
    return Vector(sum(m)[0],sum(m)[1],sum(m)[2])
def List2Vector(VectorList):
    """Convert numpy array that contains 3 int elements  to Vector
    
    Attributes
    ----------
    VectorList: numpy array
        numpy array which has 3 int elements.
    """ 
    return Vector(VectorList[0],VectorList[1],VectorList[2])
def Angle(v,u):
    """Find an angle between two Vectors.

    Attributes
    ----------
    u: Vector
        First Vector
    v: Vector
        Second Vector
    """
    return math.acos((v.x*u.x + v.y*u.y + v.z*u.z)/(v.magnitude*u.magnitude))
def DotProduct(v,u):
    """Dot product of two vectors

    Returns int

    Attributes
    ----------
    v: Vector
        First Vector
    u: Vector
        Second Vector
    """
    return v.x*u.x + v.y*u.y + v.z*u.z
def CrossProduct(v,u):
    """Cross product of two vectors

    Returns Vector

    Attributes
    ----------
    v: Vector
        First Vector
    u: Vector
        Second Vector
    """
    x = v.y*u.z - v.z*u.y
    y = -v.x*u.z + v.z*u.x
    z = v.x*u.y - v.y*u.x
    return Vector(x,y,z)
def Projection(v,u):
    """Projection of first vector to second vector

    Returns Vector

    Attributes
    ----------
    v: Vector
        First Vector
    u: Vector
        Second Vector
    """
    s = DotProduct(v,u)/(u.magnitude**2)
    return Vector(u.x*s,u.y*s,u.z*s)
def Volume(v,u,w):
    """Calculate volume of solid created by three vectors.

    Returns int

    Attributes
    ----------
    v: Vector
        First Vector
    u: Vector
        Second Vector
    w: Vector
        Third Vector
    """
    return abs(DotProduct(CrossProduct(v,u), w))
def DistanceB2Object(FirstObject,SecondObject):
    """Calculate distance between two objects.

    Position of second object - position of first object. Returns Vector.

    Attributes
    ----------
    FirstObject: Object
        First object
    SecondObject: Object
        Second object
    """
    return List2Vector(SecondObject.Position.xyz()-FirstObject.Position.xyz())   
def Work(ForceVector,DisplacementVector):
    """Calculate the work done by a force that displace the object a distance.

    Returns Vector

    Attributes
    ----------
    ForceVector: Vector
        Applied force on the object
    DisplacementVector: Vector
        Displacement of the object
    """
    return DotProduct(ForceVector,DisplacementVector)
def GravitationalForce(FirstObject,SecondObject):
    """Calculate the gravitational force act on second object applied by first object

    Returns Vector

    Attributes
    ----------
    FirstObject: Object
        First object
    SecondObject: Object
        Second object
    """
    gF = constants.G.Value * FirstObject.Mass * SecondObject.Mass / (DistanceB2Object(FirstObject,SecondObject).magnitude)**2

    vector = List2Vector(gF * DistanceB2Object(SecondObject,FirstObject).unitVector().xyz())

    return vector
def ElasticCollision(Object1,Object2):
    """Calculate final velocities of two object after an elastic collision 
    
    Returns Vector,Vector

    Attributes
    ----------
    Object1: Object
        First object of an elactic collision
    Object2: Object
        Second object of an elastic collision
    """
    RlV = List2Vector(-1*RelativeVector(Object2.Velocity,Object1.Velocity).xyz())
    IMom = List2Vector(Object1.Momentum.xyz()+Object2.Momentum.xyz())
    
    O2fV = List2Vector(IMom.xyz()+RlV.xyz()*Object1.Mass/(Object1.Mass+Object2.Mass))
    O1fV = List2Vector(O2fV.xyz()-RlV.xyz())
    return O1fV,O2fV
def CoulombsLaw(charge1,charge2):
    """Calculate electric force act on second charge applied by first charge 
    
    Returns Vector

    Attributes
    ----------
    charge1: Charge
        First charge
    charge2: Charge
        Second Charge
    """
    F = constants.k.Value * charge1.charge * charge2.charge / RelativeVector(charge1.position,charge2.position).magnitude**2
    vector = List2Vector(F * RelativeVector(charge2.position,charge1.position).unitVector().xyz())
    return vector
def EField(charge,point):
    """Calculate electric field caused by a charge at a point
    
    Returns Vector

    charge: Charge
        Charge that cause electric field
    point: Vector
        Point in a 3-D space to calculate electric field
    """
    E = constants.k.Value * charge.charge / RelativeVector(charge.position,point).magnitude**2
    vector = List2Vector(E*RelativeVector(point,charge.position).unitVector().xyz())
    return vector
def DipoleMoment(NegativeCharge,PositiveCharge):
    """Calculate the dipole moment of two charges

    Returns Vector

    Attribute
    ---------
    NegativeCharge: Charge
        Negative charge
    PositiveCharge: Charge
        Positive charge
    """
    return List2Vector(PositiveCharge.charge * RelativeVector(PositiveCharge.position,NegativeCharge.position).xyz())
#def DipoleMomentEField(DipoleMoment,Point):
    #return constants.k.Value * -1 * DipoleMoment.xyz() / RelativeVector(Point,DipoleMoment.position).magnitude**3
def DipoleMomentTorque(DipoleMoment,EField):
    """Calculates components of torque of an dipole in an electric field and return a vector.

    Attributes
    ----------
    DipoleMoment: Vector
        Dipole moment of an dipole
    EField: Vector
        External electric field
    """
    return CrossProduct(DipoleMoment,EField)
def DipoleMomentPotential(DipoleMoment,EField):
    """Calculates dipole moment potential energy of an dipole in an electric field.

    Returns int

    Attributes
    ----------
    DipoleMoment: Vector
        Dipole moment of an dipole
    EField: Vector
        External electric field
    """
    return -1*DotProduct(DipoleMoment,EField)
def EPotential(Charge,Point):
    """Calculates electric potential energy of an charge at a point.

    Returns int

    Attributes
    ----------
    Charge: Charge
        A charge
    Point: Vector
        Point in a 3-D space
    """
    return constants.k.Value * Charge.charge / RelativeVector(Charge.position,Point).magnitude
def EPotential2Charge(Charge1,Charge2):
    """Calculate potential energy that created by two charges

    Returns int

    Attribute
    ---------
    Charge1: Charge
        First charge
    Charge2: Charge
        Second charge
    """
    return constants.k.Value * Charge1.charge * Charge2.charge/ RelativeVector(Charge1.position,Charge2.position).magnitude
def CParallel(capacitor1,capacitor2):
    """Connect two capacitor in parallel

    Returns PPCapacitor

    Attributes
    ----------
    capacitor1: PPCapacitor
        First capacitor
    capacitor2: PPCapacitor
        Second capacitor
    """
    return PPCapacitor(capacitor1.capacitance+capacitor2.capacitance)
def CSeries(capacitor1,capacitor2):
    """Connect two capacitor in series

    Returns PPCapacitor

    Attributes
    ----------
    capacitor1: PPCapacitor
        First capacitor
    capacitor2: PPCapacitor
        Second capacitor
    """
    sc = (1/capacitor1.capacitance)+(1/capacitor2.capacitance)
    ceq = 1/sc
    return PPCapacitor(ceq)
def RParallel(resistor1,resistor2):
    """Connect two resistor in parallel

    Returns Resistor

    Attributes
    ----------
    resistor1: Resistor
        First resistor
    resistor1: Resistor
        Second resistor
    """
    sr = (1/resistor1.resistance)+(1/resistor2.resistance)
    req = 1/sr
    return Resistor(req)
def RSeries(resistor1,resistor2):
    """Connect two resistor in series

    Returns Resistor

    Attributes
    ----------
    resistor1: Resistor
        First resistor
    resistor2: Resistor
        Second resistor
    """
    return Resistor(resistor1.resistance+resistor2.resistance)

class Vector:
    """Create a Vector

    Create a Vector in 3-D. 

    Attributes
    ----------
    x: int
        x component of the vector
    y: int 
        y compononet of the vector
    z: int
        z component of the vector
    magnitude: int
        magnitude of the vector
    components: tuple
        components of the vector
    """
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        self.magnitude = math.sqrt((x**2)+(y**2)+(z**2))
        self.components = x,y,z

    def xyz(self):
        """Return numpy array of x, y and z component of the vector """
        return np.array([self.x,self.y,self.z])
    def unitVector(self):
        """A Vector. Return unit vector of the vector."""
        return List2Vector(np.array([self.x,self.y,self.z])/self.magnitude)
class Space:
    """Create a Space

    Attributes
    ----------
    Gravity: Vector
        A vector. Gravity of the space.
    """
    def __init__(self,Gravity):
        self.Gravity = Vector(0,0,-Gravity)
class Object:
    """It creates an object.
    
    This class create an object in a space with mass and moment of inertia at a position. 
    . . .

    Attributes
    ----------
    Space: Space
        Space
    Mass: int
        Mass of the object
    MomentOfInertia: int
        Moment of inertia of the object
    Position: Vector
        Position of the object
    Radius: int
        Radius of the object.
    Forces: list
        All applied forces on the object. Initially the gravitational force is included.
    Velocity: Vector
        Initial velocity of the object
    AngularVelocity: Vector
        Angular velocity of the object
    GravityPotentialEnergy: int
        Gravitational Potential Energy of the object
    NetForce: Vector
        Net force that applied on the object
    Acceleration: Vector
        Acceleration of the object
    
    """
    def __init__(self,Space,Mass,MomentOfInertia,Position):
        self.Space = Space 
        self.Mass = Mass
        self.MomentOfInertia = MomentOfInertia
        self.Position = Position
        self.Radius = math.sqrt(self.MomentOfInertia / self.Mass)
        self.Forces = [List2Vector(self.Mass * self.Space.Gravity.xyz())] 
        self.ForceDistances = []
        self.Torques = []
        self.Velocity = Vector(0,0,0)
        self.AngularVelocity = List2Vector(self.Radius * self.Velocity.xyz())
        self.Momentum = List2Vector(self.Mass * self.Velocity.xyz())
        self.LinearKineticEnergy = 0.5 * self.Mass * self.Velocity.magnitude ** 2 
        self.AngularKineticEnergy = 0.5 * self.MomentOfInertia * self.AngularVelocity.magnitude
        self.GravityPotentialEnergy = self.Mass * self.Space.Gravity.magnitude * self.Position.z
        self.NetForce = MultiVectorAddition(self.Forces)
        self.NetTorque = Vector(0,0,0)
        self.Acceleration = List2Vector(self.NetForce.xyz()/self.Mass)
        
    def Add(self,VectorType,Vector,DVector=None):
        """Add a Vector to the object.
        
        ...

        Attributes
        ----------
        VectorType: str
            Type of the adding Vector. 'force' or 'velocity'. 
        Vector: Vector
            A vector which will be added to the object
        DVector: Vector
            A vector which is the position vector of added force. (Default None)
        """
        if str(VectorType) == "force":
            self.Forces.append(Vector)
            self.ForceDistances.append(DVector)
            self.Torques.append(CrossProduct(DVector,Vector))
        elif str(VectorType) == "velocity":
            self.Velocity = Vector
        
        self.NetForce = MultiVectorAddition(self.Forces)
        self.Acceleration = List2Vector(self.NetForce.xyz()/self.Mass)
        self.NetTorque = MultiVectorAddition(self.Torques)
        self.AngularVelocity = List2Vector(self.Radius * self.Velocity.xyz())
        self.Momentum = List2Vector(self.Mass * self.Velocity.xyz())
        self.LinearKineticEnergy = 0.5 * self.Mass * self.Velocity.magnitude
        self.AngularKineticEnergy = 0.5 * self.MomentOfInertia * self.AngularVelocity.magnitude

    def DeleteList(self,VectorList):
        """Delete all elements in a list of the object
            
        This function delete all elements in a list.

        ...

        Attributes
        ----------
        VectorList: list
            Only 'force'
        """
        if str(VectorList) == "force":
            self.Forces.clear()
    def Future(self,Type,Time):
        """Calculate future attributes

        This function calculate future velocity or position of the object at a specific time.

        Attributes
        ----------
        Type: str
            'velocity' or 'position'
        Time: int
            Time that the function calculate velocity or position of the object, in second.
        """
        if str(Type) == "velocity":
            return List2Vector(self.Velocity.xyz() + self.Acceleration.xyz()*Time)
        elif str(Type) == "position":
            return List2Vector(self.Position.xyz() + self.Velocity.xyz()*Time + 0.5 * self.Acceleration.xyz() * Time* Time)
class Charge:
    """Create a charge

    Attributes
    ----------
    charge: int
        charge value of the Charge
    position: Vector
        position of the charge
    """
    def __init__(self,charge,position):
        self.charge = charge
        self.position = position
class Spring:
    """Create a spring

    A simple pendulum that have one or two objects (default 1 object)

    Attributes
    ----------
    SpringConstant: int
        spring constant of the spring (k)
    FirstObject: Object
        An object 
    SecondObject: Object
        default position (0,0,0)
    """
    def __init__(self,SpringConstant,FirstObject,SecondObject=Object(Space(10),1,1,Vector(0,0,0))):
        self.SpringConstant=SpringConstant
        self.FirstObject = FirstObject
        self.SecondObject = SecondObject
        self.Potential = 0

    def Compress(self,FirstObjectFinalPosition,SecondObjectFinalPosition=Vector(0,0,0)):
        """Compress spring

        Returns int. Calculate the potential after compress.

        Attributes
        ----------
        FirstObjectFinalPosition: Vector
            Final position of the first object
        SecondObjectFinalPosition: Vector
            Final position of the first object (default (0,0,0))
        """
        self.Potential =  0.5 * self.SpringConstant * List2Vector(RelativeVector(FirstObjectFinalPosition,self.FirstObject.Position).xyz()-RelativeVector(SecondObjectFinalPosition,self.SecondObject.Position).xyz() ).magnitude**2       
class Pendulum:
    """Create a pendulum

    Calculate Period

    Attributes
    ----------
    Object: Object
        An object
    RopeLength: int
        Length of the rope
    Period: int
        Period of the pendulum
    """
    def __init__(self,Object,RopeLength):
        self.Object = Object
        self.RopeLength = RopeLength
        self.Period = 2* math.pi * np.sqrt(self.RopeLength/self.Object.Space.Gravity.magnitude)
class ParallelPlate:
    """Create a parallel plate

    Calculate the capacitance

    Attributes
    ----------
    epsilon: int
        epsilon
    area: int
        area of the plates
    distance: int
        distance between the plates
    capacitance: int
        capacitance of the parallel plates
    """
    def __init__(self,epsilon,area,distance):
        self.epsilon = epsilon
        self.area = area
        self.distance = distance
        self.capacitance = self.epsilon * self.area / self.distance
class PPCapacitor:
    """Create a parallel plate capacitor

    Attributes
    ----------
    capacitance: int
        capacitance of the capacitor
    voltage: int
        voltage of the capacitor (default None)
    charge: int
        charges that passes on the capacitor (default None)
    """
    def __init__(self,capacitance,voltage=None,charge=None):
        self.capacitance = capacitance
        self.voltage = voltage
        self.charge = charge      
class Resistor:
    """Create a resistor

    Attributes
    ----------
    resistance: int
        resistance of the resitor
    voltage: int
        voltage of the resitor (default None)
    current: int
        current that passes on the resistor (default None)
    """
    def __init__(self,resistance,voltage=None,current=None):
        self.resistance = resistance
        self.voltage = voltage
        self.current = current

