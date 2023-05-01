import flatbuffers
from SpaceMap import SpaceObject, SurfacePoint, Space

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
