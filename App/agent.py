import agentpy as ap
#visualizations
from random import randint
import CircularDLinkedList
import json

ENTRIES_INDEXES = [3, 16, 11, 24]
EXITS_INDEXES = [1, 12, 15, 26]
SPAWNS = [(18,1),(33,18) ,(1, 16), (16,33)]

carPositions = {
    "nCars" : 0,
    "carPositions" : []
}

class CAR(ap.Agent):
    def setup(self):
        pass

    def agent_method(self):
        pass

class StreetModel(ap.Model):

    def makeCircle(self,startX,startY,r):
        map = []
        Epsilon = 2.2
        for y in range(startX-r,startX+r+1):
            for x in range(startY-r,startY+r+1):
                if abs((x-startX)**2 + (y-startY)**2 - r**2) < Epsilon**2:
                    map.append((x,y))
        return map

    def setup(self):
        # Create grid (street)
        self.CarJson =[]
        self.street = ap.Grid(self, [self.p.size]*2, track_empty=True)
    
        # Draw Roundabout
        rounaboutPoints = self.makeCircle(int(self.p.size/2),int(self.p.size/2),3)
        self.roundabout = ap.AgentList(self,len(rounaboutPoints))
        self.street.add_agents(self.roundabout,rounaboutPoints)
        self.roundabout.condition = 2

        #Draw Route Around Roundabout
        carRoutePoints = self.makeCircle(int(self.p.size/2),int(self.p.size/2),5)
        self.carRoute = ap.AgentList(self,len(carRoutePoints))
        self.street.add_agents(self.carRoute,carRoutePoints)
        self.carRoute.condition = 0

        #Modeling Route on Circular Doubly Linked List 
        self.route = CircularDLinkedList.buildRoundAbout(carRoutePoints)
        self.route.setNewStart(carRoutePoints[0])

        #Defining Roundabout Entries and Exits based on indexes
        self.entries = [carRoutePoints[i] for i in ENTRIES_INDEXES]
        self.exits = [carRoutePoints[i] for i in EXITS_INDEXES]
        
        #Setting Up Car Spawns
        self.spawns = ap.AgentList(self, 4)
        self.setUpSpawns()
        self.street.add_agents(self.spawns, [spawn.location for spawn in self.spawns])

        #Preparing AgentList of Cars
        self.spawned_cars = 0
        nCars = self.nCars = int(self.p["ncars"])
        self.cars = ap.AgentList(self, nCars)
        self.paso = 0
    
    def setUpSpawns(self):
        for i, spawn in enumerate(self.spawns):
            spawn.condition = 3
            spawn.available = 1
            spawn.location = SPAWNS[i]

    def setUpCar(self, car):
        STARTING_MOVEMENT = [(0,1), (-1,0), (1, 0), (0, -1)]
        ENDING_MOVEMENT = [(0,-1), (1,0), (-1, 0), (0, 1)]
        
        car.name = "Car"+ str(self.spawned_cars+1)
        car.onRoute = -1
        car.condition= 1
        
        entrie = randint(0, 3)
        car.start = self.entries[entrie]
        car.position = car.spawn = SPAWNS[entrie]  
        car.initial_movement = STARTING_MOVEMENT[entrie]
        
        exit = randint(0, 3)
        car.exit = self.exits[exit]
        car.ending_movement = ENDING_MOVEMENT[exit]
        return car

    def getSpawn(self, position):
        for index, spawn in enumerate(self.spawns):
            if spawn.location == position:
                return index 

    def updateCarPosition(self, current_position, movement):
            x, y = current_position
            xi, yi = movement
            return (x + xi, y + yi)

    def step(self):
        if self.spawned_cars < self.nCars:
            carList = ap.AgentList(self, 1, CAR)
            carAgent = self.setUpCar(carList[0])
            spawn_index = self.getSpawn(carAgent.spawn)
            if self.spawns[spawn_index].available == 1:
                self.cars[self.spawned_cars] = carAgent
                self.street._add_agent(self.cars[self.spawned_cars], carAgent.spawn, 'agents')
                self.spawned_cars += 1                     
                self.spawns[spawn_index].available = 0

        cars = self.cars[:self.spawned_cars]
        
        self.CarJson.append([])
        
        for car in cars:
            #SPAWNING
            y, x = car.position
            name = car.name
            carrito = {
                "name" : name,
                "x" : x*580,
                "y": y*580
            }
            self.CarJson[self.paso].append(carrito)
            
            #EXITING ROUNDABOUT
            if car.onRoute == 2:
                if car.position == car.exit:
                    current_position = self.route.findNode(car.position)
                    current_position.available = 1
                self.street.move_by(car, car.ending_movement)
                car.position = self.updateCarPosition(car.position,car.ending_movement)
            
            #ON ROUNDABOUT
            if car.onRoute == 1:
                current_position = self.route.findNode(car.position)
                next_position = current_position.next
                if current_position.data != car.exit and next_position.available == 1:
                    self.street.move_to(car, next_position.data)
                    current_position.available = 1
                    car.position = next_position.data
                    next_position.available = 0
                elif current_position.data == car.exit:
                    car.onRoute = 2

            #HEADING TO ROUNDABOUT
            if car.onRoute == 0:
                new_position = self.updateCarPosition(car.position, car.initial_movement)
                if new_position != car.start:
                    self.street.move_by(car, car.initial_movement)
                    car.position = new_position
                elif new_position == car.start:
                    start = self.route.findNode(new_position)
                    if start.available == 1:
                        self.street.move_by(car, car.initial_movement)
                        car.position = new_position
                        start.available = 0
                        car.onRoute = 1

            if car.onRoute == -1:
                spawn_index = self.getSpawn(car.position)
                new_position = self.updateCarPosition(car.position, car.initial_movement)
                car.position = new_position
                self.street.move_by(car, car.initial_movement)
                self.spawns[spawn_index].available = 1
                car.onRoute = 0
        
        self.paso += 1
        if self.paso == self.p["steps"]:
            carPositions["nCars"] = self.nCars
            carPositions["carPositions"] = self.CarJson  
            self.createJson("positions.json", carPositions)  
            
    def createJson(self, name, obj):
        with open(name, 'w') as file:
            json_string = json.dumps(obj, default=lambda o: o.__dict__, sort_keys=False, indent=4)
            file.write(json_string)

def runModel(nCars,steps):
    parameters = {
        'size': 35,
        'n': 10, # Height and length of the grid
        'steps': steps,
        'ncars': nCars
    }
    return StreetModel(parameters)