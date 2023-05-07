import flatbuffers
from SpaceMap import SpaceObject, SurfacePoint, Space
from Galaxy import Galaxy
import numpy as np



Gal = Galaxy.Galaxy()
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
outputGalaxy = Galaxy.Galaxy()
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
    outputGalaxy.initializeObject(id, distance, lat, long, elev)

# Reconstruct surface points
import matplotlib.pyplot as plt
# x, y, z = split_sphere()
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(outputGalaxy.objects[0].x, outputGalaxy.objects[0].y, outputGalaxy.objects[0].z)
plt.show()