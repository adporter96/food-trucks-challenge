import pytest
import requests
from Requests.get import get_nearest_food_trucks, search_food_trucks_by_name, search_food_trucks_by_street

global_search_term = "TACOS"
global_search_status = "APPROVED"
global_street_term = "BAY"


# Do a partial/keyword search. Validate all Food trucks that return 
# include the keyword we are searching by. It should also be case-insensitive
# If any trucks don't have the search term, output a list of those trucks.
def test_search_food_trucks_by_patrial_term():
    print("When searching for food trucks with a partial name")
    term = global_search_term
    response = search_food_trucks_by_name(term)
    
    assert isinstance(response, list)
    assert len(response) > 0

    missing_search_term = []
    for truck in response:
        applicant = truck.get("applicant", "")
        if term.lower() not in applicant.lower():
            missing_search_term.append(applicant)
    
    if missing_search_term:
        raise AssertionError(
            f"The following food truck(s) should not be in the list: {missing_search_term}"
        )
    
    print("All results include the partial search term")

# Search with a status. All results should have that status. Output a list of trucks that have mismatched
# statuses
def test_search_by_name_with_status():
    print("when searching for food trucks by both name and status")
    term = global_search_term
    status = global_search_status
    response = search_food_trucks_by_name(term, status)

    assert isinstance(response, list)
    assert len(response) > 0

    incorrect_status = []

    for truck in response: 
        applicant = truck.get("applicant", "")
        truck_status = truck.get("status")
        
        if truck_status != status:
            incorrect_status.append(
                {"applicant": applicant, "status": truck_status}
            )
    if incorrect_status:
        raise AssertionError(
            f"The following food truck(s) do not match the expected status of {status}: {incorrect_status}"
        )
    
    print ("All results match the specified status")


# Try searching with only status (name missing). Validate name is required.
def test_search_by_status_only():
    print("When searching for a food truck by status only")
    term = ""
    status = global_search_status

    with pytest.raises(requests.exceptions.HTTPError) as err_info:
        search_food_trucks_by_name(term, status)
    
    response = err_info.value.response

    assert response.status_code == 400
    assert response.json()["errors"]["name"][0] == "The name field is required."

    print ("Unable to search for food trucks with missing name")


# Search for food trucks by partial street name - follow same logic with searching by partial food truck name
def test_search_food_trucks_by_partial_street_name():
    print("When searching for a food truck with a partial street name")
    term = global_street_term

    response = search_food_trucks_by_street(term)

    assert isinstance(response, list)
    assert len(response) > 0

    missing_search_term = []
    for truck in response:
        address = truck.get("address", "")
        if term.lower() not in address.lower():
            missing_search_term.append(address)
    
    if missing_search_term:
        raise AssertionError(
            f"The following food truck(s) should not be in the list: {missing_search_term}"
        )
    
    print("All results include the street search term")

# Search by street with no input - validate the same as missing food truck name
def test_search_by_empty_street():
    print("when searching for food trucks with no street name")
    term = ""

    with pytest.raises(requests.exceptions.HTTPError) as err_info:
        search_food_trucks_by_street(term)
    
    response = err_info.value.response

    assert response.status_code == 400
    assert response.json()["errors"]["street"][0] == "The street field is required."

    print ("Unable to search for food trucks with missing street")


# validate search can handle whitespace - This is bugged.
# Searching with leading/trailing whitespace returns zero results 
# instead of matching trimmed input.
def test_search_by_name_with_whitespace():
    print("When searching for food trucks with trailing whitespace in your query")
    term = "San Pancho"
    whitespace_term = "    San Pancho   "

    response = search_food_trucks_by_name(term)
    whitespace_response = search_food_trucks_by_name(whitespace_term)

    ids = {truck["id"] for truck in response}
    whitespace_ids = {truck["id"] for truck in whitespace_response}

    assert ids == whitespace_ids

    print("Food trucks are returned successfully")

# search for non-existing food truck (in SF) by name to validate empty response
def test_search_invalid_food_truck_by_name():
    print("When searching by an invalid food truck name")
    term = "Black's Sliders"

    response = search_food_trucks_by_name(term)
    assert isinstance(response, list)
    assert len(response) == 0
    print("No results found")

# Search for non-existing street (in SF). Same validation as non-existing name
def test_search_by_invalid_street_name():
    print("When searching by an invalid street name")
    term = "Darnaway"

    response = search_food_trucks_by_street(term)
    assert isinstance(response, list)
    assert len(response) == 0
    print("No results found")
