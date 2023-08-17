# Flatbuffer Library Demonstration

### Purpose
  Demonstrate serialization and deserialization of data through the Flatbuffer library, and show superior performance for compression and retrieval of information compared to a traditional serialization method like JSON

### Usage
* To serialize information, a .fbs schema must first be created that defines the structure of the data to be serialized 
* The FlatBuffer compiler is needed to interact with the .fbs, and can be downloaded from the [release page of the google/flatbuffers Github repository](https://github.com/google/flatbuffers/releases)
* To generate flat buffer API run ```./flatc --python schema.fbs```
* To generate a flat buffer file (the compressed data) with sample data run main.py
* To convert a flat buffer binary to json run the following: ```./flatc --json --raw-binary schema.fbs -- space.bin```


### Resources
* [Flatbuffer tutorial with additional examples](https://flatbuffers.dev/flatbuffers_guide_tutorial.html)