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
    def open_doors_scan(self, direction): # separate function for the scan algorithm; see below comments
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
            if passenger.start_floor == self.floor and passenger.boarded == False: # passengers should not go up if their destination is down, and vice versa
                if passenger.direction == direction: # checks that the destination is in the direction the lift is travelling else the passenger will not board
                    passenger.boarded, passenger.lift_id = True, self.id
                    self.current_capacity += 1
                    self.occupants.append(passenger)
                    passenger.pickup_time = time.time() - start


    
    def scan(self):
        global passenger_list # DO NOT DELETE! YOU WILL NEED THIS!!!
        direction = self.findDirection(passenger_list[0].start_floor) # initialising; discuss whether to let user define, or generate automatically as here
        while passenger_list:
            
            while self.floor != self.max_floor and self.floor != self.min_floor:
                self.floor += direction
                self.open_doors_scan(self, direction)
            
            if self.floor == self.min_floor:
                self.direction = 1
            elif self.floor == self.max_floor:
                self.direction = -1



    
    def look(self):
        global passenger_list # This is *all* the passengers, not just the one in the lift.
            
        while passenger_list:
            queue = self.calculate_priority(passenger_list)  
            currentPassenger = queue[0][0]
            while self.floor != currentPassenger.start_floor:
                direction = self.findDirection(currentPassenger.start_floor)
                self.floor += direction
            currentPassenger.get_on()
                while self.floor != currentPassenger.end_floor:
                direction = self.findDirection(currentPassenger.end_floor)
                self.floor += direction
                currentPassenger.get_off()
            
    def findDirection(self, target_floor): #self explanatory really
        if target_floor > self.floor:
                direction = -1
        elif target_floor < self.floor:
                direction = 1
                
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
    