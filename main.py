from GalaxyJsonEncoder import *
from GalaxyEncoder import *
from Galaxy.galaxy import Galaxy
import time

def main():
    # Generate mock galaxy with mock solar systems
    input_galaxy = Galaxy()
    input_galaxy.generate_solar_systems(16)

    file_name_json = 'output.json'
    file_name_flat_buffer = 'galaxy.bin'

    # Serialize and deserialize using JSON
    start_time = time.time()
    GalaxyJsonEncoder.serialize(input_galaxy, file_name_json)
    serialize_time = time.time() - start_time
    print(f"JSON serialize runtime: {serialize_time} seconds")
    start_time = time.time()
    output_galaxy = GalaxyJsonEncoder.deserialize(file_name_json)
    deserialize_time = time.time() - start_time
    print(f"JSON deserialize runtime: {deserialize_time} seconds")
    output_galaxy.visualize_galaxy()

    # Serialize and deserialize using flat buffers
    start_time = time.time()
    GalaxyEncoder.serialize(input_galaxy, file_name_flat_buffer)
    serialize_time = time.time() - start_time
    print(f"FlatBuffer serialize runtime: {serialize_time} seconds")

    start_time = time.time()
    output_galaxy = GalaxyEncoder.deserialize(file_name_flat_buffer)
    deserialize_time = time.time() - start_time
    print(f"FlatBuffer deserialize runtime: {deserialize_time} seconds")
    output_galaxy.visualize_galaxy()


if __name__ == "__main__":
    main()
