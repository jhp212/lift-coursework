from tests.loader import Passenger, load_file
import time

number_of_lifts = 1 # We are allowing only one lift, so as not to struggle with threading.
test_file = "sources/tests/test1.json"


# Start import code
if __name__ == "__main__":
    try:
        max_floor, max_capacity, passenger_list = load_file(test_file)
    except ValueError as Error:
        print("Invalid test file: Reason:",Error)
        exit()
# End import code




class Lift:
    def __init__(self, start_floor: int, lift_id: int, max_floor: int, max_capacity):
        self.floor: int = start_floor
        self.max_floor: int = max_floor
        self.min_floor: int = 1 # Floor 1 is Ground Floor
        self.id: int = lift_id # So that (if we run multiple lifts), each passenger is only in one lift at once.
        self.capacity: int = max_capacity # Variable capacity
        self.current_capacity: int = 0 # Lift starts out as empty.
        self.occupants: list[Passenger] = []
    
    def open_doors(self):
        global terminated_passengers, passenger_list, start
        for passenger in passenger_list:
            if passenger.lift_id == self.id and passenger.end_floor == self.floor:
                passenger.boarded, passenger.lift_id = False, None
                self.current_capacity -= 1
                passenger_list.remove(passenger)
                terminated_passengers.append(passenger)
                self.occupants.remove(passenger)
                passenger.end_time = time.time() - start
        sorted_passenger_list: list[Passenger] = sorted(passenger_list, key=map(lambda x: x.passenger_id, passenger_list))
        for passenger in sorted_passenger_list:
            if self.current_capacity == self.capacity:
                break
            if passenger.start_floor == self.floor and passenger.boarded == False:
                passenger.boarded, passenger.lift_id = True, self.id
                self.current_capacity += 1
                self.occupants.append(passenger)
                passenger.pickup_time = time.time() - start


    
    def scan(self):
        global passenger_list # DO NOT DELETE! YOU WILL NEED THIS!!!
        pass
    
    def look(self): # !!!!PLEASE DONT JUDGE YET!!!!
        global passenger_list # This is *all* the passengers, not just the one in the lift.
        while passenger_list:
            direction = self.findDirection(passenger_list[0].start_floor)
                
            while passenger_list[0].start_floor != self.floor: #go until first priority target is reached
                self.floor += direction
                
                for passenger in passenger_list: #if there are any passengers to be picked up/dropped off while going to target, do that
                    
                    if self.floor == passenger.end_floor():
                        passenger.get_off() #im trusting your functions here
                        passenger_list.remove(passenger)
                        
                    elif self.floor == passenger.start_floor:
                        passenger.get_on(self.id) #pt 2
            
            direction = self.findDirection(passenger_list[0].end_floor) #repeat the same logic but target floor is the end goal now        
            while passenger_list[0].end_floor != self.floor:
                self.floor += direction
                
                for passenger in passenger_list:
                    
                    if self.floor == passenger.end_floor():
                        passenger.get_off()
                        passenger_list.remove(passenger)
                        
                    elif self.floor == passenger.start_floor:
                        passenger.get_on()
                        
    def findDirection(self, target_floor): #find appropriate direction based on where the highest priority floor is
        if target_floor > self.floor:
                direction = -1
        elif target_floor < self.floor:
                direction = 1
                
        return direction    


if __name__ == "__main__":
    start = time.time()
    # Start intitial setup for Lift objects
    terminated_passengers: list[Passenger] = []
    lift_list: list[Lift] = []
    for i in range(number_of_lifts):
        lift_list.append(Lift(0, i, max_floor, max_capacity))
    # End initial setup for Lift objects

    # Run specified algorithm
    target_algorithm = 'scan'
    result = eval(f'lift_list[0].{target_algorithm}()')
    