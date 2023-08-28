# from SpaceEncoder import *
from GalaxyEncoder import *
from Galaxy.galaxy import Galaxy


def main():
    input_galaxy = Galaxy()
    input_galaxy.generate_solar_systems(9)
    file_name = 'galaxy.bin'

    # SpaceEncoder.serialize(input_galaxy, file_name)
    GalaxyEncoder.serialize(input_galaxy, file_name)

    output_galaxy = GalaxyEncoder.deserialize(file_name)
    output_galaxy.visualize_galaxy()


if __name__ == "__main__":
    main()
