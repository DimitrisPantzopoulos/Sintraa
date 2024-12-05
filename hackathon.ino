const int flexSensorPin = A1;  // Flex sensor pin
const int photoSensorPin = A0; // Photoresistor pin
const int greenLEDPin = 4;     // Green LED pin
const int yellowLEDPin = 3;    // Yellow LED pin

int previousPhotoValue = 0;      // To store the last photoresistor value
const int lightChangeThreshold = 50; // Define a threshold for light change
String currentState = "No Meal"; // To store the current state (Meal A or None)

void setup() {
  pinMode(greenLEDPin, OUTPUT); // Set green LED as output
  pinMode(yellowLEDPin, OUTPUT); // Set yellow LED as output
  Serial.begin(9600); // Start Serial communication
}

void loop() {
  int flexValue = analogRead(flexSensorPin); // Read flex sensor
  int photoValue = analogRead(photoSensorPin); // Read photoresistor

  // Calculate the change in light conditions
  int lightChange = abs(photoValue - previousPhotoValue);

  // Check if a large change in light is detected
  if (lightChange > lightChangeThreshold) {
    if (photoValue < previousPhotoValue) {
      currentState = "Burger"; // Large decrease in light
      digitalWrite(greenLEDPin, HIGH);  // Turn on green LED
      digitalWrite(yellowLEDPin, LOW);  // Turn off yellow LED
      Serial.println(flexValue);
    } else {
      currentState = "No Meal"; // Large increase or reset
      digitalWrite(greenLEDPin, LOW);   // Turn off green LED
      digitalWrite(yellowLEDPin, HIGH); // Turn on yellow LED
    }

    // Update the previous photo value after detecting a change
    previousPhotoValue = photoValue;

    // Print the new state
    Serial.println(currentState);
  }

  // Print sensor values for debugging
  //Serial.print("Flex Value: ");
  //Serial.println(flexValue);
  //Serial.print("Photo Value: ");
  //Serial.println(photoValue);

  delay(500); // Delay for readability
}
