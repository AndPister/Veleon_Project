/*
 * Project:       Veleon-Project
 * Maintainer:    Andreas Pister
 * Discription:   This Program covers the Motor-Electonic-Interface, encoding evaluation and Motorcontroller
 * Input:         Encoder
 * Output:        analog-voltage to regulate the Motorspeed             
 * Bus:           I2C-Bus
 *                Input starts with: 
 *                E = enable Motors 1=true else false
 *                F = Quickstopp for Motor
 *                    
 *      Beware the Input sequence!!
 *      else the Motor will stop 
 * 
 * This code is the property of Andreas Pister 
 * and may not be copied or changed without explicit permission.
 */
#include <Wire.h>
#include <stdio.h>

//i2c_interface 
#define deviceNR 0x2a
int phi_dot = 0;
volatile bool enable = false;
byte resived[32]={};

//encoder 
#define enc_green_pin 2                   // Encoderpin green wire
#define enc_white_pin 3                   //Encoderpin white wire
#define n_per_Puls 0.01745329251          // 2pi/steps_per_round  //steps_per_round=360
#define rotation_switch false             //if false output Positiv rotaion while rotates right side, else left sides 
unsigned int alt=0;                       //old encoder counter
volatile unsigned int value=0;            //aktuell encoder count
volatile bool signe= true;                //set the sign to value

//Motorusage
#define high_border 250                  //higher border witch inicates the highes voltage when the Motor is aktiv
#define pin_motor 5                       //PWM pin witch the motor is Connected
#define enable_pin 6                      //Pin witch set the Breakeinput of the Motorconntroller
#define revered_rotation_pin 7            //Pin witch set the rotationdirection of the motor

//Velocitycontroller
#define tt 0.10777    //in s
#define t1 0.23196    //in s
#define Ta  0.05    //sampling-time in s
#define Kp  (t1/tt)*(245/ks)     //proportional
#define Ki  Kp/(14*tt)                   //
#define Kd  0.2*tt *Kp
#define ks 33.065

float Ki_Ta = Ta*Ki;
float Kd_Ta = Kd/Ta;
float e = 0.0;
float ealt =0.0;
float esum =0.0;
double phi_test=0.0;
float y_alt=0.0;
unsigned long t_start=millis();


void setup() {
  
  //i2_c Interface
  Wire.begin(deviceNR);
  Wire.onReceive(receiveEvent);
  Serial.begin(9600);
  //Encoder 
  pinMode(enc_green_pin, INPUT_PULLUP);
  pinMode(enc_white_pin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(enc_white_pin), countLeft, RISING ); 

  //Motor
  pinMode(enable_pin,OUTPUT);
  pinMode(revered_rotation_pin,OUTPUT);
}

void loop() {

 if(millis()-t_start>=Ta)
 {
   double w =-1* (double)phi_dot/100;
 double x = encoding();
 
 //for (int i=0;i<32;i++) Serial.println((unsigned byte)resived[i]);
 //Serial.println(resived);
 //Serial.println(phi_dot);
/* if (enable){
    analogWrite(pin_motor,get_value(phi_dot));
  }
  else{
    analogWrite(pin_motor,0);
  }*/
  double e = w-x;
  esum = esum + e;
  if(esum>high_border) esum = high_border;
  if(esum<-high_border) esum = -high_border;
  double y = Kp*e + Ki_Ta*esum + Kd_Ta*(e-ealt);
  
 if(y<0.0) {
    digitalWrite(revered_rotation_pin,LOW);
    y*=-1;
  }
  else digitalWrite(revered_rotation_pin,HIGH);
  
  Serial.println(w);
  analogWrite(pin_motor,y);
  ealt = e;
  y_alt=y;
  
 }

  /*int t_delay=Ta*1000-(int)(millis()-t_start);
  Serial.println(t_delay);
  if (t_delay>0){
    
    delay(t_delay);
  }*/

}

void receiveEvent(int value){
  
  int count=0;
  while(Wire.available()){  
    resived[count++]=Wire.read();
  }
  memcpy(&phi_dot, &resived[1], sizeof(double));
}

float encoding(){
  float rmp = (value/Ta)*n_per_Puls*0.25;
  value=0;
  if (signe) rmp*=-1;
  return rmp;
}

void countLeft(){
  if (digitalRead(enc_green_pin)==rotation_switch) signe= true;
  else signe= false;
  value++;
}
