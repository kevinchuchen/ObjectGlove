

int thumb = A0;    // select the input pin for the potentiometer
int index = A1; 
int middle = A2; 
int ring = A3;
int pinky = A4;
int LED = 13;
int button = 7;      // select the pin for the LED
int sensorValue = 0;  // variable to store the value coming from the sensor
int sensorValue1 = 0;  // variable to store the value coming from the sensor
int sensorValue2 = 0;  // variable to store the value coming from the sensor
int sensorValue3 = 0;  // variable to store the value coming from the sensor
int sensorValue4 = 0;  // variable to store the value coming from the sensor
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
      prevState = HIGH;
      Serial.println("1"); //send start sentinel to PC
    }
    else if(buttonState == LOW){
      prevState = LOW;
      lastDebounceTime = millis();
    }
  }
  


  if(Serial.available()>0){
    incomingByte = Serial.read();
    //Serial.println(incomingByte);

    while(Serial.available() == 0){
        if(incomingByte == 49){ //ASCII for 1
          
          sensorValue = analogRead(thumb);
          sensorValue1 = analogRead(index);
          sensorValue2 = analogRead(middle);
          sensorValue3 = analogRead(ring);
          sensorValue4 = analogRead(pinky);
          
          Serial.print("thumb= ");
          Serial.print(sensorValue);
          Serial.print(" ");
          Serial.print("index= ");
          Serial.print(sensorValue1);
          Serial.print(" ");
          Serial.print("middle= ");
          Serial.print(sensorValue2);  
          Serial.print(" ");
          Serial.print("ring= ");
          Serial.print(sensorValue3);  
          Serial.print(" ");
          Serial.print("index= ");
          Serial.println(sensorValue4);  
        }
        else if(incomingByte == 83){ //ASCII for 'S' : Stop sentinel
          incomingByte = 0;
          break;
        }
      }
  }



}
