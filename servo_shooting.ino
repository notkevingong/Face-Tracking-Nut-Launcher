#include <Servo.h>
#define PWM1 9
#define PWM2 3

Servo myservo1;
Servo myservo2;

int serialData;
int val;

void setup() {
  Serial.begin(9600);
  myservo1.attach(PWM1);
  myservo2.attach(PWM2);
}

void loop() {
  //reset the servo to the starting position
  myservo2.write(0); 

  //if serial recieves data
  if(Serial.available() > 0){

    //recievs data and prints to serial
    serialData = int(Serial.read());
    Serial.print(serialData);

    //map serial data coming from python (45-58) to 0-180 scale
    val = map(serialData, 45, 58, 0, 180); 
    
    //used to track value in python
    Serial.print("Mapped value: ");
    Serial.println(val);                 

    //send the position to the servo motor
    myservo1.write(val); 
    delay(1000);

    //shoot the nut
    myservo2.write(40); 
    delay(1000);
  
  }
}
