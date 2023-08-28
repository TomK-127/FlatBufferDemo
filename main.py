# from SpaceEncoder import *
from GalaxyEncoder import *
from Galaxy.galaxy import Galaxy
import time


def main():
    input_galaxy = Galaxy()
    input_galaxy.generate_solar_systems(16)
    file_name = 'galaxy.bin'

    start_time = time.time()
    GalaxyEncoder.serialize(input_galaxy, file_name)
    serialize_time = time.time() - start_time
    print(f"serialize() runtime: {serialize_time} seconds")

    start_time = time.time()
    output_galaxy = GalaxyEncoder.deserialize(file_name)
    deserialize_time = time.time() - start_time
    print(f"deserialize() runtime: {deserialize_time} seconds")

    output_galaxy.visualize_galaxy()


if __name__ == "__main__":
    main()
