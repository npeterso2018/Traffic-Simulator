'''
--------------------------------------------------
|   Toll Booth Simulator by Nick Peterson        |
|                                                |
|   A  demonstration of the Toll Booth's effects |
--------------------------------------------------
'''

from graphics import *
import random

#list of all the active vehicles.
active = []

#list of all the lanes.
lanes = []

#list of all the exits.
exits = []

#list of all the entrances.
entrances = []

#list of all the toll booths.
booths = []

#the number of regular lanes that the Vehicles are limited to each way.
nLanes = 3

#total number of lanes.
nTotalLanes = nLanes

#width of a lane.
width = 16
w = width

#height and width of the window.
winHeight = 750
winWidth = 500

#the inner limit of the lanes.
eLane = Line(Point((nTotalLanes) * width, 0), Point((nTotalLanes) * width, winHeight))

#the outer limit of the lanes.
shoulder = Line(Point(0,0), Point(0,winHeight))

#data and information.
passengers = 0
passengerFlow = 0
carCount = 0
busCount = 0
truckCount = 0
profit = 0

#how many turns in between each data drop.
dataInterval = 10

#speed of the simulation, 1 being the standard.
simSpeed = 1

#speed factor.
factor = 0.25

#represents a vehicle.
class Vehicle:

    #constructs a new vehicle based on a variety of factors. x and y are a point in the top left corner of the vehicle.
    def __init__(self,lane,y,length,width,topSpeed,curSpeed,occupancy,exit):
        self.x = lane * w
        self.y = y
        self.length = length
        self.width = width
        self.topSpeed = topSpeed
        self.curSpeed = curSpeed
        self.occupancy = occupancy
        self.exit = exit
        self.exitMode = False

        self.type = "regular"
        self.paid = []

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
        v = self.closestVehicleFront()
        if v:
            return v.y - self.p2.y
        return 999

    #gets the closest Vehicle in front.
    def closestVehicleFront(self):
        y = [i for i in active if (i.x == self.x) and (i.p1.y > self.p2.y)]
        y.sort()
        if y:
            return y[0]
        return

    #gets the closest Toll Booth in front.
    def closestTollBooth(self):
        y = [i for i in booths if (i.loc + 10 > self.p2.y)]
        y.sort()
        if y == []:
            return
        return y[0]

    #gets the distance of the closest Toll Booth in front.
    def distanceFromTollBooth(self):
        t = self.closestTollBooth()
        if t:
            return t.loc + 10 - self.p2.y
        return 999

    #returns whether Vehicle has a neighbor on its right (negative x).
    def hasRightNeighbor(self):

        global factor

        if exits and self.p1.y >= exits[self.exit].start:
            return False

        neighbors = [i for i in active if( (i.p2.x == self.x)  and ( (i.y <= self.y <= i.p2.y) or (i.y <= self.p2.y <= i.p2.y) or (self.y <= i.y <= self.p2.y) or (self.y <= i.p2.y <= self.p2.y) ) )]

        if exits and (self.exit >= 0) and (exits[self.exit].start - self.p1.y <= (self.curSpeed * factor * (self.p1.x / width))) and not neighbors:
            self.exitMode = True
            return False

        if self.p1.x == 0:
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

        if (self.p2.x <= 0) or (self.p2.x == eLane.p1.x) or not lanes[int(self.p2.x / width)].isPermitted(self):
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
        self.x -= width
        self.p1.x -= width
        self.p2.x -= width
        self.clear()
        self.body.move(-width,0)
        self.cabin.move(-width,0)

    #checks the speed of the car and makes sure it will not collide with anything in front of it.
    def checkSpeed(self):

        global factor
        global profit

        if (self.distanceFromTollBooth() / int(self.curSpeed * factor) < self.curSpeed - (10 * (self.distanceFromTollBooth() / int(self.curSpeed * factor)))) and self.curSpeed > 30:
            self.curSpeed -= 10

        else:
            self.curSpeed = self.topSpeed

        if(self.distanceFromTollBooth() < 10):
            if self.type == "car":
                profit += self.closestTollBooth().toll
            elif self.type == "bus":
                profit += self.closestTollBooth().toll * 4
            else:
                profit += self.closestTollBooth().toll * 5

        if not lanes[int(self.p1.x / 12)].isPermitted(self) and not self.exitMode and not self.hasLeftNeighbor():
            self.moveLeft()

        if(self.curSpeed * 6) > self.distanceFromCollision() * 15:

            if not (self.hasLeftNeighbor()):
                self.moveLeft()
                self.curSpeed = self.topSpeed

            elif not (self.hasRightNeighbor()):
                self.moveRight()
                self.curSpeed = self.topSpeed

            else:
                self.curSpeed = self.closestVehicleFront().curSpeed

    #draws the Vehicle as a red rectangle.
    def draw(self,window):
        #self.body.draw(window)
        #self.body.setOutline("red")
        self.cabin.draw(window)
        self.cabin.setFill("black")

    #moves the Vehicle forward.
    def move(self,factor):

        global profit

        if (self.p1.x == lanes[int(self.p1.x / 12)].type == "pHOV" and self.occupancy < 2 and not (lanes[int(self.p1.x / 12)] in self.paid)):
            self.paid.append(lanes[int(self.p1.x / 12)])
            profit += 1.25
        if exits and (self.exit >= 0) and (exits[self.exit].start - self.p1.y <= self.curSpeed * factor * (self.p1.x / width)) and not self.hasRightNeighbor():
            self.moveRight()
            self.exitMode = True
        if not self.hasRightNeighbor():
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
        elif self.lane == len(lanes) - 1:
            print("True")
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

class pHOV(Lane):

    #constructor.
    def __init__(self,lane):
        self.lane = lane
        self.x = lane * width
        self.type = "pHOV"
        lanes.append(self)

    #draws the lane with a light green shade.
    def draw(self,window):
        super().draw(window)
        rect = Rectangle(Point(self.x+1,0),Point(self.x+(width-1),winHeight)).draw(window)
        rect.setFill("springgreen")
        rect.setOutline("springgreen")

    #determines if the given Vehicle will be permitted into the Lane.
    def isPermitted(self,vehicle):
        if(vehicle.type == "car"):
            return True
        return False

#represents a freeway exit.
class Exit:

    #constructor.
    def __init__(self,y):
        self.start = y
        self.end = y + 60
        exits.append(self)

    #draws the Exit as a hole in the left side.
    def draw(self,window):
        line = Line(Point(0,self.start),Point(0,self.end)).draw(window)
        line.setOutline("white")

#represents a freeway entrance.
class Entrance:

    #constructor.
    def __init__(self,y):
        self.start = y
        self.end = y+60
        entrances.append(self)

    #draws the Entrance as a hole in the left side.
    def draw(self,window):
        line = Line(Point(0,self.start),Point(0,self.end)).draw(window)
        line.setOutline("white")

#represents a toll booth
class TollBooth:

    global width
    global lanes

    #constructor.
    def __init__(self,y,price):
        self.toll = price
        self.loc = y
        booths.append(self)

    #draws the booth.
    def draw(self,window):
        body = Rectangle(Point(0,self.loc),Point(width * len(lanes),self.loc + 20)).draw(window)
        body.setFill("red")

#refreshes the entire scene.
def refresh(window,turn):

    global passengers
    global carCount
    global busCount
    global truckCount
    global simSpeed
    global factor

    toRemove = [i for i in active if((i.p1.y >= 750) or (i.p2.x <= 0))]
    for i in toRemove:
        active.remove(i)
        if i.type == "car":
            carCount += 1
        elif i.type == "bus":
            busCount += 1
        else:
            truckCount += 1
        passengers += i.occupancy
    for i in range(len(active)):
        active[i].clear()
        active[i].move(factor)
        if turn % simSpeed == 0:
            active[i].draw(window)

#produces a Vehicle at the given entrance.
def produce(window,entrance,type,exit):
    if type == "bus":
        Bus(0,entrance.start,exit).draw(window)
    elif type == "truck":
        Truck(0,entrance.start,exit).draw(window)
    else:
        Car(0,entrance.start,random.randint(55,85),45,exit).draw(window)

#main function, puts together all the other functions.
def main():

    #the graphics window to display the simulation.
    win = GraphWin("Toll Demonstration",winWidth,winHeight)

    #shows the lanes of the road.

    for i in range(nLanes):
        Lane(i)

    for lane in lanes:
        print("Created " + lane.type + " at " + str(lane.lane))
        lane.draw(win)
    print(len(lanes))
    booth = TollBooth(winHeight / 2, 1.75)
    eLane.draw(win)
    shoulder.draw(win)
    for ent in entrances:
        ent.draw(win)
    for ex in exits:
        ex.draw(win)
    for b in booths:
        b.draw(win)

    for i in range(nLanes):
        r=random.randint(55,95)
        Car(i,0,r,r,0)

    for i in range(len(active)):
        active[i].draw(win)

    n = 1
    p = 0
    averagePassengerFlow = 0
    Tpassengers = Text(Point(winWidth / (4 / 3), 25), "Passenger count: " + str(passengers))
    TaveragePassengerFlow = Text(Point((winWidth / (4 / 3)) - (len("Passenger count: ") * 3.4), 40),"Passenger flow, updating every " + str(dataInterval) + " turns: " + str(averagePassengerFlow))
    TcarCount = Text(Point((winWidth / (4 / 3)) - (len("Passenger count: ") * 1.7), 55), "Total cars through simulation: " + str(carCount))
    TbusCount = Text(Point((winWidth / (4 / 3)) - (len("Passenger count: ") * 2.1), 70),"Total busses through simulation: " + str(busCount))
    TtruckCount = Text(Point((winWidth / (4 / 3)) - (len("Passenger count: ") * 1.9), 85),"Total trucks through simulation: " + str(truckCount))
    while active[-1].p2.y < winHeight:
        if n % simSpeed == 0:
            Tpassengers = Text(Point(winWidth / (4/3), 25), "Passenger count: " + str(passengers)).draw(win)
            TaveragePassengerFlow = Text(Point((winWidth / (4/3)) - (len("Passenger count: ") * 3.4), 40), "Passenger flow, updating every " + str(dataInterval) + " turns: " + str(averagePassengerFlow)).draw(win)
            TcarCount = Text(Point((winWidth / (4/3)) - (len("Passenger count: ") * 1.7), 55), "Total cars through simulation: " + str(carCount)).draw(win)
            TbusCount = Text(Point((winWidth / (4/3)) - (len("Passenger count: ") * 2.1), 70), "Total busses through simulation: " + str(busCount)).draw(win)
            TtruckCount = Text(Point((winWidth / (4/3)) - (len("Passenger count: ") * 1.9), 85), "Total trucks through simulation: " + str(truckCount)).draw(win)
        if n % 4 == 0:
            for j in range(nLanes):
                c=random.randint(0,10)
                if c == 7:
                    Truck(j,0,0)
                elif c == 4:
                    Bus(j,0,0)
                else:
                    r=random.randint(55,95)
                    Car(j,0,r,r,0)
        refresh(win,n)
        if n % simSpeed == 0:
            Tpassengers.undraw()
            TaveragePassengerFlow.undraw()
            TcarCount.undraw()
            TbusCount.undraw()
            TtruckCount.undraw()

        if n % dataInterval == 0:
            passengerFlow = passengers - p
            try:
                averagePassengerFlow = passengers / (n / dataInterval)

            except ZeroDivisionError:
                averagePassengerFlow = 0

            print("Passenger flow: " + str(passengerFlow) + " passengers have been transported through the simulation since last time, averaging " + str(averagePassengerFlow) + " every " + str(dataInterval) + " turns.")
            print("Passengers transported through the simulation: " + str(passengers) + ".")
            print("")
            print("Number of cars transported through the simulation: " + str(carCount))
            print("Number of busses transported through the simulation: " + str(busCount))
            print("Number of trucks transported through the simulation: " + str(truckCount))

            p = passengers
        n += 1
main()
