#include <WiFi.h>
#include <HTTPClient.h>
#include <Arduino_JSON.h>

int decimalPrecision = 2;
 
//Phase Angle, Frequency and Power Factor measurement
 
int expectedFrequency = 50;
const int voltage_sensor_Pin = 34;
const int current_sensor_Pin = 35;
float voltageAnalogOffset =-952;
float currentAnalogOffset =-732;
unsigned long startMicrosPA;
unsigned long vCurrentMicrosPA;
unsigned long iCurrentMicrosPA;
unsigned long periodMicrosPA;
float vAnalogValue =0;
float iAnalogValue =0;
float previousValueV =0;
float previousValueI =0;
float previousphaseAngleSample=0;
float phaseAngleSample =0;
float phaseAngleAccumulate =0;
float periodSample=0;
float periodSampleAccumulate = 0;
float phaseDifference =0;
float phaseAngle =0;
float frequency = 0;
float voltagePhaseAngle=0;
float currentPhaseAngle=0;
float averagePeriod =0;
int sampleCount = 0;
int a = 3;
float powerFactor;
 
//Phase Angle Offset
 
float currentOffsetRead =0;
float currentOffsetLastSample =0;
float currentOffsetSampleCount=0;
float voltageOffsetRead =0;
float voltageOffsetLastSample =0;
float voltageOffsetSampleCount=0;

const char* serverName = "http://capstone-smart-meter.herokuapp.com/val";   //server name
const char* ssid = "OnePlus6";
const char* password = "aryan123";

WiFiClient client;
HTTPClient http;
 
char voltage[10],current[100],periodsa[50],phangle[50],httpRequestData[1024]; 
void setup()
{
Serial.begin(115200);
WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());

}
 
void loop()
{

//Phase Angle, Frequency and Power Factor measurement
 
vAnalogValue = analogRead(voltage_sensor_Pin)-2048 + voltageAnalogOffset; //12-bit ADC so 4096 values (-2048 to +2048)
iAnalogValue = (analogRead(current_sensor_Pin)-2048 + currentAnalogOffset);

 
if((vAnalogValue>0) && a == 3)
{
a=0;
}
 
if((vAnalogValue<=0) && a == 0)
{
startMicrosPA = micros();
a=1;
}
 
if((vAnalogValue>0) && a == 1)
{
a = 2;
previousValueV = 0;
previousValueI = 0;
}
 
if((vAnalogValue > previousValueV ) && a==2)
{
previousValueV = vAnalogValue ;
vCurrentMicrosPA = micros();
}
 
if((iAnalogValue > previousValueI) && a==2)
{
previousValueI = iAnalogValue ;
iCurrentMicrosPA = micros();
}
 
if((vAnalogValue <=0) && a==2)
{
periodMicrosPA = micros();
periodSample = periodMicrosPA - startMicrosPA;
periodSampleAccumulate = periodSampleAccumulate + periodSample;
voltagePhaseAngle = vCurrentMicrosPA - startMicrosPA;
currentPhaseAngle = iCurrentMicrosPA - startMicrosPA;
phaseAngleSample = currentPhaseAngle - voltagePhaseAngle;
if(phaseAngleSample>=100)
{
previousphaseAngleSample = phaseAngleSample;
}
if(phaseAngleSample<100)
{
phaseAngleSample = previousphaseAngleSample;
}
phaseAngleAccumulate = phaseAngleAccumulate + phaseAngleSample;
sampleCount = sampleCount + 1;
startMicrosPA = periodMicrosPA;
a=1;
previousValueV = 0;
previousValueI = 0;
}

dtostrf((vAnalogValue/4096)*1200,7,2,voltage);
dtostrf((iAnalogValue/4096)*500,5,2,current);
dtostrf(periodSampleAccumulate,5,2,periodsa);
dtostrf(phaseAngleAccumulate,5,2,periodsa);

http.begin(client, serverName);
http.addHeader("Content-Type", "application/json");

sprintf(httpRequestData,"{\"VOLTAGE\":\"%s\",\"CURRENT\":\"%s\",\"PERIODSAMPLE\":\"%d\",\"SAMPLECOUNT\":\"%d\",\"PHASEANGLE\":\"%d\"}",voltage,current,periodsa,sampleCount,periodsa);

int httpResponseCode = http.POST(httpRequestData);

http.end(); 
 
if(sampleCount == expectedFrequency)
{
sampleCount = 0;
periodSampleAccumulate = 0;
phaseAngleAccumulate =0;
}
}
