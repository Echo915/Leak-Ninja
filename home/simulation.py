import csv

import matplotlib
matplotlib.use("Agg")
"""Agg (Anti-Grain Geometry) allows you to create and save plots without requiring a GUI to 
display the plot. This is important when working wi"""

import matplotlib.pyplot as plt
import numpy as np

from math import pi



class Leak:
    def __init__(self, location, size):
        self.location = location
        self.size = size

    # Alerts warning of leak detected at specified location
    def status(self):
        sectionStart = self.location[0]
        sectionEnd = self.location[1]
        print(f"LEAK DETECTED BETWEEN {sectionStart} AND {sectionEnd}")
        print(f"LEAK SIZE: {self.size}", "\n")


# Returns True if a number is odd
def is_odd(number):
    if number % 2 == 1:
        return True


# Returns True if a leak is present in a pipe section
def leak_present(section):
    # Calculates inlet and outlet flowrate for a pipe section 
    V_in = float(section[0]["velocity"])
    V_out = float(section[-1]["velocity"])

    # Calculates mass rate using the inlet and outlet flow rates of the section
    massRate_in = DENSITY * AREA * V_in
    massRate_out = DENSITY * AREA * V_out
    leak_size = massRate_in - massRate_out

    # Returns true if mass difference is not equal to '0'
    if leak_size > 0:
        leak_size = round(leak_size, 4)
        return True, leak_size


# Determines the location of leaks present in a pipe section
def findLeak(section):
    # length of the section / number of datapoints provided
    length = len(section)
    leakPresent, leakSize = leak_present(section)
    if len(section) == 2 and leakPresent:
        leak_location = (section[0]['length'], section[1]['length'])
        newLeak = Leak(leak_location, leakSize)
        DETECTED_LEAKS.append(newLeak)
        return

    # Leak location calculation if the number of datapoints is an odd number
    elif is_odd(length):
        midPoint = length // 2
        section1 = section[ : midPoint + 1]
        section2 = section[midPoint: ]

        if leak_present(section1):
            findLeak(section1)
        if leak_present(section2):
            findLeak(section2)

    # Leak location calculation if the number of datapoints is an even number
    elif not is_odd(length):
        section1 = section[0:2]
        section2 = section[1: ]

        if leak_present(section1):
            findLeak(section1)
        if leak_present(section2):
            findLeak(section2)


def leakSimulation(data, density, diameter):
    # Initialize parameters
    global DENSITY, DIAMETER, AREA, DATA, DETECTED_LEAKS, POSITION, PRESSURE, VELOCITY

    # Empty list to store extracted data from csv file
    DATA = []

    # All leaks detected in the entire pipe
    DETECTED_LEAKS = []

    # Chart parameters
    POSITION = []
    PRESSURE = []
    VELOCITY = []

    DENSITY = density
    DIAMETER = diameter
    AREA = (pi / 4) * DIAMETER**2

    # Opens csv file to extract data
    with open (data, "r") as fileObj:
        data = csv.DictReader(fileObj)
        for point in data:
            DATA.append(point)

    findLeak(DATA)
    return DETECTED_LEAKS


def plotGraph(position, y_axis, y_label, title):
    plt.ioff()

    plt.plot(position, y_axis)
    #plt.yticks(np.arange(0.8620, 0.863, 0.0002))

    # Axes Label
    plt.xlabel("Location")
    plt.ylabel(y_label)

    # Saves a png format of the plot
    plt.savefig(f"static/images/{title}", format="png")

    # Removes current plot
    plt.clf()


def chartSimulation(data, title):
    with open (data, "r", encoding="utf-8") as fileObj:
        datapoints = csv.DictReader(fileObj)
        for point in datapoints:
            POSITION.append(float(point["length"]))
            PRESSURE.append(float(point["pressure"]))
            VELOCITY.append(float(point["velocity"]))

    # Axes    
    position = np.array(POSITION)
    velocity = np.array(VELOCITY)
    pressure = np.array(PRESSURE)

    # Plots velocity and pressure chart against position
    vTitle = f"{title}_velocity.png"
    vLabel = "Velocity"
    pTitle = f"{title}_pressure.png"
    pLabel = "Pressure"        
    plotGraph(position, pressure, pLabel, pTitle)
    plotGraph(position, velocity, vLabel, vTitle)

    return vTitle, pTitle
