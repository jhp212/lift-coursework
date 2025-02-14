from random import randint as rng
import json
import jsbeautifier

while True:
    test_type = input("What type of test would you like?\n>>> ")
    floor_count = int(input("How many floors would you like?\n>>> "))
    total_people = int(input("How many people will there be?\n>>> "))
    capacity = int(input("How many people will the lift carry?\n>>> "))
    match test_type:
        case "random":
            if input("Do you want specific waiting (y/n)\n>>> ").lower() == "y":
                start_floor_strength: list[int] = []
                end_floor_strength: list[int] = []
                for floor in range(floor_count):
                    start_floor_strength.append(int(input(f"Relative liklihood of starting on floor {floor+1}: ")))
                for floor in range(floor_count):
                    end_floor_strength.append(int(input(f"Relative liklihood of ending on floor {floor+1}: ")))
            else:
                start_floor_strength: list[int] = [1 for i in range(floor_count)]
                end_floor_strength: list[int] = [1 for i in range(floor_count)]
            total_start = sum(start_floor_strength)
            total_end = sum(end_floor_strength)
            print("Initialised")
            total_epochs = int(input("How many different tests would you like to generate? \n>>> "))
            filename = input("What file name is this test?\n>>> ")
            if total_epochs > 1:
                start_numbering = int(input("Where should the prefix number start counting from?\n>>> "))
            for _ in range(total_epochs):
                floors: dict[str, list[int]] = {}
                for passenger in range(total_people):
                    current_start_strength = rng(1, total_start)
                    for floor in range(floor_count):
                        current_start_strength -= start_floor_strength[floor]
                        if current_start_strength <= 0:
                            break
                    start_floor = floor
                    possible_end = total_end - end_floor_strength[start_floor]
                    current_end_strength = rng(1, total_end)
                    for floor in range(floor_count):
                        if floor == start_floor:
                            continue
                        current_end_strength -= end_floor_strength[floor]
                        if current_end_strength <= 0:
                            break
                    end_floor = floor
                    if str(start_floor+1) in floors:
                        floors[str(start_floor+1)].append(end_floor+1)
                    else:
                        floors[str(start_floor+1)] = [end_floor+1]
                keys = sorted(map(int, floors.keys()))
                sorted_floors: dict[str:list[int]] = {}
                for key in keys:
                    sorted_floors[str(key)] = floors[str(key)]
                result_dict = {"floor_count":floor_count,"capacity":capacity,"floor_requests":sorted_floors}
                with open(f"sources/tests/{filename}{_ + start_numbering}.json",'w') as jsonfile:
                    options = jsbeautifier.default_options()
                    options.indent_size = 4
                    result = jsbeautifier.beautify(json.dumps(result_dict))
                    jsonfile.write(result)
                    jsonfile.close()
        case "best":
            floors: dict[str,list[int]] = {}
            total = total_people
            current_floor = 1
            while total_people > 0:
                if current_floor == 1:
                    direction = 1
                elif current_floor == floor_count:
                    direction = -1
                for i in range(min(capacity,total_people)):
                    if str(current_floor) in floors:
                        floors[str(current_floor)].append(current_floor+direction)
                    else:
                        floors[str(current_floor)] = [current_floor+direction]
                total_people -= min(capacity,total_people)
                current_floor += direction
            result_dict = {"floor_count":floor_count,"capacity":capacity,"floor_requests":floors}
            with open(f"sources/tests/best-{floor_count}-floors-{total}-people-{capacity}-capacity.json",'w') as jsonfile:
                options = jsbeautifier.default_options()
                options.indent_size = 4
                result = jsbeautifier.beautify(json.dumps(result_dict))
                jsonfile.write(result)
                jsonfile.close()
        case _:
            print("Sorry! That's not been implemented yet!")
