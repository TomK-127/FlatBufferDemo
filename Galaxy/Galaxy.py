import numpy as np


class Galaxy:
    def __init__(self):
        # Create member variables
        self.objects = []
        self.numOjbects = 0

    def createObject(self, id, distance, x, y, z):
        self.numOjbects += 1
        NewSpaceObjct = SpaceObjct(id, distance, x, y, z)
        self.objects.append(NewSpaceObjct)

    def generateObject(self, numPoints):
        # x, y, z = self.split_sphere()
        self.numOjbects += 1
        distance = 45
        NewSpaceObjct = SpaceObjct(self.numOjbects, distance, [], [], [])
        self.objects.append(NewSpaceObjct)


class SpaceObjct:
    def __init__(self, objId, distance, x, y, z):
        self.objId = objId
        self.distance = distance
        if x:
            self.x, self.y, self.z = x, y, z
        else:
            self.x, self.y, self.z = self.split_sphere()

    # Generate coordinates for a sphere
    # https://stackoverflow.com/questions/73825731/how-to-generate-points-on-spherical-surface-making-equal-parts
    def split_sphere(self, R=1.0, horizontal_split=36, vertical_split=36, method="equal_angles"):
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
        x = R * np.outer(s, np.cos(theta))
        y = R * np.outer(s, np.sin(theta))
        z = R * np.outer(c, np.ones(horizontal_split + 1))
        return x.flatten(), y.flatten(), z.flatten()
