import json

def load_file(path:str):
    with open(path, "r") as file:
        data = json.load(file)
    
    if data["floor_count"] < len(data["floor_requests"]):
        raise ValueError("Too many floors given!")
    
    passenger_list = []
    for floor in data["floor_requests"]:
        for end_floor in data["floor_requests"][floor]:
            passenger_list.append(Passenger(int(floor), end_floor, len(passenger_list)))

    return data["floor_count"], data["capacity"], passenger_list


class Passenger:
    def __init__(self, start_floor: int, end_floor: int, passenger_id: int):
        self.start_floor, self.end_floor, self.start_time = start_floor, end_floor, 0
        self.boarded, self.lift_id = False, None
        self.passenger_id = passenger_id
        self.direction = -1 if start_floor - end_floor > 0 else 1
    
    def get_on(self, lift_id: int):
        self.boarded = True
        self.lift_id = lift_id
    
    def get_off(self):
        global lift_list # list[Lift]
        if lift_list[self.lift_id].floor == self.end_floor:
            self.boarded = False
            self.lift_id = None
            global iteration_count # int
            self.end_time = iteration_count
            return True
        else:
            return False
        
if __name__ == "__main__":
    floor_count, capacity, passenger_list = load_file("sources/tests/test3.json")
    print(floor_count)
    print(capacity)
    for passenger in passenger_list:
        print((passenger.start_floor, passenger.end_floor))
    