import requests

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OSRM_URL = "https://router.project-osrm.org/route/v1/driving"

def geocode(address: str):
    params = {"q": address, "format": "json", "limit": 1}
    r = requests.get(NOMINATIM_URL, params=params, headers={"User-Agent": "hos-app/1.0"})
    r.raise_for_status()
    results = r.json()
    if not results:
        raise ValueError(f"Could not geocode address: {address}")
    lat, lon = results[0]["lat"], results[0]["lon"]
    return float(lat), float(lon)

def get_route(coords):
    """
    coords: [(lat, lon), (lat, lon), ...]
    Returns OSRM route with distance miles, duration hours, geometry
    """
    # format coords string
    coord_str = ";".join(f"{lon},{lat}" for lat, lon in coords)
    url = f"{OSRM_URL}/{coord_str}"
    params = {"overview": "full", "geometries": "geojson"}
    r = requests.get(url, params=params)
    r.raise_for_status()
    data = r.json()
    if "routes" not in data or not data["routes"]:
        raise ValueError("No route found")
    route = data["routes"][0]
    distance_miles = route["distance"] / 1609.34
    duration_hours = route["duration"] / 3600
    return {
        "distance_miles": round(distance_miles, 1),
        "duration_hours": round(duration_hours, 2),
        "geometry": route["geometry"]
    }
