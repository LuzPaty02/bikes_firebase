// Include necessary libraries here

// Define RFID card UIDs and other constants

void linkBikeToUser(const char* bikeId, const char* matricula) {
  // Function to link a bike with a user
  FirebaseData fbdo;
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  
  // Update the 'matricula' field in the 'bikes' node with the provided 'bikeId'
  String path = "/bikes/" + String(bikeId) + "/matricula";
  Firebase.setString(fbdo, path.c_str(), matricula);
  
  Serial.print("Bike ");
  Serial.print(bikeId);
  Serial.print(" linked to user with matricula ");
  Serial.println(matricula);
}

void loop() {
  // Existing RFID card reading and authorization code

  // Inside the section where access is granted
  if (compareArray(ActualUID, Usuario1)) {
    Serial.println("Acceso concedido...");

    // Link the bike with the user by updating Firebase
    linkBikeToUser("your_bike_id", "12345"); // Replace with actual bike ID and matricula

    // Continue with the rest of your code
    digitalWrite(ledPinVerde, HIGH);
    digitalWrite(ledPinRojo, LOW);
    delay(2000);
    digitalWrite(ledPinVerde, LOW);
    // Enviamos el acceso concedido a Firebase
    Firebase.setBool(fbdo, "/access_logs/user_1", true);
  } else if (compareArray(ActualUID, Usuario2)) {
    // Similar logic for the second user
  } else {
    // Similar logic for access denied
  }
}


// Inside the section where access is granted
if (compareArray(ActualUID, Usuario1)) {
    Serial.println("Acceso concedido...");

    // Log access with RFID card information
    logAccess("your_user_id", "rfid_123", "your_bike_id", "unlock", latitude, longitude);

    // Continue with the rest of your code
}
