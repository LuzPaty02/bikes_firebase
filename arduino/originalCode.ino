#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN 5    // Pin de reinicio del RC522
#define SS_PIN 4     // Pin de selección del RC522
MFRC522 mfrc522(SS_PIN, RST_PIN); ///Creamos el objeto para el RC522
const int ledPinVerde = D3;
const int ledPinRojo = D4;
const int fotoresistenciaPin = A0;
int lightPin = A0;
int lightVal;
const int pinLED = D0;
int dt = 100;
int minimo = 900;

#include <FirebaseESP8266.h> // Asegúrate de que has incluido la biblioteca de Firebase adecuada

#define WIFI_SSID "S23"
#define WIFI_PASSWORD "Keea3715"
#define API_KEY "AIzaSyCBM842ZTZp15sMTeEz0AzKCAY4Nzegkqc"
#define DATABASE_URL ""
#define USER_EMAIL ""
#define USER_PASSWORD "123456"

FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;


void setup() {
  Serial.begin(9600); // Iniciamos La comunicación serial
  SPI.begin();        // Iniciamos el Bus SPI
  mfrc522.PCD_Init(); // Iniciamos el MFRC522
  pinMode(ledPinVerde, OUTPUT);
  pinMode(ledPinRojo, OUTPUT);
  pinMode(lightPin, INPUT);
  pinMode(pinLED, OUTPUT);
  Serial.println("Control de acceso:");

  // Inicializar la conexión WiFi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Conectado a WiFi");

  // Configurar Firebase
  config.api_key = API_KEY;
  auth.user.email = USER_EMAIL;
  auth.user.password = USER_PASSWORD;
  config.database_url = DATABASE_URL;

  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);

  Serial.println("Conectado a Firebase");
}

byte ActualUID[4]; // Almacenará el código del Tag leído
byte Usuario1[4] = {0x73, 0x8A, 0x95, 0x79}; // Código del usuario 1
byte Usuario2[4] = {0xC1, 0x2F, 0xD6, 0x0E}; // Código del usuario 2
char UID_actual[12];

// el codigo para la utilizacion del sensor rfid-rc522 se baso en el siguiente tutorial: https://naylampmechatronics.com/blog/22_tutorial-modulo-lector-rfid-rc522.html 
void loop() {
  // Revisamos si hay nuevas tarjetas presentes
  if (mfrc522.PICC_IsNewCardPresent()) {
    // Seleccionamos una tarjeta
    if (mfrc522.PICC_ReadCardSerial()) {
      // Enviamos serialemente su UID
      Serial.print(F("Card UID:"));
      for (byte i = 0; i < mfrc522.uid.size; i++) {
        Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
        Serial.print(mfrc522.uid.uidByte[i], HEX);
        ActualUID[i] = mfrc522.uid.uidByte[i];
      }
      ImprimeHex();
      Serial.print("     ");
      // Comparamos los UID para determinar si es uno de nuestros usuarios
      if (compareArray(ActualUID, Usuario1)) {
        Serial.println("Acceso concedido...");
        digitalWrite(ledPinVerde, HIGH);
        digitalWrite(ledPinRojo, LOW);
        delay(2000);
        digitalWrite(ledPinVerde, LOW);
        // Enviamos el acceso concedido a Firebase
        //Firebase.setBool(fbdo, "/acceso", true);
        Firebase.setBool(fbdo, "/access_logs/user_1", true);


      } else if (compareArray(ActualUID, Usuario2)) {
        Serial.println("Acceso concedido...");
        digitalWrite(ledPinVerde, HIGH);
        digitalWrite(ledPinRojo, LOW);
        delay(2000);
        digitalWrite(ledPinVerde, LOW);
        // Enviamos el acceso concedido a Firebase
        //Firebase.setBool(fbdo, "/acceso", true);
        Firebase.setBool(fbdo, "/access_logs/user_2", true);

      } else {
        Serial.println("Acceso denegado...");
        digitalWrite(ledPinVerde, LOW);
        digitalWrite(ledPinRojo, HIGH);
        delay(2000);
        digitalWrite(ledPinRojo, LOW);
        // Enviamos el acceso denegado a Firebase
        //Firebase.setBool(fbdo, "/acceso", false);
        Firebase.setBool(fbdo, "/access_logs/user_unknown", false);
      }

      // Terminamos la lectura de la tarjeta actual
      mfrc522.PICC_HaltA();
    }
  }
  int Read_value = 0;
  Firebase.getInt(fbdo, "/led", &Read_value);
  if(Read_value == 0){
    digitalWrite(pinLED, LOW);
  } else {
    lightVal = analogRead(lightPin);
    Firebase.setString(fbdo, "/Nivel de Oscuridad", lightVal);
    delay(dt);
    if(lightVal > minimo){
      digitalWrite(pinLED, HIGH);
      Firebase.setString(fbdo, "/Luces", "Luces Encendidas");
    } else{
      digitalWrite(pinLED, LOW);
      Firebase.setString(fbdo, "/Luces", "Luces Apagadas");
      }
  }
  
  
}

// Función para comparar dos vectores
boolean compareArray(byte array1[], byte array2[]) {
  if (array1[0] != array2[0]) return (false);
  if (array1[1] != array2[1]) return (false);
  if (array1[2] != array2[2]) return (false);
  if (array1[3] != array2[3]) return (false);
  return (true);
}

void ImprimeHex(){ // pasar referencia a Byte?
   // Inicializar la cadena UID con una cadena vacía.
  strcpy(UID_actual, "");
  
  // Recorrer el arreglo de bytes y construir la cadena con el formato deseado.
  for (int i = 0; i < 4; i++) {
    char temp[3]; // Crear una cadena temporal para almacenar cada byte convertido a hexadecimal.
    sprintf(temp, "%02X", ActualUID[i]); // Convertir el byte a formato hexadecimal y almacenarlo en la cadena temporal.
    strcat(UID_actual, temp); // Concatenar la cadena temporal a la cadena UID.
    
    if (i < 3) {
      strcat(UID_actual, " "); // Agregar un espacio después de cada byte, excepto el último.
    }
  }
  FirebaseJson json;

  json.set("UID", UID_actual);

  json.set("Ts/.sv", "timestamp"); 

  Firebase.pushJSON(fbdo, "/entradas", json);
    
}