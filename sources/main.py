

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


class Lift:
    def __init__(self, start_floor: int, lift_id: int, max_floor: int):
        self.floor = start_floor
        self.max_floor = max_floor
        self.min_floor = 0 # Floor 0 is Ground Floor
        self.id = lift_id
    
    def scan(self, passengers_list: list[Passenger]):
        pass
    
    def look(self, passengers_list: list[Passenger]):
        pass
