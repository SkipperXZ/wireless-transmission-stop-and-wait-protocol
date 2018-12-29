#include <Wire.h>
#include <Math.h>
#include <Adafruit_MCP4725.h>
//#include <Adafruit_ADS1015.h>

#define defaultFreq 1700
#define f0 400
#define f1 800
#define f2 1200
#define f3 1600
int delay0,delay1,delay2,delay3;
int input[4];
const uint16_t S_DAC[4] = {2048,4095,2048,0};


Adafruit_MCP4725 dac; 
void setup() {
  Serial.begin(115200);
  dac.begin(0x64);
  delay0 = (1000000 / f0 - 1000000 / defaultFreq) / 4;
  delay1 = (1000000 / f1 - 1000000 / defaultFreq) / 4;
  delay2 = (1000000 / f2 - 1000000 / defaultFreq) / 4;
  delay3 = (1000000 / f3 - 1000000 / defaultFreq) / 4;
  Serial.flush();
}

void loop() {
  if(Serial.available() > 0){
    int in = Serial.read();
  for(int i=3; i>=0; i--){
    input[i] = in & 3 ;
    //Serial.println(input[i]);
    
    in >>= 2;
  }
  for(int k=3; k>=0; k--){
    if (input[k]==0){
      Serial.print("00");
      for(int n=0; n<f0/200; n++){
    for (int sl =0 ; sl<4;sl++){
        dac.setVoltage(S_DAC[sl] ,false);
        delayMicroseconds(delay0);
                     }
    } 
    }
    
    else if (input[k]==1){
          Serial.print("01");
      for(int n=0; n<f1/200; n++){
     for (int sl =0 ; sl<4;sl++){
        dac.setVoltage(S_DAC[sl] ,false);
        delayMicroseconds(delay1);
                     }
    } 
    }

    
    else if (input[k]==2){
        Serial.print("10");
      for(int n=0; n<f2/200; n++){
    for (int sl =0 ; sl<4;sl++){
        dac.setVoltage(S_DAC[sl] ,false);
        delayMicroseconds(delay2);
                     }
    } 
    }
    else if (input[k]==3){
          Serial.print("11"); 
      for(int n=0; n<f3/200; n++){
    for (int sl =0 ; sl<4;sl++){
        dac.setVoltage(S_DAC[sl] ,false);
        delayMicroseconds(delay3);
                     }
    } 
    }
  
  }
  Serial.println();
  dac.setVoltage(0,false);

  
  }
  delay(100);
}
