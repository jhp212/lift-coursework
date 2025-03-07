from random import randint as rng
import json, jsbeautifier, os

options = jsbeautifier.default_options()
options.indent_size = 4

def generate_test_dict(floor_count: int, capacity: int, passenger_count: int) -> dict:
    """Generates a dictionary of the random simulation.

    Args:
        floor_count (int): The number of floors in this specific simulation.
        capacity (int): The maximum capacity that the lift can transport.
        passenger_count (int): The total number of passengers in the simulation

    Returns:
        dict: The dictionary that will be saved in a .json file
    """
    result_dict = {"floor_count": floor_count, "capacity": capacity, "floor_requests": {}}
    for i in range(1, floor_count + 1):
        result_dict["floor_requests"][str(i)] = []

    for i in range(passenger_count):
        start_floor = rng(1, floor_count)
        end_floor = rng(1, floor_count)
        while start_floor == end_floor:
            end_floor = rng(1, floor_count)
        result_dict["floor_requests"][str(start_floor)].append(end_floor)

    return result_dict

def save_dict_as_json(dictionary: dict, filename: str):
    """Saves the dictionary as a .json file

    Args:
        dictionary (dict): The dictionary to be saved
        filename (str): The location where the file should be saved
    """
    with open(filename, "w") as jsonfile:
        result = jsbeautifier.beautify(json.dumps(dictionary))
        jsonfile.write(result)

def generate_tests():
    """A function to generate all the tests for the random simulation"""
    # vary floor count from 2 to 100
    capacity = 5
    passenger_count = 1000

    for floor_count in range(2, 101):
        for i in range(10):
            file_path = f"sources/tests/floor_count_{floor_count}_{i}.json"
            if os.path.exists(file_path):
                continue
            test_dict = generate_test_dict(floor_count, capacity, passenger_count)
            save_dict_as_json(test_dict, file_path)
            print(f"Generated file {file_path}")
    
    # vary capacity from 1 to 50
    floor_count = 20
    for capacity in range(1, 51):
        for i in range(10):
            file_path = f"sources/tests/capacity_{capacity}_{i}.json"
            if os.path.exists(file_path):
                continue
            test_dict = generate_test_dict(floor_count, capacity, passenger_count)
            save_dict_as_json(test_dict, file_path)
            print(f"Generated file {file_path}")
    
    # vary passenger count from 10 to 1000
    floor_count = 20
    capacity = 5
    for passenger_count in range(10, 1010, 10):
        for i in range(10):
            file_path = f"sources/tests/passenger_count_{passenger_count}_{i}.json"
            if os.path.exists(file_path):
                continue
            test_dict = generate_test_dict(floor_count, capacity, passenger_count)
            save_dict_as_json(test_dict, file_path)
            print(f"Generated file {file_path}")


if __name__ == "__main__":
    generate_tests()