import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Function to add a new user
def add_user(username, matricula, rfid_card):
    new_user = {
        'username': username,
        'matricula': matricula,
        'rfid_card': rfid_card
    }

    users_ref = db.reference('users')
    new_user_ref = users_ref.push(new_user)
    user_id = new_user_ref.key  # Get the automatically generated ID

    print(f'User added successfully with ID {user_id}: {username}')
    return user_id  # Return the generated user ID

