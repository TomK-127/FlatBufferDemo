import numpy as np
import matplotlib.pyplot as plt
from .space_object import SpaceObject


class SolarSystem:
    def __init__(self, system_id):
        self.system_id = system_id
        self.objects = []
        self.num_objects = 0

    def generate_mock_objects(self, size):
        for i in range(0, size):
            space_object = SpaceObject(i+1)
            space_object.generate_object_data()
            self.add_space_object(space_object)

    def add_space_object(self, space_object):
        self.num_objects += 1
        self.objects.append(space_object)

    def visualize_solar_system(self, axes):
        print(f"number of objects: {self.num_objects} ")
        # Reconstruct surface points
        for i in range(0, self.num_objects):
            axes.scatter(self.objects[i].x, self.objects[i].y, self.objects[i].z)