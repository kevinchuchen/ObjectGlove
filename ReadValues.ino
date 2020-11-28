

int sensorPin = A0;    // select the input pin for the potentiometer
int sensorPin1 = A1; 
int sensorPin2= A2; 
int LED = 13;
int button = 7;      // select the pin for the LED
int sensorValue = 0;  // variable to store the value coming from the sensor
int sensorValue1 = 0;  // variable to store the value coming from the sensor
int sensorValue2 = 0;  // variable to store the value coming from the sensor
int buttonState = LOW;
int prevState = LOW;
unsigned long lastDebounceTime = 0;
unsigned long debounceDelay = 60;
int incomingByte = 0;
void setup() {
  Serial.begin(9600);
}

void loop() {
  buttonState = digitalRead(button);
  
  if ((millis() - lastDebounceTime) > debounceDelay){
    if(buttonState == HIGH && prevState == LOW){
      lastDebounceTime = millis();
      //Serial.println(lastDebounceTime);
        prevState = HIGH;
        Serial.println("1");
    }
    else if(buttonState == LOW){
      prevState = LOW;
      lastDebounceTime = millis();
    }
  }
  


  if(Serial.available()>0){
    incomingByte = Serial.read();
    Serial.println(incomingByte);

    while(Serial.available() == 0){
        if(incomingByte == 49){ //ASCII for 1
          sensorValue = analogRead(sensorPin);
          sensorValue1 = analogRead(sensorPin1);
          sensorValue2 = analogRead(sensorPin2);
          Serial.print("sensorValue= ");
          Serial.print(sensorValue);
          Serial.print(" ");
          Serial.print("sensorValue1= ");
          Serial.print(sensorValue1);
          Serial.print(" ");
          Serial.print("sensorValue2= ");
          Serial.println(sensorValue2);  
        }
        else if(incomingByte == 83){ //ASCII for 'S'
          incomingByte = 0;
          break;
        }
      }
  }



}
