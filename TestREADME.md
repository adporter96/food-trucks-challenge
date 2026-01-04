Note: I had to write everything and test against localhost:5001 due to some issues with my machine

Bugs:
1. Searching by status is case-sensitive. No results when searching by "Approved". I have to search with "APPROVED" instead

2. Searching with leading/trailing whitespace returns zero results instead of matching trimmed input. i.e. "   San Pancho   " should become "San Pancho"

3. Some food trucks have a latitude/longitude of 0.

4. When searching for non-existient streets and food trucks in SF, there is no error message indicating no results found. Instead it is only an empty list

5. Unable to search for food trucks by latitude - results return the same 5 food trucks with a lat/long of 0. I CAN successfully search by longitude

6. The nearest food trucks API should error if I provide a lat/long outside of San Franciso boundaries, but instead just gives me the closest 5 food trucks from whatever location I give it anywhere in the world.


Tests I Wrote:
1.  test_food_truck_search
 This one validates search queries work as expected both in a happy path scenario, and negative tests.

    * Validate we can search for food trucks by their name using a partial search term like "tacos". This should return all food trucks with the word taco or tacos in their name.

    * Validate we can also add a status to the name search and only get back food trucks with that status. A business can have many food trucks, but not all of them will be active. Some may be REQUESTED or EXPIRED

    * Validate food truck name is required - we can't search by status only

    * Validate we can search for food trucks by a the street they are on, using a partial term like "Bay". This should only return food trucks that are located on a street that have the word "bay" on the street name

    * Validate no results come back if a street name is not provided
    * Validate the requests handle whitespacing and different casings like "    San   Pancho   " and "SaN PAnChO". This one is bugged - it doesn't handle whitespacing but I left it as is to demonstrate the test should be passing but is failing due to that bug


    *Validate we get no results when searching for a food truck or street that doesn't exist in San Francisco. This one needs proper error handling. It returns an empty list instead of a message "No results found.

2. test_nearest_food_trucks.py
This one validates I can get a random food truck from the "nearest food trucks" list and cross-verify I get the same information about that food truck and all of its related food trucks.
* Validate a random food truck can be selected from whatever is near me
* Validate I can search for that same food truck by its name and get the same results
* Validate I can search for that same food truck by its address and get the same results
* Validate I can search for that same food truck by its coordinates and get the same results
*Validate I can search for that same food truck by its status and get the same results

3. test_schema.py
This is a smoke test that validates food trucks and their properties are the correct format and type


4. test_food_truck_radius
This validates the "nearest food trucks" that are returned based on a given lat/log are actually within a reasonable distance of each other and also validates the food trucks are in San Francisco and not anywhere else.

* Validates nearest food trucks are within a 5 mile radius of each other
* Validates searching from a random location outside of San Francisco returns a list of food trucks that are >=5 miles outside of San Francisco. (Found bugs on this one 5 & 6)