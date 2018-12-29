
#ifndef cbi
#include <Adafruit_ADS1015.h>
#define cbi(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))
#endif
#ifndef sbi
#define sbi(sfr,bit) (_SFR_BYTE(sfr) |= _BV(bit))
#endif
#define r_slope 60

int max = 0;
int prev = 0;
int delay0 = (1000000 / 1600 - 1000000 / 1700) / 4 ;
int check = false;
int tmp1, tmp2, tmp;
unsigned long time1 = 0;
unsigned long time2 = 0;
int count = 0;
int f[4];
int rx_bit[4];
int i = 0;
int ch = 0;

void setup() {
  sbi (ADCSRA, ADPS2);
  cbi (ADCSRA, ADPS1);
  cbi (ADCSRA, ADPS0);
  Serial.begin(115200);
  //pinMode(A1,INPUT);
}

void loop() {

  tmp1 = analogRead(A0);
  tmp2 = analogRead(A1);
  tmp = abs( tmp1 - tmp2);

  //Serial.println(tmp);
  if (tmp > r_slope) {
    for (int k = 0; k < 4; k++) {

      for (int i = 0 ; i < 195; i++) {
        int tmp = analogRead(A0);
        if (tmp - prev > r_slope) {
          //Serial.println(tmp);
          max = 0;
          check = true;
        }
        if (tmp > max) {
          max = tmp;
        }
        if (max - tmp > r_slope) {
          if (check == true) {
            count++;
          }
          check = false;
        }
        prev = tmp;
        delayMicroseconds(delay0);
      }
      if (k == 3)
        count++;
      //Serial.println(count);
      if (count == 2)
      {

        //  Serial.print("0 0 ");
        ch >>= 2;
        ch |= 0;
      }
      else if (count == 4)
      {
        ch >>= 2;
        ch |= 64;
        //  Serial.print("0 1 ");
      }
      else if (count == 6)
      {
        ch >>= 2;
        ch |= 128;
        //   Serial.print("1 0 ");
      }
      else if (count == 8)
      {
        ch >>= 2;
        ch |= 192;
        // Serial.print("1 1 ");
      }
      else
      {

        //   Serial.print("X X ");
      }
      count = 0;

    }
    if (ch != 0)
      Serial.print(char(ch));
    //delay(100);
    ch = 0;
  }

}
