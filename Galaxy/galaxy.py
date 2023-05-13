import numpy as np
import matplotlib.pyplot as plt
from .space_object import SpaceObject


class Galaxy:
    def __init__(self):
        self.objects = []
        self.num_objects = 0

    # create a space object and initialize it based on input parameters
    def initialize_object(self, obj_id, distance, x, y, z):
        self.num_objects += 1
        space_object = SpaceObject(obj_id)
        space_object.add_surface(x, y, z)
        space_object.add_distance(distance)
        self.objects.append(space_object)

    # Generate a new random space object
    def generate_object(self):
        self.num_objects += 1
        space_object = SpaceObject(self.num_objects)
        space_object.generate_object_data()
        self.objects.append(space_object)

    def generate_mock_objects(self, size):
        for i in range(0, size):
            self.generate_object()

    def visualize_galaxy(self):
        print(f"number of objects: {self.num_objects} ")
        # Reconstruct surface points

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        for i in range(0, self.num_objects):
            ax.scatter(self.objects[i].x, self.objects[i].y, self.objects[i].z)
        plt.show()

