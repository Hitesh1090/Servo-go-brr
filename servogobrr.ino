#include <Servo.h>
Servo myservo;
int pos = 0;

void setup() {
    Serial.begin(9600);
    myservo.attach(A5); 
}

void loop() {
    if (Serial.available() > 0) {
        char command = Serial.read();
        
        if (command == 'S') {
            int angle = Serial.parseInt(); 
            myservo.write(angle);
        }
    }
}
