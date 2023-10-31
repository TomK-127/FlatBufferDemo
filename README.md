# FlatBuffer Library Demonstration

### Purpose
  Demonstrate encoding of data through the FlatBuffer library in Python, and compare performance to a traditional serialization method like JSON

### Usage (Linux)
* To serialize data, a .fbs schema must first be created that defines the structure of the data to be serialized 
* The FlatBuffer compiler is needed to interact with the .fbs, and can be downloaded from the [release page of the google/flatbuffers Github repository](https://github.com/google/flatbuffers/releases)
* To generate flat buffer API run ```./flatc --python GalaxySchema.fbs```
* To generate a flat buffer file (the compressed data) with sample data run main.py
* To convert a flat buffer binary to json run the following: ```./flatc --json --raw-binary schema.fbs -- space.bin```

### Results


### Resources
* [Flatbuffer tutorial with additional examples](https://flatbuffers.dev/flatbuffers_guide_tutorial.html)

### Future Work
* Implement FlatBuffer encoding in C++ and compare performance to Python
* Investigate other encodings, such as Apache Parquet