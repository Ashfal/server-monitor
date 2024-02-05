//zoomkat 11-12-13 String capture and parsing  
//from serial port input (via serial monitor)
//and print result out serial port
//copy test strings and use ctrl/v to paste in
//serial monitor if desired
// * is used as the data string delimiter
// , is used to delimit individual data 

#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27,16,2);

String readString; //main captured String 
String cpu; //data String
String ram;
String temp;

int ind1; // , locations
int ind2;
int ind3;
 
void setup() {
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
}

void loop() {

  //expect a string like 90,low,15.6,125*
  //or 130,hi,7.2,389*

  if (Serial.available())  {
    char c = Serial.read();  //gets one byte from serial buffer
    if (c == '*') {
      //do stuff
      lcd.clear();
      Serial.println();
      Serial.print("captured String is : "); 
      Serial.println(readString); //prints string to serial port out
      
      ind1 = readString.indexOf(',');  //finds location of first ,
      cpu = readString.substring(0, ind1);   //captures first data String
      ind2 = readString.indexOf(',', ind1+1 );   //finds location of second ,
      ram = readString.substring(ind1+1, ind2);   //captures second data String
      ind3 = readString.indexOf(',', ind2+1 );
      temp = readString.substring(ind2+1, ind3);
      
      lcd.setCursor(0,0);
      lcd.print("CPU:");
      lcd.setCursor(4,0);
      lcd.print(cpu);
      lcd.setCursor(8,0);
      lcd.print("TEMP:");
      lcd.setCursor(13,0);
      lcd.print(temp);
      lcd.setCursor(0,1);
      lcd.print("MEM:");
      lcd.setCursor(4,1);
      lcd.print(ram);
      
      readString=""; //clears variable for new input
      cpu="";
      ram="";
      temp="";
    }  
    else {     
      readString += c; //makes the string readString
    }
  }
}
