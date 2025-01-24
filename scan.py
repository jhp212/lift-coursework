def scan(start, startDirection, floors, floorCount):                #input floors as a dictionary, start direction as 'up' or 'down', start and floorcount as ints
    floors = sorted(floors.items())
    requests = floors.keys()
    remaining = requests
    waitTime = 10
    floorTime = 5
    nextFloor = 0
    time = 0
    found = False
    for i in range(requests):
        if floors[i] == start:
            nextFloor = i
            found = True
            break
    if found == False:
        if startDirection == 'up':
            nextFloor = 0
            while requests[nextFloor] < start:
                nextFloor += 1
        else:
            nextFloor = len(requests) - 1
            while requests[nextFloor] > start:
                nextFloor -= 1
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
