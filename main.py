from SpaceEncoder import *


def main():
    input_galaxy = Galaxy.Galaxy()
    input_galaxy.generate_mock_objects(10)
    file_name = 'space.bin'

    SpaceEncoder.serialize(input_galaxy, file_name)

    output_galaxy = SpaceEncoder.deserialize(file_name)
    output_galaxy.visualize_galaxy()


if __name__ == "__main__":
    main()
