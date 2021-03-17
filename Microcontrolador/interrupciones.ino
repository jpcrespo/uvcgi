const int emuPin = 10;
 
const int LEDPin = 13;
const int intPin = 2;
volatile int state = LOW;
 
void setup() {
   pinMode(emuPin, OUTPUT);
   pinMode(LEDPin, OUTPUT);
   pinMode(intPin, INPUT_PULLUP);
   attachInterrupt(digitalPinToInterrupt(intPin), blink, CHANGE);
}
 
void loop() {
   //esta parte es para emular la salida
   digitalWrite(emuPin, HIGH);
   delay(150);
   digitalWrite(emuPin, LOW);
   delay(150);
}
 
void blink() {
   state = !state;
   digitalWrite(LEDPin, state);
}