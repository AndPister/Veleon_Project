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
 * 
 * This code is the property of Andreas Pister 
 * and may not be copied or changed without explicit permission.
 */
#include <Wire.h>
#include <stdio.h>


//i2c_interface 
#define deviceNR 0x2a
volatile float phi_dot = 0.0;
volatile bool enable = false;


//encoder 
#define enc_green_pin 2                   // Encoderpin green wire
#define enc_white_pin 3                   //Encoderpin white wire
#define n_per_Puls 0.01745329251          // 2pi/steps_per_round  //steps_per_round=360
#define rotation_switch false             //if false output Positiv rotaion while rotates right side, else left sides 
unsigned int alt=0;                       //old encoder counter
volatile unsigned int value=0;            //aktuell encoder count
volatile bool signe= true;                //set the sign to value



//Motorusage
#define low_border 50                     //lower border witch inicates the lowest voltage when the Motor is aktiv
#define high_border 200                   //higher border witch inicates the highes voltage when the Motor is aktiv
#define v_max 10.0                        //maximum Speed for reference
#define pin_motor 5                       //PWM pin witch the motor is Connected
#define enable_pin 6                      //Pin witch set the Breakeinput of the Motorconntroller
#define revered_rotation_pin 7            //Pin witch set the rotationdirection of the motor
int range = high_border-low_border;       //Constand Value witch indicates the space between the higher and the lower border


//Velocitycontroller
#define Ta  0.05     //sampling-time in s
#define Kp  0.0     //proportional
#define Ki  0.0                       //
#define Kd  0.0
float Ki_Ta = Ta*Ki
float Kd_Ta = Kd/Ta
float e = 0.0;
float ealt =0.0;
float esum =0.0;


void setup() {
  
  //i2_c Interface
  Wire.begin(deviceNR);
  Wire.onReceive(receiveEvent);
  
  //Encoder 
  pinMode(enc_green_pin, INPUT_PULLUP);
  pinMode(enc_white_pin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(enc_white_pin), countLeft, RISING ); 

  //Motor
  pinMode(enable_pin,OUTPUT);
  pinMode(revered_rotation_pin,OUTPUT);
}

void loop() {

 float rmp = encoding(); 
 float w = phi_dot;
 float x = encoding();
 if (enable){
    analogWrite(pin_motor,get_value(phi_dot));
  }
  else{
    analogWrite(pin_motor,0);
  }
  int e = x-w;
  esum = esum + e;
  if(esum>high_border) esum = high_border;
  if(esum<-high_border) esum = -high_border;
  float y = Kp*e + Ki_Ta*esum + Kd_Ta*(e – ealt);
  ealt = e;
  
  if(y<0.0) {
    digitalWrite(revered_rotation_pin,HIGH);
    y*=-1;
  }
  else digitalWrite(revered_rotation_pin,LOW);
  
  analogWrite(pin_motor,(y+low_border));
  delay(Ta);
}

void receiveEvent(int value){
  char resived[value];
  int count=0;
  while(Wire.available()){  
    resived[count++]=Wire.read();
  }
  if(resived[0]=='F') phi_dot=0.000;
  else if(resived[0]=='E') enable!= enable;
  //else memcpy(&phi_dot, resived, sizeof(phi_dot));
}

int get_value(float phi_dot){
  int value = (int)(range*v_max/phi_dot)+low_border;
  if (0<value<255) value=0;
  return value;
}

float encoding(){
  float rmp = ((value-alt)/Ta)*n_per_Puls;
  value=0; alt= 0;
  if (signe) rmp*=-1;
  return rmp;
}

void countLeft(){
  if (digitalRead(enc_green_pin)==rotation_switch) signe= true;
  else signe= false;
  value++;
}
