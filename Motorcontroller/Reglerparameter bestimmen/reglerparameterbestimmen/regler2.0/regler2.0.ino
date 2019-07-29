
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
#define runn 5

unsigned int alt = 0; //old encoder counter
volatile unsigned long value = 0; //aktuell encoder count
volatile bool signe = true; //set the sign to value
int spinningrate = (int) rate * 1000; //set rate in ms
int count = 0;

void setup() {
  Serial.begin(9600);
  pinMode(enc_green_pin, INPUT_PULLUP);
  pinMode(enc_white_pin, INPUT_PULLUP);
  pinMode(4,OUTPUT);
  attachInterrupt(digitalPinToInterrupt(enc_white_pin), countLeft, RISING );

  digitalWrite(4,LOW);
  
}

void loop() {
  Serial.print("Messung startet\nAnzahl der Durchläufe: ");Serial.println(runn);
  double ts_array[runn];
  double tt_array[runn];
  double t1_array[runn];
  double ks_array[runn];
  for(int i =0; i<runn; i++){
    Serial.print("Messung: "); Serial.println(i+1);
    analogWrite(5, 0);
    delay(5000);
    bool jumpout_1 = false;
    double t0;
    double tt = -1.0;
    double t_i = 0.0;
    double rmp_i = 0.0;
    double ts = 0.0;
    double t1 = 0.0;
    double m =0.0;
    double b=0.0;
    double rmp_n;
    double t_n ;
    value=0.0;
    t0=micros();
    long mills =0;
    long mics =0;
    
    analogWrite(5,255);
    while(true){
       mills=millis();
       if (value > 0 and tt <= 0.0) {
          tt = (double)(micros()-t0)/1000000.0;
          //analogWrite(5, 255);
          
        }else{
          if (tt>0.0 and mills >= (2000+((tt+t0)/1000)) and !jumpout_1) {
            jumpout_1 = true;
            rmp_i = value*n_per_Puls*transmission;
            t_i = (micros()-t0)/1000000;
          }
          if (tt>0.0 and mills >=2500+((long)(tt+t0)/1000)) {
            rmp_n = value*n_per_Puls*transmission;
            t_n = (double)(micros()-t0);
            t_n=t_n/1000000.0;
            m = (double)(rmp_n - rmp_i)/(double)(t_n - t_i);
            b = (double)rmp_i - m * t_i;
            ts = -b / m;
            t1=ts-tt;
            break;
          }
        }
    }
    analogWrite(5, 0);
    ts_array[i]=ts;
    tt_array[i]=tt;
    t1_array[i]=t1;
    ks_array[i]=m;


    
    Serial.print("Ts = ");Serial.println(ts,10);
    Serial.print("Tt = ");Serial.println(tt,10);
    Serial.print("T1 = ");Serial.println(t1,10);
    Serial.print("Ks = ");Serial.println(m,10);
    //delay(2000);
  }
  double TS = 0.0;
  double TT = 0.0;
  double T1 = 0.0;
  double KS = 0.0;
  for(int n=0; n<runn; n++){
     TS+=ts_array[n];
     TT+=tt_array[n];
     T1+=t1_array[n];
     KS+=ks_array[n];
    }
  TS=TS/(double)runn;
  TT=TT/(double)runn;
  T1=T1/(double)runn;
  KS=KS/(double)runn;
  Serial.println("Messung beendet\nMittelwert der Messungen:");
  Serial.print("Ts = ");Serial.println(TS,10);
  Serial.print("Tt = ");Serial.println(TT,10);
  Serial.print("T1 = ");Serial.println(T1,10);
  Serial.print("Ks = ");Serial.println(KS,10);
  while(true){
    delay(100);
    }
}
/**/
/*double encoding(){
  //double rmp = (value/rate)*n_per_Puls;
  //value=0; alt= 0;
  //if (signe) rmp*=-1;
  return (rmp*transmission);
  }*/
void countLeft() {
  //if (digitalRead(enc_green_pin) == rotation_switch) signe = true;
  //else signe = false;
  value++;
}
