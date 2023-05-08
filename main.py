import serialization


def main():
    input_galaxy = serialization.generate_mock_galaxy(10)
    serialization.serialize(input_galaxy)

    output_galaxy = serialization.deserialize()
    serialization.visualize_galaxy(output_galaxy)


if __name__ == "__main__":
    main()
