from Galaxy.galaxy import Galaxy
from Galaxy.solar_system import SolarSystem
from Galaxy.space_object import SpaceObject
import json
import numpy as np

class GalaxyJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Galaxy) or isinstance(obj, SolarSystem) or isinstance(obj, SpaceObject):
            return obj.__dict__
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)
    
    @staticmethod
    def serialize(input_galaxy, file_name):
        input_galaxy_json = json.dumps(input_galaxy, indent=4, cls=GalaxyJsonEncoder)
        with open(file_name, 'w') as file:
            json.dump(input_galaxy_json, file)

    @staticmethod
    def deserialize(file_name):
        with open(file_name, 'r') as file:
            serialized_json = file.read()

        output_galaxy = Galaxy()
        
        # Reconstruct space objects
        deserialized_json = json.loads(json.loads(serialized_json))
        for solar_system in deserialized_json['solar_systems']:
            new_solar_sytem = SolarSystem(solar_system['system_id'])
            for space_object in solar_system['objects']:
                new_space_object = SpaceObject(space_object['id'])
                new_space_object.add_distance(space_object['distance'])
                new_space_object.add_surface(space_object['x'], space_object['y'], space_object['z'])
                new_solar_sytem.add_space_object(new_space_object)
            output_galaxy.add_solar_system(new_solar_sytem)

        return output_galaxy
