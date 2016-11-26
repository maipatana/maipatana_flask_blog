String incomemess;
int ledPin = 2;
void setup()                    
{
 Serial.begin(9600);    
  pinMode(ledPin, OUTPUT);
 digitalWrite(ledPin, LOW);     
}

void loop(){
  
 // when characters arrive over the serial port...
  if (Serial.available()) {    
    // wait a bit for the entire message to arrive
    delay(100);
    lightonoff();
  }
}
void lightonoff(){
  while (Serial.available() > 0 ) {
      // Get the message from Serial
      incomemess += Serial.readString();
    }
  
    if(incomemess=="on"){
      digitalWrite(ledPin, HIGH);
    }else if(incomemess=="off"){
     digitalWrite(ledPin, LOW);
    }else{
    }
   incomemess ="";//Reset
}
