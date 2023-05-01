import flatbuffers
from SpaceMap import SpaceObject, SurfacePoint, Space
import numpy as np
class Galaxy:
    def __init__(self):
        # Create member variables
        self.objects = []
        self.numOjbects = 0

    def createObject(self, numPoints):
        # x, y, z = self.split_sphere()
        self.numOjbects += 1
        distance = 45
        NewSpaceObjct = SpaceObjct(self.numOjbects, distance, numPoints)
        self.objects.append(NewSpaceObjct)
        # import matplotlib.pyplot as plt
        # # x, y, z = split_sphere()
        # fig = plt.figure()
        # ax = fig.add_subplot(projection='3d')
        # ax.scatter(x, y, z)
        # plt.show()


class SpaceObjct:
    def __init__(self, objId, distance, num_points):
        self.objId = objId
        self.distance = distance
        self.x, self.y, self.z = self.split_sphere()
        # return self.size

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
Gal.createObject(1)
Gal.createObject(2)

# builder = flatbuffers.Builder(1024)
builder = flatbuffers.Builder(0)

# Create some SurfacePoints
points = []
for point_id in [1, 2, 3]:
    SurfacePoint.SurfacePointStart(builder)
    SurfacePoint.SurfacePointAddLatitude(builder, 1.1)
    SurfacePoint.SurfacePointAddLongitude(builder, 1.2)
    SurfacePoint.SurfacePointAddElevation(builder, 1.3)
    points.append(SurfacePoint.SurfacePointEnd(builder))
#
# Create a SpaceObject that contains SurfacePoints
SpaceObject.SpaceObjectStartSurfaceVector(builder, len(points))
for point in reversed(points):
    builder.PrependUOffsetTRelative(point)
points_vector = builder.EndVector(len(points))

SpaceObject.SpaceObjectStart(builder)
SpaceObject.SpaceObjectAddId(builder, 1)
SpaceObject.SpaceObjectAddSurface(builder, points_vector)

SpaceObject.SpaceObjectAddDistance(builder, 1.0)
spaceObject1 = SpaceObject.SpaceObjectEnd(builder)

SpaceObject.SpaceObjectStart(builder)
SpaceObject.SpaceObjectAddSurface(builder, points_vector)
SpaceObject.SpaceObjectAddId(builder, 2)
SpaceObject.SpaceObjectAddDistance(builder, 3.0)
spaceObject2 = SpaceObject.SpaceObjectEnd(builder)

Space.StartSpaceObjectsVector(builder, 2)
builder.PrependUOffsetTRelative(spaceObject1)
builder.PrependUOffsetTRelative(spaceObject2)
spaceObjects = builder.EndVector()

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

for i in range(space_output.SpaceObjectsLength()):
    print("ID, Distance: ")
    print(space_output.SpaceObjects(i).Id())
    print(space_output.SpaceObjects(i).Distance())
    for j in range(space_output.SpaceObjects(i).SurfaceLength()):
        print("Lat/Long/Elevation: ")
        print(space_output.SpaceObjects(i).Surface(j).Latitude())
        print(space_output.SpaceObjects(i).Surface(j).Longitude())
        print(space_output.SpaceObjects(i).Surface(j).Elevation())
