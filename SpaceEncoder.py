import flatbuffers
from SpaceMap import SpaceObject, SurfacePoint, Space
from Galaxy.galaxy import Galaxy


class SpaceEncoder:
    @staticmethod
    def serialize(galaxy, file_name):
        # builder = flatbuffers.Builder(1024)
        builder = flatbuffers.Builder(0)

        space_objects = SpaceEncoder.serialize_space_objects(builder, galaxy)

        # Create space and add space objects
        Space.SpaceStart(builder)
        Space.AddSpaceObjects(builder, space_objects)
        space = Space.End(builder)

        # Finish building the FlatBuffers object and write it to a file
        builder.Finish(space)
        buf = builder.Output()
        with open(file_name, 'wb') as f:
            f.write(buf)

    @staticmethod
    def serialize_space_objects(builder, galaxy):
        space_objects = []
        for space_object in galaxy.objects:
            SpaceEncoder.serialize_space_object(builder, space_object, space_objects)

        # Serialize space objects into vector
        Space.StartSpaceObjectsVector(builder, len(space_objects))
        for space_object in reversed(space_objects):
            builder.PrependUOffsetTRelative(space_object)
        return builder.EndVector(len(space_objects))

    @staticmethod
    def serialize_space_object(builder, space_object, space_objects):
        # Serialize each surface point
        points = []
        for x, y, z in zip(space_object.x, space_object.y, space_object.z):
            SurfacePoint.SurfacePointStart(builder)
            SurfacePoint.SurfacePointAddLatitude(builder, x)
            SurfacePoint.SurfacePointAddLongitude(builder, y)
            SurfacePoint.SurfacePointAddElevation(builder, z)
            points.append(SurfacePoint.SurfacePointEnd(builder))

        # turn points into vector
        SpaceObject.SpaceObjectStartSurfaceVector(builder, len(points))
        for point in reversed(points):
            builder.PrependUOffsetTRelative(point)
        points_vector = builder.EndVector(len(points))

        # create space object and fill fields
        SpaceObject.SpaceObjectStart(builder)
        SpaceObject.SpaceObjectAddId(builder, space_object.id)
        SpaceObject.SpaceObjectAddSurface(builder, points_vector)
        SpaceObject.SpaceObjectAddDistance(builder, space_object.distance)

        space_objects.append(SpaceObject.SpaceObjectEnd(builder))

    @staticmethod
    def deserialize(file_name):
        with open(file_name, 'rb') as f:
            buf = f.read()

        space_output = Space.Space.GetRootAsSpace(buf, 0)

        # Reconstruct space objects
        output_galaxy = Galaxy()
        for i in range(space_output.SpaceObjectsLength()):
            object_id = space_output.SpaceObjects(i).Id()
            distance = space_output.SpaceObjects(i).Distance()
            lat = []
            long = []
            elev = []
            for j in range(space_output.SpaceObjects(i).SurfaceLength()):
                lat.append(space_output.SpaceObjects(i).Surface(j).Latitude())
                long.append(space_output.SpaceObjects(i).Surface(j).Longitude())
                elev.append(space_output.SpaceObjects(i).Surface(j).Elevation())
            # space_object = SpaceObject(object_id)
            output_galaxy.initialize_object(object_id, distance, lat, long, elev)

        return output_galaxy
