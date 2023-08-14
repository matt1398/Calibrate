const int AXIS_X = A0;
const int AXIS_Y = A1;
const int SW_P = 6; 
 
void setup() {
  Serial.begin(9600);
  pinMode(SW_P,INPUT_PULLUP);
}
 
void loop() {

  Serial.print(analogRead(AXIS_X));
  Serial.print(" ");
  Serial.print(analogRead(AXIS_Y));
  Serial.print(" ");
  Serial.println(digitalRead(SW_P));
  delay(500);
}