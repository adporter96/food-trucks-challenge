import math
import pytest
import requests
from Requests.get import get_nearest_food_trucks, search_food_trucks_by_name, search_food_trucks_by_street

# Smoke tests below. These are health checks that validate 
# data formatting, data types and data logic works as expected

# Test food truck object has the right properties, and those
# properties are the correct data type
def test_food_truck_schema_and_types():
    print("When validating the food truck schema and data types")
    response = search_food_trucks_by_name("San")
    truck = response[0]

    schema = {
        "id": int,
        "applicant": str,
        "latitude": (float, str, int),
        "longitude": (float, str, int),
        "status": str
    }

    assert all(
        key in truck and isinstance(truck[key], expected_type)
        for key, expected_type in schema.items()    
    )
    print("All data types are valid in the schema")