import geocoder
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time
import astropy.units as u
from astroquery.simbad import Simbad
import json

def get_location_from_ip():
    # Get the IP address of the current machine
    ip_address = geocoder.ip('me').ip
    
    # Use the IP address to get location information (latitude, longitude)
    location = geocoder.ip(ip_address)
    
    # Extract latitude and longitude
    latitude = location.latlng[0]
    longitude = location.latlng[1]
    your_elevation = location.meters
    
    return latitude, longitude, your_elevation

# Function to calculate motor adjustments
def calculate_motor_angles(current_alt, current_az, target_alt, target_az):
    # Calculate motor adjustments (assuming a simple proportional control)
    alt_adjustment = target_alt - current_alt
    az_adjustment = target_az - current_az
    
    return alt_adjustment, az_adjustment

# Get location information
your_latitude, your_longitude, your_elevation = get_location_from_ip()

# Camera orientation (current pointing direction) - Example values
current_alt = 45.0  # Example altitude in degrees
current_az = 180.0  # Example azimuth in degrees

# Initialize SIMBAD query tool
simbad = Simbad()

# Query for a specific astronomical object
object_name = "Sirius"  # Example object name
result_table = simbad.query_object(object_name)

# Extract coordinates if the query is successful
if result_table is not None:
    # Extract target object coordinates (RA and DEC)
    target_ra = result_table['RA'][0]
    target_dec = result_table['DEC'][0]
    
    # Convert target object coordinates to SkyCoord object
    target_coord = SkyCoord(ra=target_ra, dec=target_dec, unit=(u.hourangle, u.deg))

    # Location information
    location = EarthLocation(lat=your_latitude*u.deg, lon=your_longitude*u.deg, height=your_elevation*u.m)

    # Current time
    obs_time = Time.now()

    # Calculate altitude and azimuth of the target object
    target_altaz = target_coord.transform_to(AltAz(obstime=obs_time, location=location))
    target_alt = target_altaz.alt.deg
    target_az = target_altaz.az.deg

    # Calculate motor adjustments
    alt_adjustment, az_adjustment = calculate_motor_angles(current_alt, current_az, target_alt, target_az)

    # Print the obtained location information
    print("Your latitude:", your_latitude)
    print("Your longitude:", your_longitude)
    print("Your elevation:", your_elevation, "meters")

    # Print target coordinates
    print("Target object:", object_name)
    print("Target RA:", target_ra)
    print("Target DEC:", target_dec)

    # Print motor adjustments
    print("Altitude adjustment:", alt_adjustment)
    print("Azimuth adjustment:", az_adjustment)
else:
    print("Object not found in SIMBAD database.")
