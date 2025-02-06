# We need to discuss what to base the priority queue on, currently it is based on the total distance the lift will have to travel to take the passenger from their start_floor to their end_floor
# I used heap sort for the priority queue, obviously the cost of each passenger changs as we travel so calculate_priority() will have to run periodically
# This is still incomplete (lol), but the rest is trivial really. Only need to make te lift move and open the doors every time we are at a target
# I've noticed you guys have made some changes to the structures as well so I'll integrate those into my code 

    def look(self):
            global passenger_list # This is *all* the passengers, not just the one in the lift.
            queue = self.calculate_priority(passenger_list)  
            #                                              #
                            TO BE COMPLETED
            #                                              #
            
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
