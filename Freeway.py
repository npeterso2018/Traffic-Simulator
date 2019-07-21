'''

---------------------------------------------
|   Freeway Simulator by Nick Peterson      |
|                                           |
|   Simulates traffic on a generic freeway. |
---------------------------------------------

'''

from graphics import *
import random

#list of all the active vehicles.
active = []

#list of all the lanes.
lanes = []

#the number of regular lanes that the Vehicles are limited to each way.
nLanes = 2

#the number of HOV lanes to create.
nHOVLanes = 1

#the number of LV lanes to create.
nLVLanes = 2

#the number of BUS lanes to create.
nBUSLanes = 1

#width of a lane.
width = 12
w = width

#height of the window.
winHeight = 750

#the inner limit of the lanes
eLane = Line(Point((nLanes + nHOVLanes + nLVLanes + nBUSLanes) * width, 0), Point((nLanes + nHOVLanes + nLVLanes + nBUSLanes) * width, winHeight))

#the outer limit of the lanes
shoulder = Line(Point(0,0), Point(0,winHeight))

#represents a vehicle.
class Vehicle:

    #constructs a new vehicle based on a variety of factors. x and y are a point in the top left corner of the vehicle.
    def __init__(self,lane,y,length,width,topSpeed,curSpeed,occupancy,distance):
        self.x = lane * w
        self.y = y
        self.length = length
        self.width = width
        self.topSpeed = topSpeed
        self.curSpeed = curSpeed
        self.occupancy = occupancy
        self.distance = distance

        self.type = "regular"

        self.p1 = Point(self.x,y)
        self.p2 = Point(self.x+width,y+length)

        self.body = Rectangle(self.p1,self.p2)

        self.cabin = Rectangle(Point(self.p1.x + 3, self.p1.y + 5), Point(self.p2.x - 3, self.p2.y - 5))

        active.append(self)

    #less than override.
    def __lt__(self, other):
        return self.y < other.y

    #gets the y coordinate of the closest Vehicle in front.
    def distanceFromCollision(self):
        y = [i for i in active if (i.x == self.x) and (i.y > self.y)]
        y.sort()
        if y == []:
            return 999
        return(y[0].y - (self.y + self.length))

    #gets the closest Vehicle in front.
    def closestVehicleFront(self):
        y = [i for i in active if (i.x == self.x) and (i.y > self.y)]
        y.sort()
        if y:
            return y[0]

    #returns whether Vehicle has a neighbor on its right (negative x).
    def hasRightNeighbor(self):
        neighbors = [i for i in active if( (i.p2.x == self.x)  and ( (i.y <= self.y <= i.p2.y) or (i.y <= self.p2.y <= i.p2.y) or (self.y <= i.y <= self.p2.y) or (self.y <= i.p2.y <= self.p2.y) ) )]

        if (int(self.p1.x / width)) == 0:
            return True

        if not lanes[int(self.p1.x / width) - 1].isPermitted(self):
            return True

        if neighbors:
            return True
        else:
            return False

    #returns whether Vehicle has a neighbor on its left (positive x).
    def hasLeftNeighbor(self):
        neighbors = [i for i in active if( (i.x == self.p2.x) and ( (i.y <= self.y <= i.p2.y) or (i.y <= self.p2.y <= i.p2.y) or (self.y <= i.y <= self.p2.y) or (self.y <= i.p2.y <= self.p2.y) ) )]

        if (int(self.p2.x / width)) == len(lanes):
            return True

        if not lanes[int(self.p2.x / width)].isPermitted(self):
            return True

        if neighbors:
            return True

        else:
            return False

    #clears the graphical representation of the Vehicle.
    def clear(self):
        self.body.undraw()
        self.cabin.undraw()

    #moves the vehicle one lane to the left.
    def moveLeft(self):
        self.x += width
        self.p1.x += width
        self.p2.x += width
        self.clear()
        self.body.move(width,0)
        self.cabin.move(width,0)

    #moves the vehicle one lane to the right.
    def moveRight(self):
        if self.x >= width:
            self.x -= width
            self.p1.x -= width
            self.p2.x -= width
            self.clear()
            self.body.move(-width,0)
            self.cabin.move(-width,0)

    #checks the speed of the car and makes sure it will not collide with anything in front of it.
    def checkSpeed(self):
        if(self.curSpeed * 6) > self.distanceFromCollision() * 15:

            if not (self.hasLeftNeighbor()):
                self.moveLeft()
                self.curSpeed = self.topSpeed
                return False

            if not (self.hasRightNeighbor()):
                self.moveRight()
                self.curSpeed = self.topSpeed
                return False
            self.curSpeed = self.closestVehicleFront().curSpeed
            return True

    #draws the Vehicle as a red rectangle.
    def draw(self,window):
        #self.body.draw(window)
        #self.body.setOutline("red")
        self.cabin.draw(window)
        self.cabin.setFill("black")

    #moves the Vehicle forward.
    def move(self,factor):
        if not self.hasRightNeighbor() and self.x >= width:
            self.moveRight()
        self.checkSpeed()
        if(self.curSpeed / 10 * 15) > self.distanceFromCollision() * 15:
            self.curSpeed = self.closestVehicleFront().curSpeed
        self.y += self.curSpeed * factor
        self.p1.y += self.curSpeed * factor
        self.p2.y += self.curSpeed * factor
        self.body.move(0,self.curSpeed * factor)
        self.cabin.move(0,self.curSpeed * factor)

#a car.
class Car(Vehicle):
    def __init__(self,lane,y,topSpeed,curSpeed,distance):
        super().__init__(lane,y,20,width,topSpeed,curSpeed,random.randint(1,5),distance)
        self.type = "car"
    def draw(self,window):
        super().draw(window)
        if self.occupancy > 1:
            self.cabin.setFill("green")

#a truck.
class Truck(Vehicle):
    def __init__(self,lane,y,distance):
        super().__init__(lane,y,50,width,65,65,random.randint(1,3),distance)
        self.type = "truck"

#a bus.
class Bus(Vehicle):
    def __init__(self,lane,y,distance):
        super().__init__(lane,y,40,width,70,70,random.randint(20,101),distance)
        self.type = "bus"

#represents a lane.
class Lane:

    #constructor.
    def __init__(self,lane):
        self.lane = lane
        self.x = lane * width
        self.type = "regular"
        lanes.append(self)

    #draws the lane.
    def draw(self,window):
        if self.lane == 0:
            for i in range(int(winHeight / 10)):
                Line(Point(width * (self.lane + 1), i * 20), Point(width * (self.lane + 1), i * 20 + 10)).draw(window)
        elif self.lane == len(lanes):
            return
        else:
            for i in range(int(winHeight / 10)):
                Line(Point(width * (self.lane + 1), i * 20), Point(width * (self.lane + 1), i * 20 + 10)).draw(window)

    #generic function to determine if the given Vehicle will be permitted into the lane.
    def isPermitted(self,vehicle):
        return True

#represents an HOV lane.
class HOV(Lane):

    #constructor.
    def __init__(self,lane):
        self.lane = lane
        self.x = lane * width
        self.type = "HOV"
        lanes.append(self)

    #draws the lane with a light blue shade.
    def draw(self,window):
        super().draw(window)
        rect = Rectangle(Point(self.x+1,0),Point(self.x+(width-1),winHeight)).draw(window)
        rect.setFill("skyblue")
        rect.setOutline("skyblue")

    #determines if the given Vehicle will be permitted into the Lane.
    def isPermitted(self,vehicle):
        if (vehicle.occupancy >= 2) and (vehicle.type == "car"):
            return True
        return False

#represents a Large Vehicle lane.
class LV(Lane):

    #constructor.
    def __init__(self,lane):
        super().__init__(lane)
        self.type = "LV"

    #draws the lane with a light red shade.
    def draw(self,window):
        super().draw(window)
        rect = Rectangle(Point(self.x + 1, 0), Point(self.x + (width-1), winHeight)).draw(window)
        rect.setFill("salmon")
        rect.setOutline("salmon")

    #determines if the given Vehicle will be permitted into the Lane.
    def isPermitted(self,vehicle):
        if vehicle.length >= 40:
            return True
        return False

#represents a Bus lane.
class BUS(Lane):

    #constructor.
    def __init__(self,lane):
        super().__init__(lane)
        self.type = "BUS"

    #draws the lane with a mild yellow shade.
    def draw(self,window):
        super().draw(window)
        rect = Rectangle(Point(self.x + 1, 0), Point(self.x + (width-1), winHeight)).draw(window)
        rect.setFill("blanchedalmond")
        rect.setOutline("blanchedalmond")

    #determines if the given Vehicle will be permitted into the Lane.
    def isPermitted(self,vehicle):
        if vehicle.type == "bus":
            return True
        return False

#refreshes the entire scene.
def refresh(window):
    for i in range(len(active)):
        active[i].clear()
        active[i].move(0.25)
        active[i].draw(window)

#main function, puts together all the other functions.
def main():

    #the graphics window to display the simulation.
    win = GraphWin("I-95",500,winHeight)

    lanesTotal = 0

    #shows the lanes of the road
    for i in range(nBUSLanes):
        BUS(i).draw(win)
        lanesTotal += 1
    for i in range(lanesTotal, lanesTotal + nLVLanes):
        LV(i).draw(win)
        lanesTotal += 1
    for i in range(lanesTotal, nLanes + lanesTotal):
        Lane(i).draw(win)
        lanesTotal += 1
    for i in range(lanesTotal,nHOVLanes + lanesTotal):
        HOV(i).draw(win)
        lanesTotal += 1
    for i in range(len(lanes)):
        print(lanes[i].type + " at " + str(lanes[i].lane))
    eLane.draw(win)
    shoulder.draw(win)
    Car(3,0,90,90,20)
    t = Truck(1,80,20)
    Truck(3, 120, 20)
    Truck(4, 160, 20)
    Truck(5, 200, 20)
    s = Truck(3, 0, 20)
    Bus(3,220,20)
    s.curSpeed = 120
    s.topSpeed = 120

    """for i in range(nLanes):
        r=random.randint(55,95)
        Car(i,0,r,r,20)"""

    for i in range(len(active)):
        active[i].draw(win)

    while t.p2.y < winHeight:
        refresh(win)

    n = 0
    """while active[-1].p2.y < winHeight:
        if n % 4 == 0:
            for j in range(nLanes):
                c=random.randint(0,10)
                if c == 9:
                    Truck(j,0,20)
                elif c == (4 or 5):
                    Bus(j,0,20)
                else:
                    r=random.randint(55,95)
                    Car(j,0,r,r,20)
        refresh(win)
        n += 1"""

main()