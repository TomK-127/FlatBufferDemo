import flatbuffers
from SpaceMap import SpaceObject, SurfacePoint, Space
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
    def split_sphere(self, R = 1.0, horizontal_split = 36, vertical_split = 36, method="equal_angles"):
        theta = np.linspace(0,360,horizontal_split+1)
        if method == "equal_angles":
            phi = np.linspace(0, 180, vertical_split+1)
            c = np.cos(phi)
            s = np.sin(phi)
        elif method == "equal_area":
            c = np.linspace(-1, 1, vertical_split+1)
            s = 1 - c**2
        else:
            raise(ValueError('method must be "equal_angles" or "equal_area"'))
        x = R * np.outer(s, np.cos(theta))
        y = R * np.outer(s, np.sin(theta))
        z = R * np.outer(c, np.ones(horizontal_split+1))
        return x.flatten(), y.flatten(), z.flatten()

Gal = Galaxy()
Gal.generateObject(1)
Gal.generateObject(2)


# builder = flatbuffers.Builder(1024)
builder = flatbuffers.Builder(0)

# Serialize space objects
space_objects = []
for spaceObject in Gal.objects:

    # each space object has a vector of surface points
    points = []
    for i in range(0, len(spaceObject.x)):
        SurfacePoint.SurfacePointStart(builder)
        SurfacePoint.SurfacePointAddLatitude(builder, spaceObject.x[i])
        SurfacePoint.SurfacePointAddLongitude(builder, spaceObject.y[i])
        SurfacePoint.SurfacePointAddElevation(builder, spaceObject.z[i])
        points.append(SurfacePoint.SurfacePointEnd(builder))

    # Create a SpaceObject that contains SurfacePoints
    SpaceObject.SpaceObjectStartSurfaceVector(builder, len(points))
    for point in reversed(points):
        builder.PrependUOffsetTRelative(point)
    points_vector = builder.EndVector(len(points))

    SpaceObject.SpaceObjectStart(builder)
    SpaceObject.SpaceObjectAddId(builder, spaceObject.objId)
    SpaceObject.SpaceObjectAddSurface(builder, points_vector)
    SpaceObject.SpaceObjectAddDistance(builder, spaceObject.distance)

    space_objects.append(SpaceObject.SpaceObjectEnd(builder))

SpaceObject.SpaceObjectStartSurfaceVector(builder, len(space_objects))
for spaceObj in reversed(space_objects):
    builder.PrependUOffsetTRelative(spaceObj)
spaceObjects = builder.EndVector(len(space_objects))

Space.SpaceStart(builder)
Space.AddSpaceObjects(builder, spaceObjects)
space = Space.End(builder)

# Finish building the FlatBuffers object and write it to a file
builder.Finish(space)
buf = builder.Output()
with open('space.bin', 'wb') as f:
    f.write(buf)

# Access the newly written file and check for correctness
with open('space.bin', 'rb') as f:
    buf = f.read()

space_output = Space.Space.GetRootAsSpace(buf, 0)

# Reconstruct space objects
outputGalaxy = Galaxy()
for i in range(space_output.SpaceObjectsLength()):
    id = space_output.SpaceObjects(i).Id()
    distance = space_output.SpaceObjects(i).Distance()
    lat = []
    long = []
    elev = []
    for j in range(space_output.SpaceObjects(i).SurfaceLength()):
        lat.append(space_output.SpaceObjects(i).Surface(j).Latitude())
        long.append(space_output.SpaceObjects(i).Surface(j).Longitude())
        elev.append(space_output.SpaceObjects(i).Surface(j).Elevation())
    outputGalaxy.createObject(id, distance, lat, long, elev)

# Reconstruct surface points
import matplotlib.pyplot as plt
# x, y, z = split_sphere()
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(outputGalaxy.objects[0].x, outputGalaxy.objects[0].y, outputGalaxy.objects[0].z)
plt.show()