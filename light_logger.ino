// Light logger: sends one light reading per line over USB serial.
// Wiring: photoresistor + 10k voltage divider on A0, LED + 220 ohm on pin 9.

const int SENSOR_PIN = A0;
const int LED_PIN = 9;
const int THRESHOLD = 600;   // below this counts as "dark"; match logger.py

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int light = analogRead(SENSOR_PIN);   // 0 to 1023
  Serial.println(light);                // one number per line, nothing else

  // Hardware alert: LED on when it's dark
  digitalWrite(LED_PIN, light < THRESHOLD ? HIGH : LOW);

  delay(100);                           // about 10 readings per second
}
