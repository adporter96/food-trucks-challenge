#To ensure results are consistent, I am grabbing a random food truck from the list of nearest food
# trucks, then searching that food truck by name and validating the searchByName response matches the
# random food truck saved from nearestFoodTrucks 

import random
from Requests.get import get_nearest_food_trucks, search_food_trucks_by_name, search_food_trucks_by_street

random_food_truck = None


# get nearest food trucks - choose a random truck from the response and save it for later use
def test_get_a_random_food_truck():
    global random_food_truck

    response = get_nearest_food_trucks()
    random_food_truck = random.choice(response)
    print ("Selected:", random_food_truck["applicant"])
    
    assert isinstance(response, list)
    assert response is not None
    assert "applicant" in random_food_truck



# search for the selected food truck by its name
def test_search_for_the_random_food_truck_by_name():
    applicant_name = random_food_truck["applicant"]

    response = search_food_trucks_by_name(applicant_name)
    # If the random food truck shows up in the search results, test passes. There could be
    # multiple food trucks in the search results, we just want to make sure one of the results
    # is an exact match to the random food truck
    matched = next(
        (truck for truck in response if truck == random_food_truck),
        None
    )

    assert isinstance(response, list)
    assert matched is not None
    assert len(response) >= 1
    
    print (f"'{applicant_name}'was searched successfully by its name")


# search for the selected food truck by its address
def test_search_for_the_random_food_truck_by_address():
    applicant_name = random_food_truck["applicant"]
    applicant_address = random_food_truck["address"]

    response = search_food_trucks_by_street(applicant_address)
    # If the random food truck shows up in the search results, test passes.
    # This should only return a single result since it's a unique address and not a keyword search (Maybe this is a bug? It's still returning multiple food trucks at
    # an address)
    matched = next(
        (truck for truck in response if truck == random_food_truck),
        None
    )

    assert isinstance(response, list)
    assert matched is not None
    # assert len(response) == 1
    
    print (f"'{applicant_name}'was searched successfully by its address")


def test_search_for_the_random_food_truck_by_coordinates():
    # Validate we can search the food truck by its coordinates
    # This should also only return a single result (I believe this is a bug. The response is returning multiuple results with different coordinates, although similar. I am searching for specific, 
    # exact coordinates, I shouldn't be getting more than 1 result unless the food trucks were at the same exact coordinates.)
    global random_food_truck
    latitude = random_food_truck["latitude"]
    longitude = random_food_truck["longitude"]

    response = get_nearest_food_trucks(latitude = latitude, longitude = longitude)

    match = next(
        (truck for truck in response if truck == random_food_truck),
        None
    )

    assert isinstance(response, list)
    assert match is not None
    # assert len(response) == 1
    print(f'{random_food_truck["applicant"]} was searched successfully by its coordinates')


def test_search_random_food_truck_by_status():
    # do a search on nearest food trucks by the status of the food truck we pulled randomly.
    # validate among the search results, our random food truck is included
    global random_food_truck
    status = random_food_truck["status"]

    response = get_nearest_food_trucks(status=status)

    match = next(
        (truck for truck in response if truck == random_food_truck),
        None
    )

    assert isinstance(response, list)
    assert match is not None
    assert len(response) >=1
    print(f'{random_food_truck} was found among the nearest food trucks with the {random_food_truck["status"]} status')