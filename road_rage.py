import math
import random
import statistics as st
import numpy as np
import matplotlib.pyplot as plt

class Driver:
    """
    Responsibilities:
    - Acceleration in m/s/s
    - Desired Speed in km/h
    - Vehicle Size in m
    - Minimum Spacing in m
    - Chance to Slow
    """
    def __init__(self, location, max_speed=120, accel=2, size=5, slow_chance=.1, min_space_mod=1):
        self.max_speed = max_speed*1000/3600
        self.accel = accel
        self.size = size
        self.slow_chance = slow_chance
        self.curr_speed = self.max_speed
        self.location = location
        self.min_space_mod = min_space_mod

    def motion(self):
        self.location += self.curr_speed

    def __str__(self):
        return "Driver(accel={}, max_speed={}, size={}, slow_chance={}, min_space_mod={}, curr_speed={}, location={})".format(
            self.accel, self.max_speed, self.size, self.slow_chance, self.min_space_mod, self.curr_speed, self.location)

    def __repr__(self):
        return self.__str__()

class Road:
    """
    Responsibilities:
    - Hold Drivers
    - Number of drivers (in drivers per k/m)
    - Hold length
    - Slow down modifiers

    Collaboroators:
    -Driver
    """

    def __init__(self, speed_limit=120, length=1000, density=30):
        self.speed_limit = speed_limit
        self.length = length
        self.vehicles = [self.roll_car(loc*length//density) for loc in range(density*length//1000)]


    def roll_car(self, loc):
#        roll = random.random()
        return Driver(loc, self.speed_limit)


class Simulation:
    """
    Responsibilities:
    - Handles acceleration, deceleration, stopping
    - Handles motion
    - Handles ticks
    - Returns data"""

    def __init__(self, speed_limit, max_ticks=60):
        self.road = Road(speed_limit)
        self.max_ticks = max_ticks
        self.ticks = 0
        self.speeds = np.array([])
        self.locations = np.array([])
        self.speeds.resize(max_ticks+1, (len(self.road.vehicles)*self.road.length//1000))
        self.locations.resize(max_ticks+1, (len(self.road.vehicles)*self.road.length//1000))
        self.speeds[0] = [x.curr_speed for x in self.road.vehicles]
        self.locations[0] = [x.location for x in self.road.vehicles]


    def roll_accel(self, x):
        if random.random() > self.road.vehicles[x].slow_chance and self.road.vehicles[x].curr_speed <= self.road.speed_limit:
            self.road.vehicles[x].curr_speed += self.road.vehicles[x].accel
        else:
            self.road.vehicles[x].curr_speed -= 2

    def check_too_close(self, x, y, new_loc):
        #If driver would hit
        if new_loc > ((self.road.vehicles[y].location-self.road.vehicles[y].size - 1)):
            self.road.vehicles[x].curr_speed = 0
        #If driver would be too close for comfort
        elif new_loc > ((self.road.vehicles[y].location-self.road.vehicles[y].size - 1)-self.road.vehicles[x].curr_speed*self.road.vehicles[x].min_space_mod):
            self.road.vehicles[x].curr_speed = self.road.vehicles[y].curr_speed
        #Otherwise, roll for acceleration/deceleration
        else:
            self.roll_accel(x)


    def acceleration(self, x, y):
        new_loc = self.road.vehicles[x].location + self.road.vehicles[x].curr_speed
        if self.road.vehicles[x].location > self.road.vehicles[y].location:
            if new_loc > self.road.length:
                self.check_too_close(x-1, x, new_loc)
                del self.road.vehicles[x]
                self.road.vehicles.insert(0, self.road.roll_car(0 - self.road.speed_limit*1000//3600))
            else:
                self.roll_accel(x)
        else:
            self.check_too_close(x, y, new_loc)

    def tick(self):
        for x in range(len(self.road.vehicles) - 1, -1, -1):
            self.acceleration(x, (x+1) % len(self.road.vehicles))
            self.road.vehicles[x].motion()

    def run_sim(self):
        while self.ticks < self.max_ticks:
            self.tick()
            self.speeds[self.ticks+1] += [x.curr_speed for x in self.road.vehicles]
#            self.locations[self.ticks+1] += [x.location for x in self.road.vehicles]
            self.ticks += 1
        return self.speeds#, self.locations


class SimLoc(Simulation):
    def __init__(self, speed_limit):
        super().__init__(speed_limit)

    def run_sim(self):
        while self.ticks < self.max_ticks:
            self.tick()
            self.locations[self.ticks+1] += [x.location for x in self.road.vehicles]
            self.ticks += 1
        return self.locations
