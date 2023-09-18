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
        self.num_systems += 1

    def generate_solar_systems(self, size):
        for i in range(0, size):
            self.num_systems += 1
            new_solar_system = SolarSystem(self.num_systems)
            new_solar_system.generate_mock_objects(self.num_systems)
            self.solar_systems.append(new_solar_system)

    def visualize_galaxy(self):
        nrows = int(np.sqrt(self.num_systems))
        ncols = int(np.sqrt(self.num_systems))
        fig, axes = plt.subplots(nrows, ncols, subplot_kw={'projection': '3d'}, figsize=(18, 9))
        num_subplots = len(axes.flatten())
        for i, ax in zip(range(num_subplots), axes.flatten()):
            if i < self.num_systems:
                solar_system = self.solar_systems[i]
                
                # Call sub-function for visualizing the solar system passing the current axes
                ax.set_title(f'Solar System: {solar_system.system_id}')
                solar_system.visualize_solar_system(ax)

        plt.show()
