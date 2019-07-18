'''

Freeway Simulator 1.0v2 by Nick Peterson

Simulates traffic on a generic freeway.

'''

from graphics import *
import time

#list of all the active vehicles.
active = []

#the number of lanes that the cars are limited to each way
nLanes = 3

#width of a lane.
width = 12

#height of the window.
winHeight = 750

# the inner limit of the lanes
shoulder = Line(Point(nLanes * width, 0), Point(nLanes * width, winHeight))

#Represents a vehicle.
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

        self.p1 = Point(self.x,y)
        self.p2 = Point(self.x+width,y+length)

        self.body = Rectangle(self.p1,self.p2)

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
        if neighbors:
            return True
        else:
            return False

    #returns whether Vehicle has a neighbor on its left (positive x).
    def hasLeftNeighbor(self):
        #need to figure out how to give neighbor for small object
        neighbors = [i for i in active if( (i.x == self.p2.x) and ( (i.y <= self.y <= i.p2.y) or (i.y <= self.p2.y <= i.p2.y) or (self.y <= i.y <= self.p2.y) or (self.y <= i.p2.y <= self.p2.y) ) )]
        if shoulder.p1.x == self.p2.x:
            neighbors.append(shoulder)
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

    #moves the vehicle one lane to the right.
    def moveRight(self):
        if self.x >= 12:
            self.x -= width
            self.p1.x -= width
            self.p2.x -= width
            self.clear()
            self.body.move(-12,0)

    #checks the speed of the car and makes sure it will not collide with anything in front of it.
    def checkSpeed(self):
        if(self.curSpeed / 10 * 15) > self.distanceFromCollision() * 15:

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
        self.cabin = Rectangle(Point(self.p1.x+3,self.p1.y+5),Point(self.p2.x-3,self.p2.y-5))
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
    for i in range(nLanes - 1):
        for j in range(int(winHeight / 10)):
            Line(Point(width * (i + 1), j * 20),Point(width * (i + 1), j * 20 + 10)).draw(win)
    shoulder.draw(win)

    car1 = Vehicle(0,0,20,12,70,70,1,20)
    car2 = Vehicle(0,40,20,12,50,60,1,20)
    car3 = Vehicle(0,80,20,12,60,50,1,20)
    car4 = Vehicle(0,120,20,12,50,40,1,20)
    car5 = Vehicle(0,160,20,12,20,30,1,20)

    for i in range(len(active)):
        active[i].draw(win)

    while car2.y < winHeight:
        refresh(win)

main()