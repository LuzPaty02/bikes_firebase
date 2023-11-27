from firebase_admin import db
import time

gps_coordinates = {}

# Function to add new GPS data
def add_gps(gps_status=False, latitude=None, longitude=None):
    new_gps_data = {
        'gps_status': bool(gps_status),
        'latitude': latitude,
        'longitude': longitude
    }

    gps_ref = db.reference('gps')
    new_gps_ref = gps_ref.push(new_gps_data)
    gps_id = new_gps_ref.key

    # Update the coordinates dictionary
    gps_coordinates[gps_id] = (latitude, longitude)
    print(f"\nCurrent coordinates ->", gps_coordinates)

    print('GPS data added successfully')
    return gps_id

# Function to update existing GPS data
def update_gps(gps_id, gps_status, latitude, longitude):
    updated_gps_data = {
        'gps_status': bool(gps_status.lower() == 'true'),
        'latitude': latitude,
        'longitude': longitude
    }

    gps_ref = db.reference(f'gps/{gps_id}')
    gps_ref.update(updated_gps_data)

    print('GPS data updated successfully')

# Function to link a bike with a GPS ID
def link_bike_to_gps(bike_id, gps_id):
    bike_ref = db.reference(f'bikes/{bike_id}')
    bike_ref.update({
        'gps_id': gps_id,
        'latitude': gps_coordinates[gps_id][0],
        'longitude': gps_coordinates[gps_id][1]
    })

    print(f'Bike {bike_id} linked to GPS {gps_id} successfully')

# Function to get coordinates based on GPS ID
def get_coordinates_by_gps_id(gps_id):
    return gps_coordinates.get(gps_id, (0.0, 0.0))

# Function to handle changes in Firebase Realtime Database
def handle_gps_change(event):
    if event.data:
        gps_data = event.data
        gps_id = event.path.split('/')[-1]

        # Assuming Arduino sends 'latitude', 'longitude'
        latitude = gps_data.get('latitude', 0.0)
        longitude = gps_data.get('longitude', 0.0)

        update_gps(gps_id, True, latitude, longitude)

# Set up the listener
gps_ref = db.reference('gps')
gps_ref.listen(handle_gps_change)


# Keep the script running
while True:
    time.sleep(1)