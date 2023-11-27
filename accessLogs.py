from firebase_admin import db
from datetime import datetime

# Retrieve bike location based on bike ID
def get_bike_location(bike_id):
    bike_ref = db.reference('bikes').child(bike_id)
    bike_info = bike_ref.get()
    if bike_info:
        return bike_info.get('latitude'), bike_info.get('longitude')
    else:
        return None, None

# Create access log
def log_access(user_id, rfid_card_id, bike_id, access_type, return_latitude=None, return_longitude=None, unlock_id=None):
    
    pickup_latitude, pickup_longitude = get_bike_location(bike_id)  # Retrieve latitude and longitude from the bike table

    # Create access log dictionary
    access_log = {
        'user_id': user_id,  # User ID
        'rfid_card_id': rfid_card_id,  # RFID card ID
        'access_type': access_type,  # Access type
        'bike_id': bike_id,  # Bike ID

        # ------pick up data
        'pickup_access_time': {'timestamp': datetime.utcnow().isoformat()},  # Pickup access time
        'pickup_latitude': pickup_latitude,  # Pickup latitude
        'pickup_longitude': pickup_longitude,  # Pickup longitude

        # -----return data
        'return_access_time': None if access_type == 'pickup' else {'timestamp': datetime.utcnow().isoformat()},  # Return access time (asynchronous)
        'return_latitude': None if access_type == 'pickup' else return_latitude,  # Return latitude (asynchronous)
        'return_longitude': None if access_type == 'pickup' else return_longitude,  # Return longitude (asynchronous)

        
        # -----unlock data
        'unlock_id': None if access_type == 'pickup' else find_access_log_id_by_rfid(rfid_card_id, unlock_id)  # Unlock ID

    }

    # --Push access log to the 'accessLogs' table in the database
    access_logs_ref = db.reference('accessLogs')
    new_log_ref = access_logs_ref.push(access_log)
    access_log_id = new_log_ref.key

    # --Print success message with access log ID
    print(f'Access logged successfully with ID: {access_log_id}')
    return access_log_id


# ------- Log return asynchronously------
def log_return_async(user_id, rfid_card_id, bike_id_return, access_type, unlock_id):
    return_latitude, return_longitude = get_bike_location(bike_id_return)  # Retrieve latitude and longitude from the bike table
    return log_access(user_id, rfid_card_id, bike_id_return, access_type='return', return_latitude=return_latitude, return_longitude=return_longitude, unlock_id=unlock_id)


# -----Handle return event based on RFID card ID and return location----
def handle_return_event(rfid_card_id_return, return_latitude, return_longitude, unlock_id):
    access_log_id = find_access_log_id_by_rfid(rfid_card_id_return, unlock_id)  # Find the corresponding access log ID based on the RFID or some other identifier

    if access_log_id:
        update_return_data(access_log_id, return_latitude, return_longitude)  # Update return data in the access log
        print('return data updated!')
    else:
        print(f'Access log not found for RFID: {rfid_card_id_return}')


# ---------- AUXILIARY FUNCTIONS FOR RETURN -------

# Update return data in the access log
def update_return_data(access_log_id, return_latitude, return_longitude):
    access_logs_ref = db.reference('accessLogs')
    access_logs_ref.child(access_log_id).update({
        'return_access_time': {'timestamp': datetime.utcnow().isoformat()},
        'return_latitude': return_latitude,
        'return_longitude': return_longitude
    })

# Find if
def find_access_log_id_by_rfid(rfid_card_id_return, unlock_id):
    access_logs_ref = db.reference('accessLogs')
    access_logs = access_logs_ref.get()

    if access_logs:
        for log_id, log_data in access_logs.items():
            if log_data.get('rfid_card_id') == rfid_card_id_return and log_data.get('unlock_id') == unlock_id:
                return log_id

    return None


