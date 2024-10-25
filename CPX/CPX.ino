// https://github.com/adafruit/Adafruit_CircuitPlayground

#include <Adafruit_CircuitPlayground.h>

void setup() {
  CircuitPlayground.begin();
  // Set the buzzer on Circuit Playground to off initially
  CircuitPlayground.playTone(0, 1); // Stop any sound
  Serial.begin(115200);
}

void loop() {
  float x = CircuitPlayground.motionX();
  float y = CircuitPlayground.motionY();
  float z = CircuitPlayground.motionZ();

  // Calculate movement field
  float movement = sqrt(x ** 2 + y ** 2 + z ** 2);
  Serial.println(movement);
  

  // Check if movement exceeds a threshold
  if (movement > 14) { 
    // Play a tone if movement is detected
    CircuitPlayground.playTone(262, 500); // Play a middle C note for 500ms
    delay(1000); // Delay to avoid multiple sounds at once
  }

  delay(100); 
}

