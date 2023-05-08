import numpy as np
import matplotlib.pyplot as plt


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


class SpaceObject:
    def __init__(self, obj_id):
        self.id = obj_id
        self.x, self.y, self.z = [], [], []
        self.distance = 0

    def generate_object_data(self):
        # Create randomized surface
        radius = np.random.rand() * 10000.0
        split_factor = np.random.randint(36, 50)
        horizontal_split = split_factor
        vertical_split = split_factor
        self.x, self.y, self.z = self.split_sphere(radius, horizontal_split, vertical_split)

        self.distance = np.random.rand() * 100000.0
        phi = np.random.rand() * 360
        theta = np.random.rand() * 360
        x_offset = self.distance * (np.cos(phi) * np.cos(theta))
        y_offset = self.distance * (np.sin(phi) * np.cos(theta))
        z_offset = self.distance * (np.sin(theta))
        self.x += x_offset
        self.y += y_offset
        self.z += z_offset

    def add_surface(self, x, y, z):
        self.x, self.y, self.z = np.array(x), np.array(y), np.array(z)

    def add_distance(self, distance):
        self.distance = distance

    # Generate coordinates for a sphere
    # https://stackoverflow.com/questions/73825731/how-to-generate-points-on-spherical-surface-making-equal-parts
    def split_sphere(self, radius, horizontal_split, vertical_split, method="equal_angles"):
        theta = np.linspace(0, 360, horizontal_split + 1)
        if method == "equal_angles":
            phi = np.linspace(0, 180, vertical_split + 1)
            c = np.cos(phi)
            s = np.sin(phi)
        elif method == "equal_area":
            c = np.linspace(-1, 1, vertical_split + 1)
            s = 1 - c ** 2
        else:
            raise (ValueError('method must be "equal_angles" or "equal_area"'))
        x = radius * np.outer(s, np.cos(theta))
        y = radius * np.outer(s, np.sin(theta))
        z = radius * np.outer(c, np.ones(horizontal_split + 1))
        return x.flatten(), y.flatten(), z.flatten()
