from tests.loader import Passenger, load_file
import time

number_of_lifts = 1 # We are allowing only one lift, so as not to struggle with threading.
test_file = "sources/tests/test1.json"
floor_time = 10
doors_time = 2


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
        self.max_request: int = 1 # all floors should be higher than this, so it will be overwritten; useful for look algorithm
        self.min_request: int = max_floor # all floors lower or equal, so this will be overwritten
    
    def open_doors(self):
        global terminated_passengers, passenger_list, start, iteration_count, doors_time
        for passenger in passenger_list:
            if passenger.lift_id == self.id and passenger.end_floor == self.floor:
                print(f'Passenger {passenger.passenger_id} has left on floor {self.floor}!')
                passenger.boarded, passenger.lift_id = False, None
                self.current_capacity -= 1
                passenger_list.remove(passenger)
                terminated_passengers.append(passenger)
                self.occupants.remove(passenger)
                passenger.end_time = iteration_count - start
        sorted_passenger_list: list[Passenger] = sorted(passenger_list, key=lambda x: x.passenger_id)
        for passenger in sorted_passenger_list:
            if self.current_capacity == self.capacity:
                break
            if passenger.start_floor == self.floor and passenger.boarded == False:
                print(f'Passenger {passenger.passenger_id} has boarded on floor {self.floor}!')
                passenger.boarded, passenger.lift_id = True, self.id
                self.current_capacity += 1
                self.occupants.append(passenger)
                passenger.pickup_time = iteration_count- start
        iteration_count += doors_time
    def open_doors_scan(self, direction): # separate function for the scan algorithm; see below comments
        global terminated_passengers, passenger_list, start, iteration_count, doors_time
        for passenger in passenger_list:
            if passenger.lift_id == self.id and passenger.end_floor == self.floor:
                print(f'Passenger {passenger.passenger_id} has left on floor {self.floor}!')
                passenger.boarded, passenger.lift_id = False, None
                self.current_capacity -= 1
                passenger_list.remove(passenger)
                terminated_passengers.append(passenger)
                self.occupants.remove(passenger)
                passenger.end_time = iteration_count - start
        sorted_passenger_list: list[Passenger] = sorted(passenger_list, key=lambda x: x.passenger_id)
        for passenger in sorted_passenger_list:
            if self.current_capacity == self.capacity:
                break
            if passenger.start_floor == self.floor and passenger.boarded == False: # passengers should not go up if their destination is down, and vice versa
                if passenger.direction == direction: # checks that the destination is in the direction the lift is travelling else the passenger will not board
                    print(f'Passenger {passenger.passenger_id} has boarded on floor {self.floor}!')
                    passenger.boarded, passenger.lift_id = True, self.id
                    self.current_capacity += 1
                    self.occupants.append(passenger)
                    passenger.pickup_time = iteration_count - start
        iteration_count += doors_time
    def open_doors_look(self, direction): # separate function for the look algorithm; see below changes
        global terminated_passengers, passenger_list, start, iteration_count, doors_time
        for passenger in passenger_list:
            if passenger.lift_id == self.id and passenger.end_floor == self.floor:
                print(f'Passenger {passenger.passenger_id} has left on floor {self.floor}!')
                passenger.boarded, passenger.lift_id = False, None
                self.current_capacity -= 1
                passenger_list.remove(passenger)
                terminated_passengers.append(passenger)
                self.occupants.remove(passenger)
                passenger.end_time = iteration_count - start
        sorted_passenger_list: list[Passenger] = sorted(passenger_list, key=lambda x: x.passenger_id)
        for passenger in sorted_passenger_list:
            if self.current_capacity == self.capacity:
                break
            if passenger.start_floor == self.floor and passenger.boarded == False: # passengers should not go up if their destination is down, and vice versa
                if passenger.direction == direction: # checks that the destination is in the direction the lift is travelling else the passenger will not board
                    print(f'Passenger {passenger.passenger_id} has boarded on floor {self.floor}!')
                    passenger.boarded, passenger.lift_id = True, self.id
                    if passenger.end_floor > self.max_request: #extra clauses to set the highest point the lift should go to before changing direction
                        self.max_request = passenger.end_floor
                    elif passenger.end_floor < self.min_request: #lowest floor the lift should go to before turning
                        self.min_request = passenger.end_floor
                    self.current_capacity += 1
                    self.occupants.append(passenger)
                    passenger.pickup_time = iteration_count - start
        iteration_count += doors_time


    
    def scan(self):
        global passenger_list, iteration_count, floor_time # DO NOT DELETE! YOU WILL NEED THIS!!!
        direction = 1
        while passenger_list:
            self.open_doors_scan(direction)
            if self.floor == self.min_floor:
                direction = 1
            elif self.floor == self.max_floor:
                direction = -1
            self.floor += direction
            iteration_count += floor_time




    def look(self):
        global passenger_list, iteration_count, floor_time 
        direction = 1
        for passenger in passenger_list:
            if passenger.start_floor > self.max_request:
                self.max_request = passenger.start_floor
            elif passenger.start_floor < self.min_request:
                self.min_request = passenger.start_floor
        while passenger_list:
            self.open_doors_look(direction)
            if self.floor == self.min_request:
                direction = 1
            elif self.floor == self.max_request:
                direction = -1
            self.floor += direction
            iteration_count += floor_time


    
    def my_lift(self):
        global passenger_list, iteration_count, floor_time # This is *all* the passengers, not just the one in the lift.
            
        while passenger_list:
            queue = self.calculate_priority(passenger_list)  
            currentPassenger = queue[0][0]
            while self.floor != currentPassenger.start_floor:
                direction = self.findDirection(currentPassenger.start_floor)
                self.floor += direction
                iteration_count += floor_time
            self.open_doors()
            while self.floor != currentPassenger.end_floor:
                direction = self.findDirection(currentPassenger.end_floor)
                self.floor += direction
                iteration_count += floor_time
            self.open_doors()
            
    def findDirection(self, target_floor): #self explanatory really
        if target_floor > self.floor:
                direction = 1
        elif target_floor < self.floor:
                direction = -1
                
        return direction
                                
    def calculate_priority(self,passenger_list):
        queue = [[] for passenger in passenger_list] # 2D array [[passenger, cost],...]
        for i in range(len(passenger_list)):
            if self.floor > passenger_list[i].start_floor:
                cost = (passenger_list[i].start_floor - self.floor) + (passenger_list[i].end_floor - passenger_list[i].start_floor) #as we are going down then up, we need to consider the extra distance
            else:
                cost = passenger_list[i].end_floor - self.floor # target - current
            
            queue[i] = [passenger_list[i],cost]
        
        prioritisedQueue = self.heap_sort(queue)
        
        return prioritisedQueue
            
    def heapify(self,arr, n, i):
        largest = i  # Initialize the largest as root
        left = 2 * i + 1  # Left child index
        right = 2 * i + 2  # Right child index

        # If left child exists and is greater than root
        if left < n and arr[left][1] > arr[largest][1]:
            largest = left

        # If right child exists and is greater than largest so far
        if right < n and arr[right][1] > arr[largest][1]:
            largest = right

        # If largest is not root, swap and continue heapifying
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]  # Swap
            self.heapify(arr, n, largest)  # Heapify the affected subtree

    def heap_sort(self,arr):
        n = len(arr)

        # Build a max heap (rearrange the array)
        for i in range(n // 2 - 1, -1, -1):
         self.heapify(arr, n, i)

        # Extract elements one by one
        for i in range(n - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]  # Swap the root with the last element
            self.heapify(arr, i, 0)  # Heapify the reduced heap    

        return arr

            
                        

if __name__ == "__main__":
    start = 0
    iteration_count = 0
    # Start intitial setup for Lift objects
    terminated_passengers: list[Passenger] = []
    lift_list: list[Lift] = []
    for i in range(number_of_lifts):
        lift_list.append(Lift(1, i, max_floor, max_capacity))
    # End initial setup for Lift objects

    # Run specified algorithm
    target_algorithm = 'my_lift'
    start_time = time.time()
    result = eval(f'lift_list[0].{target_algorithm}()')
    end_time = time.time()
    print(f'{target_algorithm} algorithm took {iteration_count} "seconds" (iterations) to run.')
    print(f'{target_algorithm} algorithm took {end_time - start_time} real-time seconds to run.')