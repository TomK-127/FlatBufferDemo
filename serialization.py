import flatbuffers
from SpaceMap import SpaceObject, SurfacePoint, Space

builder = flatbuffers.Builder(1024)

# Create some SurfacePoints
point_ids = [1, 2, 3]
points = []
for point_id in point_ids:
    SurfacePoint.SurfacePointStart(builder)
    SurfacePoint.SurfacePointAddLatitude(builder, point_id)
    SurfacePoint.SurfacePointAddLongitude(builder, point_id)
    SurfacePoint.SurfacePointAddElevation(builder, point_id)
    points.append(SurfacePoint.SurfacePointEnd(builder))

# Create a SpaceObject that contains SurfacePoints
SpaceObject.SpaceObjectStartSurfaceVector(builder, len(points))
for point in reversed(points):
    builder.PrependUOffsetTRelative(point)
points_vector = builder.EndVector(len(points))

SpaceObject.SpaceObjectStart(builder)
SpaceObject.SpaceObjectAddId(builder, 1)
SpaceObject.SpaceObjectAddDistance(builder, 1)
SpaceObject.SpaceObjectAddSurface(builder, points_vector)
Space = SpaceObject.SpaceObjectEnd(builder)

# Finish building the FlatBuffers object and write it to a file
builder.Finish(Space)
buf = builder.Output()
with open('space.bin', 'wb') as f:
    f.write(buf)

