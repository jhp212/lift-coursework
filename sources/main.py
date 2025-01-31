from tests.loader import Passenger, load_file





class Lift:
    def __init__(self, start_floor: int, lift_id: int, max_floor: int, max_capacity):
        self.floor = start_floor
        self.max_floor = max_floor
        self.min_floor = 0 # Floor 0 is Ground Floor
        self.id = lift_id
        self.capacity = max_capacity
        self.current_capacity = 0
    
    def open_doors(self, passengers_list: list[Passenger]):
        global terminated_passengers, lift_list
        for passenger in passengers_list:
            if passenger.lift_id == self.id and passenger.end_floor == self.floor:
                passenger.boarded, passenger.lift_id = False, None
                self.current_capacity -= 1
                passengers_list.remove(passenger)
                terminated_passengers.append(passenger)
        for passenger in sorted(passengers_list, key=map(lambda x: x.passenger_id, passengers_list)):
            if self.current_capacity == self.capacity:
                break
            if passenger.start_floor == self.floor and passenger.boarded == False:
                passenger.boarded, passenger.lift_id = True, self.id
                self.current_capacity += 1


    
    def scan(self, passengers_list: list[Passenger]):
        pass
    
    def look(self, passengers_list: list[Passenger]): # !!!!PLEASE DONT JUDGE YET!!!!
        while passengers_list:
            direction = self.findDirection(passengers_list[0].start_floor)
                
            while passengers_list[0].start_floor != self.floor: #go until first priority target is reached
                self.floor += direction
                
                for passenger in passengers_list: #if there are any passengers to be picked up/dropped off while going to target, do that
                    
                    if self.floor == passenger.end_floor():
                        passenger.get_off() #im trusting your functions here
                        passengers_list.remove(passenger)
                        
                    elif self.floor == passenger.start_floor:
                        passenger.get_on(self.id) #pt 2
            
            direction = self.findDirection(passengers_list[0].end_floor) #repeat the same logic but target floor is the end goal now        
            while passengers_list[0].end_floor != self.floor:
                self.floor += direction
                
                for passenger in passengers_list:
                    
                    if self.floor == passenger.end_floor():
                        passenger.get_off()
                        passengers_list.remove(passenger)
                        
                    elif self.floor == passenger.start_floor:
                        passenger.get_on()
                        
    def findDirection(self, target_floor): #find appropriate direction based on where the highest priority floor is
        if target_floor > self.floor:
                direction = -1
        elif target_floor < self.floor:
                direction = 1
                
        return direction    


if __name__ == "__main__":
    terminated_passengers = []