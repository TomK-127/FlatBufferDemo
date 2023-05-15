# FlatBufferPractice
 Serialization and deserialization of flat buffer files through a fbs schema

## Usage
* To generate flat buffer API run ```./flatc --python schema.fbs```
* To generate a flat buffer with sample data run serialization.py
* To convert a flat buffer binary to json run the following: ```./flatc --json --raw-binary schema.fbs -- space.bin```


## Resources
* https://flatbuffers.dev/flatbuffers_guide_tutorial.html