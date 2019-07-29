/*
 * Project:       Veleon-Project
 * Maintainer:    Andreas Pister
 * Discription:   This Program covers the Motor-Electonic-Interface, encoding evaluation and Motorcontroller
 * Input:         Encoder
 * Output:        analog-voltage to regulate the Motorspeed             
 * Bus:           I2C-Bus
 *                Input starts with: 
 *                E = enable Motors 1=true else false
 *                D = driving mode is used 
 *                    first speed for left Motor starts with L
 *                    second speed for right Motor starts with R
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


//i2c_interface define
#define deviceNR 0x2a
#define low_border 50
#define high_border 200
#define v_max 3.33
#define pin_motor 5                       //PWM pin witch the motor is Connected
#define enable_pin 6                      //Pin witch set the Breakeinput of the Motorconntroller
#define revered_rotation_pin 7           //Pin witch set the rotationdirection of the motor

//Motorusage
int range = high_border-low_border;
float phi_dot = 0.0;
float param[2];
bool enable =false;



void setup() {
  
  //i2_c Interface
  Wire.begin(deviceNR);
  Wire.onReceive(receiveEvent);
  
  //Encoder 
  Serial.begin(9200);
}

void loop() {
  Serial.println(enable);
  Serial.println(phi_dot);
 if (!enable){
    analogWrite(pin_motor,get_value(phi_dot));
  }
  else{
    analogWrite(pin_motor,0);
  }
}

void receiveEvent(int value){
  char resived[value];
  int count=0;
  while(Wire.available()){  
    resived[count++]=Wire.read();
  }
  if(resived[0]=='F') 
    phi_dot=0.000;
  else if(resived[0]=='E') 
    enable!= enable;
  else 
    memcpy(&phi_dot, &resived, sizeof(phi_dot));
  
}

int get_value(float phi_dot){
  float value = (range/phi_dot)*v_max+low_border;
  if (0<value<255) value=0;
  return value;
}
