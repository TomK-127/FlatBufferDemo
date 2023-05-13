from SpaceEncoder import *
from Galaxy.galaxy import Galaxy
# from Galaxy.solar_system import SolarSystem
# from Galaxy.space_object import SpaceObject


def main():
    input_galaxy = Galaxy()
    input_galaxy.generate_mock_objects(10)
    file_name = 'space.bin'

    SpaceEncoder.serialize(input_galaxy, file_name)

    output_galaxy = SpaceEncoder.deserialize(file_name)
    output_galaxy.visualize_galaxy()


if __name__ == "__main__":
    main()
