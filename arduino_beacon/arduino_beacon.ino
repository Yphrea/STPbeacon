#include <ArduinoBLE.h>

void setup()
{
  Serial.begin(9600); 
  while (!Serial); //wait for initialization of Serial output (so it prints something)
  if (BLE.begin()) {
    Serial.println("BLE device successfully initialized!");
    Serial.print("BLE device adress is: ");
    Serial.println(BLE.address()); //print MAC
  }  
  else{
    Serial.println("BLE device initialization failed!");
  }
  int N = 32;
  BLE.setAdvertisingInterval(N); //interval = 0.625 ms*N, min 20 ms (N=32)
  BLE.advertise();
}

void loop()
{
}
