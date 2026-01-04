import math
import random

from Requests.get import get_nearest_food_trucks

#This one I used copilot to help build out the necessary methods to get random coordinates withint San Franciso so I could test wether or not the "nearest" 
# trucks are actually within a reasonable distance of each other. I noticed the API returns a list of food trucks anywhere between 1 and 7 miles from each other.
# For the sake of the test, I wanted to validate the food trucks are at most within 5 miles of each other, because any more than that I feel is not "nearby".

# After generating up the haversine_miles method and assert_all_within_radius, I created tests for checking food trucks within 5 miles of the random origin coordinates
# and a negative test for checking for food trucks outside of that 5 mile radius, ensuring nothing is closer than a 5 mile minimum.


def haversine_miles(lat1, lon1, lat2, lon2) -> float:
    R_MI = 3958.7613
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (math.sin(dphi / 2) ** 2) + math.cos(phi1) * math.cos(phi2) * (math.sin(dlambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R_MI * c


def random_point_in_bbox(lat_min, lat_max, lon_min, lon_max, seed=None):
    rng = random.Random(seed)
    return rng.uniform(lat_min, lat_max), rng.uniform(lon_min, lon_max)


SF_BBOX = {"lat_min": 37.70, "lat_max": 37.83, "lon_min": -122.52, "lon_max": -122.35}
NYC_BBOX = {"lat_min": 40.60, "lat_max": 40.90, "lon_min": -74.10, "lon_max": -73.70}


def assert_all_within_radius(results, origin_lat, origin_lon, radius_miles):
    out_of_radius = []
    for truck in results:
        lat = float(truck["latitude"])
        lon = float(truck["longitude"])
        dist = haversine_miles(origin_lat, origin_lon, lat, lon)
        if dist > radius_miles:
            out_of_radius.append(
                {
                    "id": truck.get("id"),
                    "applicant": truck.get("applicant"),
                    "distance_miles": round(dist, 3),
                    "truck_lat": lat,
                    "truck_lon": lon,
                }
            )

    assert not out_of_radius, (
        f"Some results were outside {radius_miles} miles.\n"
        f"Origin: ({origin_lat}, {origin_lon})\n"
        f"Outliers: {out_of_radius}"
    )


def test_nearest_food_trucks_within_5_miles():
    origin_lat, origin_lon = random_point_in_bbox(**SF_BBOX, seed=1337)
    results = get_nearest_food_trucks(latitude=origin_lat, longitude=origin_lon)

    assert isinstance(results, list)
    assert len(results) > 0

    assert_all_within_radius(results, origin_lat, origin_lon, radius_miles=5.0)


def test_nearest_food_trucks_not_within_5_miles():
    
    # Negative test: If origin is far away (NYC), results should NOT be within a 5-mile radius
    # of that origin (because the API still returns SF trucks).
    
    origin_lat, origin_lon = random_point_in_bbox(**NYC_BBOX, seed=2024)
    results = get_nearest_food_trucks(latitude=origin_lat, longitude=origin_lon)

    assert isinstance(results, list)
    assert len(results) > 0 
    distances = [
        haversine_miles(origin_lat, origin_lon, float(t["latitude"]), float(t["longitude"]))
        for t in results
    ]
    assert any(d > 5.0 for d in distances), (
        "Expected at least one result to be farther than 5 miles from a far-away origin, "
        f"but got distances: {[round(d, 3) for d in distances]}"
    )
