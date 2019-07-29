#include <PID_v1.h>

#define tt 0.10777    //in s
#define t1 0.23196    //in s
#define ks 33.065
#define Ta  0.05    //sampling-time in s
#define Kp  (t1/tt)*(255/ks)  //proportional
#define Ki  Kp/(15.4*tt)                 //
#define Kd  0.2*tt *Kp

//Define Variables we'll be connecting to
double Setpoint, Input, Output;

//Specify the links and initial tuning parameters
PID myPID(&Input, &Output, &Setpoint,Kp,Ki,Kd, DIRECT);


//encoder 
#define enc_green_pin 2                   //Encoderpin green wire
#define enc_white_pin 3                   //Encoderpin white wire
#define n_per_Puls 0.01745329251          //2pi/steps_per_round  //steps_per_round=360
#define rotation_switch false             //if false output Positiv rotaion while rotates right side, else left sides 
unsigned int alt=0;                       //old encoder counter
volatile unsigned int value=0;            //aktuell encoder count
volatile bool signe= true;                //set the sign to value

float ealt=0.0;
float esum=0.0;
float Ki_Ta = Ta*Ki;
float Kd_Ta = Kd/Ta;

void setup()
{
  Serial.begin(9600);
  pinMode(enc_green_pin, INPUT_PULLUP);
  pinMode(enc_white_pin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(enc_white_pin), countLeft, RISING ); 
}

void loop()
{
  /*Input = encoding();
  myPID.Compute();
  analogWrite(5,Output);
  Serial.println(Input);*/

  float w = 3;
  float x = encoding();
  float e = w-x;
  esum = esum + e;
  
  if(esum>255) esum = 255;
  //if(esum<-high_border) esum = -high_border;
  float y = Kp*e + Ki_Ta*esum + Kd_Ta*(e-ealt);
  ealt = e;  
  analogWrite(5,y);
  Serial.println(x);
  delay((int)Ta*1000);
}


double encoding(){
  double rmp = ((value-alt)/(Ta+0.003))*n_per_Puls*0.25;
  value=0; alt= 0;
  //if (signe) rmp*=-1;
  return rmp;
}

void countLeft(){
  //if (digitalRead(enc_green_pin)==rotation_switch) signe= true;
  //else signe= false;
  value++;
}
