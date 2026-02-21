import math

# Reference Point: Hinjewadi Junction (Approximate)
REF_LAT = 18.59
REF_LON = 73.74

def xy_to_latlon(x, y):
    """
    Converts SUMO cartesian (x,y) meters to Geo Coordinates (lat, lon).
    Required because the Frontend uses Deck.gl which needs Lat/Lon.
    """
    r_earth = 6378137  # Earth radius in meters
    
    # Coordinate projection (Equirectangular approximation)
    new_lat = REF_LAT + (y / r_earth) * (180 / math.pi)
    new_lon = REF_LON + (x / r_earth) * (180 / math.pi) / math.cos(REF_LAT * math.pi / 180)
    
    return [new_lon, new_lat]