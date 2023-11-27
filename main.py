import firebase_admin
from firebase_admin import credentials
#from firebase_admin import db
from users_db import add_user
from bikes_db import add_bike, update_bike
from gps_db import add_gps, link_bike_to_gps, update_gps, handle_gps_change	
from accessLogs import log_access, log_return_async
import time

def initialize_firebase():
    cred = credentials.Certificate(r"D:\uni - 3\IoT\bikes_firebase\credentials.json")
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://biketec-d84db-default-rtdb.firebaseio.com/'})


def main():
    print("Initializing Firebase...")
    initialize_firebase()        
    # Keep the script running

    # Instancias

        #print("Adding GPS...")

    #add_gps(gps_status, latitude, longitude)
        #new_gps_id=add_gps('true', 20.73312365828817, -103.45598686285568)
            #Ejemplo: add_gps('true', 20.6654223, -103.3582220)
        #new_gps_id= '-NjFuANNdkLPLM5mHgxv'
        #print(f"\nGenerated id: {new_gps_id}")

    # print("\n\nAdding bikes...")
    #add_bike(gps_id, is_available)

        #new_bike_id=add_bike(new_gps_id, 'true') 
            #Ejemplo: add_bike('-NjG-7Flr0hsEtulAPYj', 'true')
    new_bike_id='-NjmKZaAabRxjSGuArjj'
        #print ("Current Id's:\nBike: "+new_bike_id+"\nGPS: "+new_gps_id)


        #print("\n\nLinking bikes to GPS...")
    #link_bike_to_gps(bike_id, gps_id)
        
        #link_bike_to_gps(new_bike_id, new_gps_id)
            #Ejemplo: link_bike_to_gps('-NjFuAP2iAkYAAgto78l', '-NjFuANNdkLPLM5mHgxv')

        # print("Updating GPS...")
    #update_gps(gps_id, gps_status, latitude, longitude)


        #print("Updating bikes...")
    #update_bike(bike_id, gps_id, is_available)
        #update_bike(new_bike_id, new_gps_id, 'true')

        #print("Adding users...")
        #user_id= add_user(username, matricula, rfid_card)
        #new_user_id= add_user('Moi', 'A01234567', 'rfid_1')
        new_user_id= '-NjmbGGWoQFiw7mB3hEe'

        # Assume RFID card 'rfid_123' is used to access Bike 'bike_1' for unlocking
    #log_access(user_id, rfid_card_id, bike_id, access_type)
        #print("Logging access...")
        #log_access(new_user_id, 'rfid_123', new_bike_id, 'unlock')

    #Asynchronous return logging
    #log_return_async(user_id, rfid_card_id, bike_id_return, unlock_id)
        new_unlock_id= '-NjmbGKHJHeW3s9w451d'
        print("Logging return...")
        log_return_async(new_user_id, 'rfid_123', new_bike_id, 'return', new_unlock_id)

if __name__ == "__main__":
    main()
