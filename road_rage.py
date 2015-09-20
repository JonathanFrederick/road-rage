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

    def acceleration(self, driver_1, driver_2):
        new_loc = driver_1.location + driver_1.curr_speed
        #If driver would hit
        if new_loc % self.road.length > ((driver_2.location-driver_2.size - 1)) % self.road.length:
            driver_1.curr_speed = 0
        #If driver would be too close for comfort
        elif new_loc % self.road.length > ((driver_2.location-driver_2.size - 1)-driver_1.curr_speed*driver_1.min_space_mod) % self.road.length:
            driver_1.curr_speed = driver_2.curr_speed
        #Otherwise, roll for acceleration/deceleration
        else:
            if random.random() > driver_1.slow_chance and driver_1.curr_speed <= self.road.speed_limit:
                driver_1.curr_speed += driver_1.accel
            else:
                driver_1.curr_speed -= 2

    def tick(self):
        for x in range(len(self.road.vehicles) - 1, -1, -1):
            self.acceleration(self.road.vehicles[x], self.road.vehicles[(x+1) % len(self.road.vehicles)])
            self.road.vehicles[x].motion()

    def run_sim(self):
        while self.ticks < self.max_ticks:
            self.tick()
            self.speeds[self.ticks+1] += [x.curr_speed for x in self.road.vehicles]
#            self.locations[self.ticks+1] += [x.location for x in self.road.vehicles]
            self.ticks += 1
        return self.speeds#, self.locations
