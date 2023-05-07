import numpy as np


class Galaxy:
    def __init__(self):
        self.objects = []
        self.numOjbects = 0

    def initializeObject(self, id, distance, x, y, z):
        self.numOjbects += 1
        newSpaceObject = SpaceObject(id, distance)
        newSpaceObject.addSurface(x, y, z)
        self.objects.append(newSpaceObject)

    def generateObject(self, numPoints):
        self.numOjbects += 1
        distance = 45
        newSpaceObject = SpaceObject(self.numOjbects, distance)
        newSpaceObject.generateSurface()
        self.objects.append(newSpaceObject)


class SpaceObject:
    def __init__(self, objId, distance):
        self.objId = objId
        self.distance = distance

    def generateSurface(self):
        self.x, self.y, self.z = self.split_sphere()

    def addSurface(self, x, y, z):
        self.x, self.y, self.z = np.array(x), np.array(y), np.array(z)

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
