from firebase_admin import credentials
from firebase_admin import db
from gps_db import get_coordinates_by_gps_id
# Function to get coordinates based on GPS ID (you need to implement this)


# Function to add a new bike
def add_bike(gps_id, is_available):
    latitude, longitude = get_coordinates_by_gps_id(gps_id)

    new_bike = {
        'gps_id': gps_id,
        'is_available': is_available == 'true',
        'latitude': latitude,
        'longitude': longitude
    }

    bikes_ref = db.reference('bikes')
    bikes_ref.push(new_bike)

    print('Bike added successfully')
  
    # Retrieve the automatically generated key for the new bike data
    bikes_ref = db.reference('bikes')
    new_gps_ref = bikes_ref.push(new_bike)
    bike_id = new_gps_ref.key

    return bike_id

# Function to update an existing bike
def update_bike(bike_id, gps_id, is_available):
    latitude, longitude = get_coordinates_by_gps_id(gps_id)

    updated_bike_data = {
        'gps_id': gps_id,
        'is_available': is_available == 'true',
        'latitude': latitude,
        'longitude': longitude
    }

    bike_ref = db.reference(f'bikes/{bike_id}')
    bike_ref.update(updated_bike_data)

    print('Bike updated successfully')

# Example usage:
#add_bike('5', 'true')
#update_bike('-NjAs5KE-O_6cU5BRuZP', '-NjB0ZImdM6wyRf6r5O5', 'true')
