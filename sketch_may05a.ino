



int PulseSensorPurplePin = 0;        // Pulse Sensor PURPLE WIRE connected to ANALOG PIN 0

int Threshold = 550;            // Determine which Signal to "count as a beat", and which to ingore.

const long interval = 1000;
unsigned long previousMicros = 0;
unsigned long currentMicros;


long values = 200;

unsigned int myValues[200];
long count=0;
// The SetUp Function:
void setup() {

    Serial.begin(2000000);
  
}

// The Main Loop Function
void loop() {
  uint16_t sendSize = 0;
 
  currentMicros = micros();

  if((currentMicros - previousMicros) >= interval && count<values){
    previousMicros+= interval;
    myValues[count++] = analogRead(PulseSensorPurplePin);
  }else if(count == values){
   //Serial.println(currentMicros);
    //Serial.print("Count  ");
    //Serial.println(count);
    count++;
  }
  if(myValues[199]>0)
  {
  for(int k=0;k<200;k++)
  Serial.println(myValues[k]);

for(int k=0;k<200;k++)
  myValues[k]=0;
count=0;
previousMicros = 0;
  }
}
