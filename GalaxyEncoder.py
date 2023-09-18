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

        serialized_galaxy = GalaxyEncoder.serialize_galaxy(builder, input_galaxy)
        solar_systems = GalaxyEncoder.serialize_solar_systems(builder, input_galaxy)

        Galaxy.GalaxyStart(builder)
        Galaxy.AddSolarSystems(builder, solar_systems)

        builder.Finish(serialized_galaxy)
        buf = builder.Output()
        with open(file_name, 'wb') as f:
            f.write(buf)

    @staticmethod
    def serialize_galaxy(builder, input_galaxy):
        solar_systems = GalaxyEncoder.serialize_solar_systems(builder, input_galaxy)

        Galaxy.GalaxyStart(builder)
        Galaxy.AddSolarSystems(builder, solar_systems)
        return SolarSystem.End(builder)

    @staticmethod
    def serialize_solar_systems(builder, input_galaxy):
        solar_systems = []

        for input_solar_system in input_galaxy.solar_systems:
            solar_systems.append(GalaxyEncoder.serialize_solar_system(builder, input_solar_system))

        # Turn into vector to be stored in a galaxy
        Galaxy.StartSolarSystemsVector(builder, len(solar_systems))
        for input_solar_system in reversed(solar_systems):
            builder.PrependUOffsetTRelative(input_solar_system)
        return builder.EndVector(len(solar_systems))

    @staticmethod
    def serialize_solar_system(builder, input_solar_system):
        space_objects = GalaxyEncoder.serialize_space_objects(builder, input_solar_system.objects)

        SolarSystem.SolarSystemStart(builder)
        SolarSystem.AddId(builder, input_solar_system.system_id)
        SolarSystem.AddSpaceObjects(builder, space_objects)
        return SolarSystem.End(builder)

    @staticmethod
    def serialize_space_objects(builder, input_space_objects):
        space_objects = []
        for system_object in input_space_objects:
            space_objects.append(GalaxyEncoder.serialize_space_object(builder, system_object))

        # Serialize space objects into vector
        SolarSystem.StartSpaceObjectsVector(builder, len(space_objects))
        for system_object in reversed(space_objects):
            builder.PrependUOffsetTRelative(system_object)
        return builder.EndVector(len(space_objects))

    @staticmethod
    def serialize_space_object(builder, input_space_object):
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

        return SpaceObject.SpaceObjectEnd(builder)

    @staticmethod
    def deserialize(file_name):
        with open(file_name, 'rb') as f:
            buf = f.read()

        input_galaxy = Galaxy.Galaxy.GetRootAsGalaxy(buf, 0)

        # Reconstruct space objects
        output_galaxy = galaxy.Galaxy()
        for i in range(input_galaxy.SolarSystemsLength()):
            input_solar_system = input_galaxy.SolarSystems(i)
            output_solar_system = solar_system.SolarSystem(input_solar_system.Id())
            for j in range(input_solar_system.SpaceObjectsLength()):
                input_space_object = input_solar_system.SpaceObjects(j)
                object_id = input_space_object.Id()
                distance = input_space_object.Distance()
                lat, long, elev = [], [], []
                for k in range(input_space_object.SurfaceLength()):
                    lat.append(input_space_object.Surface(k).Latitude())
                    long.append(input_space_object.Surface(k).Longitude())
                    elev.append(input_space_object.Surface(k).Elevation())
                new_space_object = space_object.SpaceObject(object_id)
                new_space_object.add_surface(lat, long, elev)
                new_space_object.add_distance(distance)
                output_solar_system.add_space_object(new_space_object)
            output_galaxy.add_solar_system(output_solar_system)
        return output_galaxy
