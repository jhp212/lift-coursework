import json

class Passenger:
    def __init__(self, start_floor: int, end_floor: int, passenger_id: int):
        """Generates a `Passenger` class to store the data

        Args:
            start_floor (int): The starting floor of this passenger
            end_floor (int): The target floor of this passenger
            passenger_id (int): The passenger id, to differentiate different passengers that would otherwise be identical.
        """
        self.start_floor, self.end_floor, self.start_time = start_floor, end_floor, 0
        self.boarded, self.lift_id = False, None
        self.passenger_id = passenger_id
        self.direction = -1 if start_floor - end_floor > 0 else 1
        self.pickup_time = None
        self.end_time = None


def load_file(path:str) -> tuple[int, int, list[Passenger]]:
    """Loads the current file into the necessary data to run main.py

    Args:
        path (str): The path for the .json file

    Raises:
        KeyError: if floor_count does not exist
        KeyError: if capacity does not exist
        KeyError: if the floor_requests do not exist
        TypeError: if the floor_count is not an integer type
        TypeError: if the capacity is not an integer type
        ValueError: if floor_count is not a natural number
        ValueError: if capacity is not a natural number
        ValueError: if any passengers attempt to go to a higher floor than max_floor
        ValueError: if any passenger's target floor is not an integer

    Returns:
        tuple: Returns (floor_count, max_capacity, passenger_list), where:
            - `floor_count` is the number of floors
            - `max_capacity` is the maximum capacity the lift can transport at any one time
            - `passenger_list` is the list of Passenger classes representing the people needing to be transported.
    """
    # load json file as a python dictionary
    with open(path, "r") as file:
        data = json.load(file)
    
    #checking keys exists in the file
    if "floor_count" not in data:
        raise KeyError("floor_count does not exist!")
    if "capacity" not in data:
        raise KeyError("capacity does not exist!")
    if "floor_requests" not in data:
        raise KeyError("floor_requests does not exist!")
    
    #checking data types
    if type(data["floor_count"]) != int:
        raise TypeError("Floor count must be an integer!")
    if type(data["capacity"]) != int:
        raise TypeError("Capacity must be an integer!")
    
    #checking values are greater than 0
    if data["floor_count"] <= 0:
        raise ValueError("Floor count is <= 0")
    if data["capacity"] <= 0:
        raise ValueError("Capacity is <= 0")
    
    
    passenger_list = []
    for floor in data["floor_requests"]:
        try:
            if int(floor) > data["floor_count"]:
                raise ValueError(f"There is a passenger waiting on floor {floor} which is greater than the floor count!")
            
        except ValueError:
            raise ValueError("Floor values must be integers inside strings! e.g '2'")
        
        for end_floor in data["floor_requests"][floor]:
            if int(end_floor) > data["floor_count"]:
                raise ValueError(f"There is a passenger wanting to go to floor {end_floor} which is greater than the floor count!")
            passenger_list.append(Passenger(int(floor), end_floor, len(passenger_list)))

    return data["floor_count"], data["capacity"], passenger_list

    
        
if __name__ == "__main__":
    floor_count, capacity, passenger_list = load_file("sources/tests/test3.json")
    print(floor_count)
    print(capacity)
    for passenger in passenger_list:
        print((passenger.start_floor, passenger.end_floor))
    int("2.3")