from SpaceEncoder import *
from Galaxy.galaxy import Galaxy

def main():
    input_galaxy = Galaxy()
    input_galaxy.generate_mock_objects(10)
    # input_galaxy.generate_mock_systems(1)
    file_name = 'space.bin'

    SpaceEncoder.serialize(input_galaxy, file_name)

    output_galaxy = SpaceEncoder.deserialize(file_name)
    output_galaxy.visualize_galaxy()


if __name__ == "__main__":
    main()
