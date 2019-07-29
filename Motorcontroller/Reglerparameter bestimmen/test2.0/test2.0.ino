
/*
   Project:       Veleon-Project
   Maintainer:    Andreas Pister
   Discription:   This Program covers the testscript for using the encoder and debuggung.
   Beware:        Do not set the Rate to highe.Couse the integer maby become a overflow while higher rotationspeed.
                  This error is not catched!!


   This code is the property of Andreas Pister
   and may not be copied or changed without explicit permission.
*/

#define enc_green_pin 2 // Encoderpin green wire
#define enc_white_pin 3 //Encoderpin white wire
#define rate 0.01 // detectionrate in s
#define transmission 0.25
#define n_per_Puls 0.01745329251

unsigned int alt = 0; //old encoder counter
volatile unsigned long value = 0; //aktuell encoder count
volatile bool signe = true; //set the sign to value
int spinningrate = (int) rate * 1000; //set rate in ms
int count = 0;
double t0;
double tt = -1;
double t_i = 0;
double rmp_i = 0;
bool jumpout_1 = false;
bool jumpout_2 = false;
double ts = 0;
double t1 = 0;
double m =0.0;
double b=0.0;
double rmp_n;
double t_n ;

void setup() {
  Serial.begin(9600);
  pinMode(enc_green_pin, INPUT_PULLUP);
  pinMode(enc_white_pin, INPUT_PULLUP);
  pinMode(4,OUTPUT);
  attachInterrupt(digitalPinToInterrupt(enc_white_pin), countLeft, RISING );

  digitalWrite(4,LOW);
  
}

void loop() {
  //Serial.println(count);
  //double rmp = encoding();
  //Serial.println(millis());
  //Serial.println(value);}
  Serial.println("Cooldown");
  analogWrite(5, 255);
  delay(2000);
//  analogWrite(5, 90);
//  delay(5000);}

  Serial.println("Start messurment");
  value=0.0;
  t0=(micros()/1000000);
  long mills =0;
  long mics =0;
  analogWrite(5,180);
  while(true){
    double micro=(double)(micros()/1000000)-t0;
    double rmp = value*n_per_Puls;
     if (rmp > 0 and tt <= 0.0) {
        tt = micro;
        //analogWrite(5, 255);  
      }
      else{
        if (tt>0.0 and micro >= 2.0+tt and !jumpout_1) {
        jumpout_1 = true;
        rmp_i = rmp;
        t_i = (micros()-t0)/1000000;
      }
      if (tt>0.0 and micro >=3.0+tt) {
        rmp_n = rmp;
        t_n = micro;

        m = (rmp_n - rmp_i)/(t_n - t_i);
        b = rmp_i - m * t_i;
        ts = b / m;
        t1=ts-tt;
        break;
     }
      }
     
    //delay(10);
  }
  analogWrite(5, 255);
  Serial.println("Stopp messurment");
  Serial.println(t0/1000000,10);
  Serial.println(t_n,10);
  Serial.println(t_i,10);
  Serial.println(rmp_n,10);
  Serial.println(rmp_i,10);
  Serial.println(m,10);
  Serial.println(b);
  Serial.print("Ts = ");Serial.println(ts,10);
  Serial.print("Tt = ");Serial.println(tt,10);
  Serial.print("T1 = ");Serial.println(t1,10);
  delay(5000);
  while(true){
    delay(100);
    }
}
/**/
/*double encoding(){
  //double rmp = (value/rate)*n_per_Puls;
  //value=0; alt= 0;
  //if (signe) rmp*=-1;
  return (value*n_per_Puls);
  }*/
void countLeft() {
  //if (digitalRead(enc_green_pin) == rotation_switch) signe = true;
  //else signe = false;
  value++;
}
