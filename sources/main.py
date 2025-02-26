from loader import Passenger, load_file
import time

number_of_lifts = 1 # We are allowing only one lift, so as not to struggle with threading.
floor_time = 10
doors_time = 2


# # Start import code
# if __name__ == "__main__":
#     try:
#         max_floor, max_capacity, passenger_list = load_file(test_file)
#     except Exception as Error:
#         print("Invalid test file: Reason:",Error)
#         exit()
#     target_algorithm = 'my_lift'
# # End import code




class Lift:
    def __init__(self, start_floor: int, lift_id: int, max_floor: int, max_capacity: int):
        """The lift class stores the algorithms and information such as `floor`, which is the floor it is on.

        Args:
            start_floor (int): The floor on which the lift starts
            lift_id (int): The current index of the lift_list for this lift
            max_floor (int): The maximum floor the lift can reach
            max_capacity (int): The maximum capacity of the lift
        """
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
        """Simulates the lift "opening the doors" and letting the first passengers in the queue on, regardless of direction.
        """
        global terminated_passengers, passenger_list, start, iteration_count, doors_time
        passenger_moved = False
        for passenger in passenger_list:
            if passenger.lift_id == self.id and passenger.end_floor == self.floor:
                print(f'Passenger {passenger.passenger_id} has left on floor {self.floor}!')
                passenger.boarded, passenger.lift_id = False, None
                self.current_capacity -= 1
                terminated_passengers.append(passenger)
                self.occupants.remove(passenger)
                passenger_moved = True
                passenger.end_time = iteration_count - start
        for passenger in terminated_passengers:
            if passenger in passenger_list:
                passenger_list.remove(passenger)
        sorted_passenger_list: list[Passenger] = sorted(passenger_list, key=lambda x: x.passenger_id)
        for passenger in sorted_passenger_list:
            if self.current_capacity == self.capacity:
                break
            if passenger.start_floor == self.floor and passenger.boarded == False:
                print(f'Passenger {passenger.passenger_id} has boarded on floor {self.floor}!')
                passenger.boarded, passenger.lift_id, passenger.start_time = True, self.id, iteration_count
                self.current_capacity += 1
                self.occupants.append(passenger)
                passenger_moved = True
                passenger.pickup_time = iteration_count- start
        if passenger_moved == True:
            iteration_count += doors_time

    def open_doors_directional(self, direction: int): # separate function for the scan algorithm; see below comments
        """Simulates the lift opening the doors with a display overtop indicating direction of travel, thus filtering for those going up/down

        Args:
            direction (int): The current direction of the lift
        """
        global terminated_passengers, passenger_list, start, iteration_count, doors_time
        passenger_moved = False
        for passenger in passenger_list:
            if passenger.lift_id == self.id and passenger.end_floor == self.floor:
                print(f'Passenger {passenger.passenger_id} has left on floor {self.floor}!')
                passenger.boarded, passenger.lift_id = False, None
                self.current_capacity -= 1
                terminated_passengers.append(passenger)
                self.occupants.remove(passenger)
                passenger_moved = True
                passenger.end_time = iteration_count - start
        for passenger in terminated_passengers:
            if passenger in passenger_list:
                passenger_list.remove(passenger)
        sorted_passenger_list: list[Passenger] = sorted(passenger_list, key=lambda x: x.passenger_id)
        for passenger in sorted_passenger_list:
            if self.current_capacity == self.capacity:
                break
            if passenger.start_floor == self.floor and passenger.boarded == False: # passengers should not go up if their destination is down, and vice versa
                if passenger.direction == direction: # checks that the destination is in the direction the lift is travelling else the passenger will not board
                    print(f'Passenger {passenger.passenger_id} has boarded on floor {self.floor}!')
                    passenger.boarded, passenger.lift_id, passenger.start_time = True, self.id, iteration_count
                    self.current_capacity += 1
                    self.occupants.append(passenger)
                    passenger_moved = True
                    passenger.pickup_time = iteration_count - start
        if passenger_moved == True:
            iteration_count += doors_time
    
    def scan(self):
        """Runs the "scan" algorithm, which goes up and down to the top floor without changing direction in between
        """
        global passenger_list, iteration_count, floor_time 
        direction = 1
        while passenger_list:
            if self.floor == self.min_floor:
                direction = 1 # changes direction to up if on bottom floor
            elif self.floor == self.max_floor:
                direction = -1 # changes direction to down if on top floor
            self.open_doors_directional(direction)
            self.floor += direction
            iteration_count += floor_time # increments floor in current direction, and adds time to travle to next floor




    def look(self):
        """Runs the "look" algorithm, which can change direction if theres no more direction to move
        """
        global passenger_list, iteration_count, floor_time 
        direction = 1
        while passenger_list:
            if self.floor == self.min_floor:
                direction = 1 # changes direction to up if on bottom floor
            elif self.floor == self.max_floor:
                direction = -1  # changes direction to down if on top floor
            self.open_doors_directional(direction)
            try:
                self.min_request = min(map(lambda x: x.end_floor ,self.occupants)) # finds lowest floor to either pick up or drop off passengers
                self.max_request = max(map(lambda x: x.end_floor ,self.occupants)) # finds highest floor to either pick up or drop off passengers
            except ValueError:
                try:
                    self.min_request = min(map(lambda x: x.start_floor ,passenger_list))
                    self.max_request = max(map(lambda x: x.start_floor ,passenger_list))
                except:
                    break
            if self.min_request == self.max_request:
                if self.findDirection(self.min_request) != 0:
                    direction = self.findDirection(self.min_request)
                else:
                    direction = passenger_list[0].direction
                    self.open_doors_directional(direction)
            elif self.floor <= self.min_request or self.floor <= self.min_floor:
                direction = 1 # changes direction to up if on bottom floor, or lowest requested floor
            elif self.floor >= self.max_request or self.floor >= self.max_floor:
                direction = -1 # changes direction to down if on top floor, or highest requested floor
            self.floor += direction
            iteration_count += floor_time # increments floor in current direction, and adds time to travle to next floor


    
    def my_lift(self):
        """Runs the "My lift" algorithm, which is a custom-made algorithm which utilises a sorting algorithm to attempt to do minimum moves in a greedy approach.
        """
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
            
    def findDirection(self, target_floor: int): #self explanatory really
        """Finds the direction the lift needs to travel to reach a target floor.

        Args:
            target_floor (int): The floor you want to go to

        Returns:
            int: either -1 (down), 1 (up) or 0 (same floor)
        """
        if target_floor > self.floor:
            direction = 1
        elif target_floor < self.floor:
            direction = -1
        else:
            direction  = 0        
        return direction
                                
    def calculate_priority(self,passenger_list: list[Passenger]) -> list[Passenger]:
        """This calculates a "cost" value for the passengers, and then sorts the passengers by this cost from smallest to largest.

        Args:
            passenger_list (list[Passenger]): The list of all Passengers yet to be transported to their floor

        Returns:
            list[Passenger]: This is the "sorted" list of all passengers, with the "cheapest" passenger first.
        """
        queue = [[] for passenger in passenger_list] # 2D array [[passenger, cost],...]
        for i in range(len(passenger_list)):
            if self.floor > passenger_list[i].start_floor:
                cost = (passenger_list[i].start_floor - self.floor) + (passenger_list[i].end_floor - passenger_list[i].start_floor) #as we are going down then up, we need to consider the extra distance
            else:
                cost = passenger_list[i].end_floor - self.floor # target - current
            if passenger_list[i] in self.occupants:
                cost -= self.max_floor
            
            queue[i] = [passenger_list[i],cost]
        
        prioritisedQueue = self.heap_sort(queue)
        
        return prioritisedQueue
            
    def heapify(self,arr: list, n:int, i:int) -> None:
        """Converts the un-heaped list into an in-place maximum heap using the classic `heapify` algorithm (see https://en.wikipedia.org/wiki/Heapsort#Pseudocode)

        Args:
            arr (list): The list to be converted into a heap
            n (int): The current "root" to be compared
            i (int): The index of the current value
        """
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

    def heap_sort(self,arr:list) -> list:
        """Sorts the list using heap-sort, which is an O(nlog|n|) sorting algorithm, 
        which is the most efficient time-complexity of a comparison based 
        sorting algorithm.

        Args:
            arr (list): The array to be sorted

        Returns:
            list: The sorted array 
        """
        n = len(arr)

        # Build a max heap (rearrange the array)
        for i in range(n // 2 - 1, -1, -1):
            self.heapify(arr, n, i)

        # Extract elements one by one
        for i in range(n - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]  # Swap the root with the last element
            self.heapify(arr, i, 0)  # Heapify the reduced heap    

        return arr

def run_test_file(filename, algo):
    global passenger_list, terminated_passengers, iteration_count, start
    try:
        floor_count, capacity, passenger_list = load_file(f"{filename}")
    except Exception as Error:
        print("Invalid test file: Reason:", Error)
        exit()

    lift = Lift(1, 0, floor_count, capacity)

    terminated_passengers = []

    start = 0
    iteration_count = 0
    average_journey_time = 0
    longest_journey_time = 0

    start_time = time.time()
    getattr(lift, algo)()
    real_time = time.time() - start_time

    for passenger in terminated_passengers:
        average_journey_time += passenger.end_time - passenger.start_time
        longest_journey_time = max(longest_journey_time, passenger.end_time - passenger.start_time)
    average_journey_time /= len(terminated_passengers)

    return iteration_count, average_journey_time, longest_journey_time, real_time

if __name__ == "__main__":
    print(run_test_file("sources/tests/test3.json", "scan"))