from random import randint as rng
import json
import jsbeautifier

options = jsbeautifier.default_options()
options.indent_size = 4

def generate_test_dict(floor_count, capacity, passenger_count):
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

def save_dict_as_json(dict, filename):
    with open(filename, "w") as jsonfile:
        result = jsbeautifier.beautify(json.dumps(dict))
        jsonfile.write(result)

def main():
    # vary floor count
    capacity = 5
    passenger_count = 1000

    for floor_count in range(2, 100):
        for i in range(5):
            test_dict = generate_test_dict(floor_count, capacity, passenger_count)
            save_dict_as_json(test_dict, f"sources/tests/floor_count_{floor_count}_{i}.json")
    
    # vary capacity
    floor_count = 20
    for capacity in range(1, 50):
        for i in range(5):
            test_dict = generate_test_dict(floor_count, capacity, passenger_count)
            save_dict_as_json(test_dict, f"sources/tests/capacity_{capacity}_{i}.json")
    
    # vary passenger count
    floor_count = 20
    capacity = 5
    for passenger_count in range(10, 1010, 10):
        for i in range(5):
            test_dict = generate_test_dict(floor_count, capacity, passenger_count)
            save_dict_as_json(test_dict, f"sources/tests/passenger_count_{passenger_count}_{i}.json")


if __name__ == "__main__":
    main()