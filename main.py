# from SpaceEncoder import *
from GalaxyEncoder import *
from Galaxy.galaxy import Galaxy


def main():
    input_galaxy = Galaxy()
    input_galaxy.generate_solar_systems(40)
    file_name = 'galaxy.bin'

    # SpaceEncoder.serialize(input_galaxy, file_name)
    GalaxyEncoder.serialize(input_galaxy, file_name)

    output_galaxy = GalaxyEncoder.deserialize(file_name)
    # output_galaxy.solar_systems[0].visualize_solar_system()
    # output_galaxy.solar_systems[1].visualize_solar_system()


if __name__ == "__main__":
    main()
