from loader import Passenger, load_file
from bulk_testmaker import generate_test_dict, save_dict_as_json, generate_tests
import time, jsbeautifier, os, json
import matplotlib.pyplot as plt

# check if the user is accessing from a GUI
# if so, import tkinter
try:
    import tkinter
    from tkinter import filedialog
    gui_available = True
except ImportError:
    gui_available = False

tkinter.Tk().withdraw()

options = jsbeautifier.default_options()
options.indent_size = 4

floor_time = 10
doors_time = 2

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
                # print(f'Passenger {passenger.passenger_id} has left on floor {self.floor}!')
                passenger.boarded, passenger.lift_id = False, None
                self.current_capacity -= 1
                terminated_passengers.append(passenger)
                self.occupants.remove(passenger)
                passenger_moved = True
                passenger.end_time = iteration_count
        for passenger in terminated_passengers:
            if passenger in passenger_list:
                passenger_list.remove(passenger)
        sorted_passenger_list: list[Passenger] = sorted(passenger_list, key=lambda x: x.passenger_id)
        for passenger in sorted_passenger_list:
            if self.current_capacity == self.capacity:
                break
            if passenger.start_floor == self.floor and passenger.boarded == False:
                # print(f'Passenger {passenger.passenger_id} has boarded on floor {self.floor}!')
                passenger.boarded, passenger.lift_id = True, self.id
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

        # let off passengers
        for passenger in self.occupants[:]:
            if passenger.end_floor == self.floor:
                # print(f'Passenger {passenger.passenger_id} has left on floor {self.floor}!')
                self.current_capacity -= 1
                terminated_passengers.append(passenger)
                self.occupants.remove(passenger)
                passenger.boarded, passenger.lift_id = False, None
                passenger_moved = True
                passenger.end_time = iteration_count

        # let on passengers
        for passenger in passenger_list[:]:
            if self.current_capacity == self.capacity:
                break
            if passenger.start_floor == self.floor and passenger.boarded == False:
                if passenger.direction == direction: # checks that the destination is in the direction the lift is travelling else the passenger will not board
                    # print(f'Passenger {passenger.passenger_id} has boarded on floor {self.floor}!')
                    passenger.boarded, passenger.lift_id = True, self.id
                    passenger.pickup_time = iteration_count - start
                    self.current_capacity += 1
                    self.occupants.append(passenger)
                    passenger_list.remove(passenger)
                    passenger_moved = True
                    
        if passenger_moved == True:
            iteration_count += doors_time
    
    def check_requests_in_current_direction(self, direction: int):
        """Checks if there are any passengers waiting in the current direction

        Args:
            direction (int): the current direction of the lift

        Returns:
            bool: Whether there are any passengers waiting in the current direction or not
        """

        global passenger_list
        passenger_waiting_in_direction = True
        if self.floor != self.max_floor and self.floor != 1 and not self.occupants:
            passenger_waiting_in_direction = False
            if direction == 1:
                for passenger in passenger_list:
                    if passenger.start_floor in range(self.floor + 1, self.max_floor + 1):
                        passenger_waiting_in_direction = True
                        break
            elif direction == -1:
                for passenger in passenger_list:
                    if passenger.start_floor in range(1, self.floor):
                        passenger_waiting_in_direction = True
                        break

        return passenger_waiting_in_direction
    
    def scan(self):
        """Runs the "scan" algorithm, which goes up and down to the top floor without changing direction in between
        """
        global passenger_list, iteration_count, floor_time 
        direction = 1
        while passenger_list or self.occupants:
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
        while passenger_list or self.occupants:
            self.open_doors_directional(direction)
            if self.floor == self.min_floor:
                direction = 1 # changes direction to up if on bottom floor
                self.open_doors_directional(direction)
            elif self.floor == self.max_floor:
                direction = -1  # changes direction to down if on top floor
                self.open_doors_directional(direction)

            passenger_waiting_in_direction = self.check_requests_in_current_direction(direction)
            if not passenger_waiting_in_direction:
                direction *= -1
                self.open_doors_directional(direction)

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

def run_test_file(path, algorithm):
    """Runs a given .json test file

    Args:
        path (str): The location of the test file
        algo (str): The algorithm to be used

    Returns:
        tuple: Returns (iteration_count, average_journey_time, longest_journey_time, real_time)
    """

    global passenger_list, terminated_passengers, iteration_count, start
    try:
        floor_count, capacity, passenger_list = load_file(f"{path}")
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
    getattr(lift, algorithm)()
    real_time = time.time() - start_time

    for passenger in terminated_passengers:
        average_journey_time += passenger.end_time - passenger.pickup_time
        longest_journey_time = max(longest_journey_time, passenger.end_time - passenger.pickup_time)
    average_journey_time /= len(terminated_passengers)

    return iteration_count, average_journey_time, longest_journey_time, real_time


def run_range_of_tests(param_values, file_pattern, xlabel):
    """A general function to run a range of tests for a given parameter

    Args:
        param_values (list): The list of values to be tested
        file_pattern (str): The pattern of the test files
        xlabel (str): The label for the x-axis on the graph
    """
    
    algorithms = ["look", "scan",]
    results = {algo: [[], [], [], []] for algo in algorithms}

    # Check if data.json exists, and load existing data
    if os.path.exists(f"results/data/{xlabel}.json"):
        with open(f"results/data/{xlabel}.json", "r") as f:
            data = json.load(f)
    else:
        data = {}

    # Ensure top-level key exists
    if xlabel not in data:
        data[xlabel] = {}

    for algorithm in algorithms:
        for value in param_values:
            average_total_time, average_individual_time, average_longest_wait, average_real_time = 0, 0, 0, 0
            for i in range(10):

                algo_time, average_wait, longest_wait, real_time = run_test_file(file_pattern.format(value, i), algorithm)

                average_total_time += algo_time
                average_individual_time += average_wait
                average_longest_wait += longest_wait
                average_real_time += real_time
                
                print(f"Ran file {file_pattern.format(value, i)} with {algorithm}")

            # Compute averages
            average_total_time /= 10
            average_individual_time /= 10
            average_longest_wait /= 10
            average_real_time /= 10

            # Store in results for plotting
            values = [average_total_time, average_individual_time, average_longest_wait, average_real_time]
            for i, data_point in enumerate(values):
                results[algorithm][i].append(data_point)
            
            value_str = str(value)
            if value_str not in data[xlabel]:
                data[xlabel][value_str] = {}
            
            data[xlabel][value_str][algorithm] = {
                "average_total_time": average_total_time,
                "average_individual_time": average_individual_time,
                "average_longest_wait": average_longest_wait,
                "average_real_time": average_real_time
            }

    # Save data to JSON files
    with open(f"results/data/{xlabel}.json", "w") as f:
        json.dump(data, f, indent=4)

    # Plot results
    plt.rc("font", size=10)

    fig, axs = plt.subplots(2, 2, figsize=(12, 9))

    markers = ["o","s","^"]
    for i, algorithm in enumerate(algorithms):
        for j, ax in enumerate(axs.flat):
            ax.plot(param_values, results[algorithm][j], label=algorithm, alpha=0.7, marker=markers[i], markersize=3)

    for i, ax in enumerate(axs.flat):
        ax.legend()
        ax.set_xlabel(xlabel)
        if i in [0, 1, 2]:
            ax.set_ylabel("Time Taken (Hypothetical seconds)")
        else:
            ax.set_ylabel("Time Taken (Real seconds)")

    axs[0, 0].set_title("Average Total Time")
    axs[0, 1].set_title("Average Individual Time")
    axs[1, 0].set_title("Average Longest Wait")
    axs[1, 1].set_title("Average Real Time")

    title = f"Time Taken for varying {xlabel}"
    plt.savefig(f"results/charts/{title}.svg", format="svg", dpi=600)

    match xlabel:
        case "Capacity":
            title += "\nFloor Count = 20, Passenger Count = 1000"
        case "Floor Count":
            title += "\nCapacity = 5, Passenger Count = 1000"
        case "Passenger Count":
            title += "\nCapacity = 5, Floor Count = 20"
    fig.suptitle(title)

    plt.show()

def print_results(iteration_count, average_journey_time, longest_journey_time, real_time):
    """Prints out the results of the test in a readable format

    Args:
        iteration_count (int): The total time in "seconds"
        average_journey_time (float): The average journey time
        longest_journey_time (float): The longest journey time
        real_time (float): The real time taken to run the algorithm
    """

    print("Results:")
    print(f"Total time in 'seconds': {iteration_count}")
    print(f"Average journey time: {average_journey_time}")
    print(f"Longest journey time: {longest_journey_time}")
    print(f"Real time: {real_time}")



if __name__ == "__main__":
    print("Welcome to the Lift Simulator!")
    
    while True:
        choice = input("Would you like to:\na) Run a specific test file\nb) Generate a test file\nc) Test all algorithms over a range of tests and view graphs\nx) Exit\n>>> ").lower()

        match choice:
            case "x": exit()

            case "a":
                if gui_available:
                    path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")], title="Select a test file")
                else:
                    path = input("\nEnter the path to the test file\n>>> ")

                if not path:
                    continue

                algorithm = input("\nWhich algorithm would you like to run?\na) SCAN\nb) LOOK\nc) MYLIFT\n>>> ")
                algorithms = {"a": "scan", "b": "look", "c": "my_lift"}

                if algorithm.lower() not in algorithms:
                    continue

                iteration_count, average_journey_time, longest_journey_time, real_time = run_test_file(path, algorithms[algorithm.lower()])
                print_results(iteration_count, average_journey_time, longest_journey_time, real_time)
            
            
            case "b":
                try:
                    floor_count = int(input("\nHow many floors are there?\n>>> "))
                    capacity = int(input("How many people can the lift carry?\n>>> "))
                    passenger_count = int(input("How many people will there be?\n>>> "))
                except ValueError:
                    print("Invalid input")
                    continue

                if gui_available:
                    print("Select a save location...")
                    path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")], title="Select a save location")
                else:
                    path = input("\nEnter the path to save the test file (e.g. folder/test.json)\n>>> ")
                    path = os.path.abspath(path)

                if not path:
                    continue

                data = generate_test_dict(floor_count, capacity, passenger_count)
                save_dict_as_json(data, path)


            case "c":
                choice = input("\nWould you like to:\na) Test all algorithms over a range of tests\nb) Generate a lot of test files\n>>> ").lower()

                match choice:
                    case "a":
                        print("\nThis function will analyse the performance of all algorithms over a range of tests.")
                        print("This will take a while, so please be patient.")
                        choice = input("\nWould you like to:\na) Analyse varying capacity\nb) Analyse varying floor count\nc) Analyse varying passenger count\n>>> ").lower()
                        match choice:
                            case "a":
                                print("\nThe default values are:\nNumber of Floors = 20\nNumber of passengers = 1000")
                                
                                begin = input("Would you like to start the tests? (y/n)\n>>> ").lower()
                        
                                if begin != "y":
                                    continue
                                
                                try:
                                    run_range_of_tests(range(2, 50), "sources/tests/capacity_{}_{}.json", "Capacity")
                                except FileNotFoundError:
                                    print("You have not generated the test files. Please create them and try again.")

                            case "b":
                                print("The default values are:\nCapacity = 5\nNumber of passengers = 1000")

                                begin = input("Would you like to start the tests? (y/n)\n>>> ").lower()

                                if begin != "y":
                                    continue
                                
                                try:
                                    run_range_of_tests(range(2, 100), "sources/tests/floor_count_{}_{}.json", "Floor Count")
                                except FileNotFoundError:
                                    print("You have not generated the test files. Please create them and try again.")

                            case "c":
                                print("The default values are:\nCapacity = 5\nNumber of Floors = 20")

                                begin = input("Would you like to start the tests? (y/n)\n>>> ").lower()

                                if begin != "y":
                                    continue
                                
                                try:
                                    run_range_of_tests(range(10, 1010, 10), "sources/tests/passenger_count_{}_{}.json", "Passenger Count")
                                except FileNotFoundError:
                                    print("You have not generated the test files. Please create them and try again.")
                            case _:
                                continue


                    case "b":
                        current_dir = os.getcwd()
                        path = os.path.join(current_dir, "sources", "tests")
                        print(f"!!! WARNING !!!\nThis will generate a lot of test files (2400+) in this folder:\n{path}\nThis may take a long time.\nIf these files already exist, they will not be overwritten.\nAre you sure you want to continue? (y/n)")
                        if input(">>> ").lower() != "y":
                            continue

                        generate_tests()
                        print("Done!")