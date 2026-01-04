Bugs:
1. Searching by status is case-sensitive. No results when searching by "Approved". I have to search with "APPROVED" instead

2. Searching with leading/trailing whitespace returns zero results instead of matching trimmed input. i.e. "   San Pancho   " should become "San Pancho"

3. Some food trucks have a latitude/longitude of 0.

4. When searching for non-existient streets and food trucks in SF, there is no error message indicating no results found. Instead it is only an empty list

5. Unable to search for food trucks by latitude - results return the same 5 food trucks with a lat/long of 0. I CAN successfully search by longitude


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
