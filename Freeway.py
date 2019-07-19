'''

Freeway Simulator 1.0v2 by Nick Peterson

Simulates traffic on a generic freeway.

'''

from graphics import *
import random

#list of all the active vehicles.
active = []

#list of all the lanes.
lanes = []

#the number of lanes that the cars are limited to each way.
nLanes = 3

#the number of HOV lanes to create.
nHOVLanes = 1

#width of a lane.
width = 12

#height of the window.
winHeight = 750

#the inner limit of the lanes
eLane = Line(Point((nLanes + nHOVLanes) * width, 0), Point((nLanes + nHOVLanes) * width, winHeight))

#the outer limit of the lanes
shoulder = Line(Point(0,0), Point(0,winHeight))

#represents a vehicle.
class Vehicle:

    #constructs a new vehicle based on a variety of factors. x and y are a point in the top left corner of the vehicle.
    def __init__(self,lane,y,length,width,topSpeed,curSpeed,occupancy,distance):
        self.x = lane*12
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
        if self.p1.x == 0:
            neighbors.append(eLane)
        if eLane.p1.x == self.p1.x:
            neighbors.append(eLane)
        if neighbors:
            return True
        else:
            return False

    #returns whether Vehicle has a neighbor on its left (positive x).
    def hasLeftNeighbor(self):
        neighbors = [i for i in active if( (i.x == self.p2.x) and ( (i.y <= self.y <= i.p2.y) or (i.y <= self.p2.y <= i.p2.y) or (self.y <= i.y <= self.p2.y) or (self.y <= i.p2.y <= self.p2.y) ) )]
        if shoulder.p1.x == self.p2.x:
            neighbors.append(shoulder)
        if int(self.p2.x / 12) > len(lanes) - 1:
            return True
        if lanes[int(self.p2.x / 12)].lane != len(lanes):
            if lanes[int((self.p2.x / 12))].type == "HOV":
                if ((self.occupancy == 1) or (not self.type == "car")):
                    neighbors.append(lanes[int(self.p2.x / 12)].type)
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
        self.body.move(12,0)
        self.cabin.move(12,0)

    #moves the vehicle one lane to the right.
    def moveRight(self):
        if self.x >= 12:
            self.x -= width
            self.p1.x -= width
            self.p2.x -= width
            self.clear()
            self.body.move(-12,0)
            self.cabin.move(-12,0)

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
        if not self.hasRightNeighbor() and self.x >= 12:
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
        super().__init__(lane,y,20,12,topSpeed,curSpeed,random.randint(1,5),distance)
        self.type = "car"
    def draw(self,window):
        super().draw(window)
        if self.occupancy > 1:
            self.cabin.setFill("green")

#a truck.
class Truck(Vehicle):
    def __init__(self,lane,y,distance):
        super().__init__(lane,y,50,12,65,65,random.randint(1,3),distance)
        self.type = "truck"

#a bus.
class Bus(Vehicle):
    def __init__(self,lane,y,distance):
        super().__init__(lane,y,40,12,70,70,random.randint(20,101),distance)
        self.type = "bus"

#represents a lane.
class Lane:

    #constructor.
    def __init__(self,lane):
        self.lane = lane
        self.x = lane * 12
        self.type = "regular"
        lanes.append(self)

    #draws the lane.
    def draw(self,window):
        if self.lane == 0:
            for i in range(int(winHeight / 10)):
                Line(Point(width * (self.lane + 1), i * 20), Point(width * (self.lane + 1), i * 20 + 10)).draw(window)
        elif self.lane == nLanes:
            return
        else:
            for i in range(int(winHeight / 10)):
                Line(Point(width * (self.lane + 1), i * 20), Point(width * (self.lane + 1), i * 20 + 10)).draw(window)

#represents an HOV lane.
class HOV(Lane):

    #constructor.
    def __init__(self,lane):
        super().__init__(lane)
        self.type = "HOV"

    #draws the lane with a light blue shade.
    def draw(self,window):
        super().draw(window)
        rect = Rectangle(Point(self.x+1,0),Point(self.x+11,winHeight)).draw(window)
        rect.setFill("skyblue")
        rect.setOutline("skyblue")

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

    #shows the lanes of the road
    for i in range(nLanes):
        Lane(i).draw(win)
    for i in range(nLanes,nHOVLanes + nLanes):
        HOV(i).draw(win)
    eLane.draw(win)
    shoulder.draw(win)

    for i in range(nLanes):
        r=random.randint(55,95)
        Car(i,0,r,r,20)

    for i in range(len(active)):
        active[i].draw(win)

    n = 0
    while active[-1].p2.y < winHeight:
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
        n += 1

main()