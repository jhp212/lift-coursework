'''

Dear Thomas,

We're gonna try something different. Please see main.py for the new "Lift" class, which includes a scan() function.

We use a Passenger class rather than a dictionary for requests.

The lift has several in-built variables, such as:

self.max_floor
self.min_floor
self.floor (This is current floor)
self.lift_if (The index in lift_list which this lift is)
self.open_doors() (This opens the door and lets off all Passengers.)

'''





def scan(start: int, startDirection: str, floors: dict, floorCount: int):                #input floors as a dictionary, start direction as 'up' or 'down', start and floorcount as ints
    # Initialise 
    floors = sorted(floors.items()) # floors is now a list
    requests = floors.keys() # This will result in an error
    remaining = requests
    waitTime = 10
    floorTime = 5
    nextFloor = 0
    time = 0
    found = False

    # WTH is this
    for i in range(requests):
        if floors[i] == start:
            nextFloor = i
            found = True
            break
    
    #
    if found == False:
        if startDirection == 'up':
            nextFloor = 0
            while requests[nextFloor] < start:
                nextFloor += 1
        else:
            nextFloor = len(requests) - 1
            while requests[nextFloor] > start:
                nextFloor -= 1
    
    #
    if startDirection == 'up':
        if found == True:
            time += waitTime
            remaining.append(floors[nextFloor])
            remaining = sorted(remaining)
            nextFloor += 1
        time += (remaining[nextFloor] - start) * floorTime
        current = remaining[nextFloor]
        while len(requests) > 0:
            time += (remaining[nextFloor] - current) * floorTime
