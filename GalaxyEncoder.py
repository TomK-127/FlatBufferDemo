import flatbuffers
# from SpaceMap import SpaceObject, SurfacePoint, Space
from GalaxyMap import Galaxy, SolarSystem, SpaceObject, SurfacePoint
from Galaxy import galaxy
from Galaxy import solar_system
from Galaxy import space_object


class GalaxyEncoder:
    @staticmethod
    def serialize(input_galaxy, file_name):
        # builder = flatbuffers.Builder(1024)
        builder = flatbuffers.Builder(0)

        # Create Galaxy
        solar_systems = GalaxyEncoder.serialize_solar_systems(builder, input_galaxy)

        Galaxy.GalaxyStart(builder)
        Galaxy.AddSolarSystems(builder, solar_systems)
        enc_solar_system = SolarSystem.End(builder)

        builder.Finish(enc_solar_system)
        buf = builder.Output()
        with open(file_name, 'wb') as f:
            f.write(buf)

    @staticmethod
    def serialize_solar_systems(builder, input_galaxy):
        solar_systems = []

        for input_solar_system in input_galaxy.solar_systems:
            GalaxyEncoder.serialize_solar_system(builder, input_solar_system, solar_systems)

        # Serialize solar systems into vector
        Galaxy.StartSolarSystemsVector(builder, len(solar_systems))
        for input_solar_system in reversed(solar_systems):
            builder.PrependUOffsetTRelative(input_solar_system)
        return builder.EndVector(len(solar_systems))

    @staticmethod
    def serialize_solar_system(builder, input_solar_system, solar_systems):
        space_objects = GalaxyEncoder.serialize_space_objects(builder, input_solar_system)

        SolarSystem.SolarSystemStart(builder)
        SolarSystem.AddSpaceObjects(builder, space_objects)
        solar_systems.append(SolarSystem.End(builder))

    @staticmethod
    def serialize_space_objects(builder, input_solar_system):
        space_objects = []
        for system_object in input_solar_system.objects:
            GalaxyEncoder.serialize_space_object(builder, system_object, space_objects)

        # Serialize space objects into vector
        SolarSystem.StartSpaceObjectsVector(builder, len(space_objects))
        for system_object in reversed(space_objects):
            builder.PrependUOffsetTRelative(system_object)
        return builder.EndVector(len(space_objects))

    @staticmethod
    def serialize_space_object(builder, input_space_object, space_objects):
        # Serialize each surface point
        points = []
        for x, y, z in zip(input_space_object.x, input_space_object.y, input_space_object.z):
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
        SpaceObject.SpaceObjectAddId(builder, input_space_object.id)
        SpaceObject.SpaceObjectAddSurface(builder, points_vector)
        SpaceObject.SpaceObjectAddDistance(builder, input_space_object.distance)

        space_objects.append(SpaceObject.SpaceObjectEnd(builder))

    @staticmethod
    def deserialize(file_name):
        with open(file_name, 'rb') as f:
            buf = f.read()

        input_galaxy = Galaxy.Galaxy.GetRootAsGalaxy(buf, 0)

        # Reconstruct space objects
        output_galaxy = galaxy.Galaxy()
        output_galaxy.add_solar_system(solar_system.SolarSystem(1))
        solar_system1 = input_galaxy.SolarSystems(0)
        # output_galaxy.add_solar_system(solar_system1)
        for i in range(solar_system1.SpaceObjectsLength()):
            input_space_object = solar_system1.SpaceObjects(i)
            object_id = input_space_object.Id()
            distance = input_space_object.Distance()
            lat = []
            long = []
            elev = []
            for j in range(input_space_object.SurfaceLength()):
                lat.append(input_space_object.Surface(j).Latitude())
                long.append(input_space_object.Surface(j).Longitude())
                elev.append(input_space_object.Surface(j).Elevation())
            new_space_object = space_object.SpaceObject(object_id)
            new_space_object.add_surface(lat, long, elev)
            new_space_object.add_distance(distance)
            output_galaxy.solar_systems[0].add_space_object(new_space_object)

        return output_galaxy
