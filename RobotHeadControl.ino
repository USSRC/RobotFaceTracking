/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h>

int input = 0;

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  Serial.begin(115200);
  //Serial.setTimeout(10);
  char inByte = ' ';
}

void loop() {
while(Serial.available())
{
  char inByte = Serial.read();
  pos += inByte;
  myservo.write(pos);
  delay(100);
}

/*if(Serial.available() > 0)
{
  input = Serial.read();
  Serial.print("I got: ");
  Serial.println(input);
  if(input == 114)
  {
    for (pos = 0; pos <= 150; pos += 1)
    {
        myservo.write(pos);              // tell servo to go to position in variable 'pos'
        delay(15);                       // waits 15ms for the servo to reach the position
    }
  }else if(input == 108)
  {
    for (pos = 150; pos >= 0; pos -= 1) 
    {
        myservo.write(pos);              // tell servo to go to position in variable 'pos'
        delay(15);                       // waits 15ms for the servo to reach the position
    }
  }

}*/
}

