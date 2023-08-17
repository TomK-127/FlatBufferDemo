import numpy as np
import matplotlib.pyplot as plt
from .space_object import SpaceObject
from .solar_system import SolarSystem


class Galaxy:
    def __init__(self):
        self.solar_systems = []
        self.num_systems = 0

    def add_solar_system(self, solar_system):
        self.solar_systems.append(solar_system)

    def generate_solar_systems(self, size):
        for i in range(0, size):
            self.num_systems += 1
            new_solar_system = SolarSystem(self.num_systems)
            new_solar_system.generate_mock_objects(self.num_systems)
            self.solar_systems.append(new_solar_system)


