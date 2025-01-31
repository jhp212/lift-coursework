import json

def load_file(path:str):
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
            passenger_list.append(Passenger(int(floor), end_floor, len(passenger_list)))

    return data["floor_count"], data["capacity"], passenger_list


class Passenger:
    def __init__(self, start_floor: int, end_floor: int, passenger_id: int):
        self.start_floor, self.end_floor, self.start_time = start_floor, end_floor, 0
        self.boarded, self.lift_id = False, None
        self.passenger_id = passenger_id
        self.direction = -1 if start_floor - end_floor > 0 else 1
    
        
if __name__ == "__main__":
    floor_count, capacity, passenger_list = load_file("sources/tests/test3.json")
    print(floor_count)
    print(capacity)
    for passenger in passenger_list:
        print((passenger.start_floor, passenger.end_floor))
    int("2.3")