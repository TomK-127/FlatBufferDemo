from GalaxyJsonEncoder import *
from GalaxyFlatBufferEncoder import *
from Galaxy.galaxy import Galaxy
import time
import os
import shutil

def main():
    # Delete files from previous runs
    output_folder = "output"
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.mkdir(output_folder)

    # Generate mock galaxy with mock solar systems
    input_galaxy = Galaxy()
    input_galaxy.generate_solar_systems(9)

    file_name_json = 'output/galaxy.json'
    file_name_flat_buffer = 'output/galaxy.bin'

    # Serialize and deserialize using JSON
    start_time = time.time()
    GalaxyJsonEncoder.serialize(input_galaxy, file_name_json)
    process_time = time.time() - start_time
    print(f"JSON serialize runtime: {process_time} seconds")
    start_time = time.time()
    output_galaxy = GalaxyJsonEncoder.deserialize(file_name_json)
    process_time = time.time() - start_time
    print(f"JSON deserialize runtime: {process_time} seconds")
    output_galaxy.visualize_galaxy()

    # Serialize and deserialize using flat buffers
    start_time = time.time()
    GalaxyFlatBufferEncoder.serialize(input_galaxy, file_name_flat_buffer)
    process_time = time.time() - start_time
    print(f"FlatBuffer serialize runtime: {process_time} seconds")

    start_time = time.time()
    output_galaxy = GalaxyFlatBufferEncoder.deserialize(file_name_flat_buffer)
    process_time = time.time() - start_time
    print(f"FlatBuffer deserialize runtime: {process_time} seconds")
    output_galaxy.visualize_galaxy()


if __name__ == "__main__":
    main()
