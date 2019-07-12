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
#include <string.h>
#include <stdio.h>

#define deviceNR 0x2a
#define low_border 50
#define high_border 200
#define v_max 10.0
#define pin_motor_L 1
#define pin_motor_R 7

int range = high_border-low_border;
float phi_l = 0.0;
float phi_r = 0.0;
float param[2];
bool enable=false;
char resived[32];
bool new_msg=false;
void setup() {
  Wire.begin(deviceNR);
  Wire.onReceive(receiveEvent);
  Serial.begin(9200);
  pinMode(3,OUTPUT);
}

void loop() {
  digitalWrite(3,HIGH);
  if(new_msg){
    check_msg(resived);
    new_msg=false;
  }
  if (enable){
    analogWrite(pin_motor_L,get_value(phi_l));
    analogWrite(pin_motor_R,get_value(phi_r));
  }
  else{
    analogWrite(pin_motor_L,0);
    analogWrite(pin_motor_R,0);
  }
  digitalWrite(3,LOW);
}

void receiveEvent(int anzahl){
  memset(resived, 0, sizeof(resived));
  int count=0;
  digitalWrite(3,HIGH);
  while(Wire.available()){
    
    resived[count++]=Wire.read();
  }
  digitalWrite(3,LOW);
  new_msg=true;
  //check_msg(resived);
}
void check_msg(char receive[]){
  String msgs(receive);
  msgs.trim();
  if (msgs.startsWith("E")){
    enable= (bool)msgs[1];
  }
  else if(msgs.startsWith("D"))
  {
    int L = msgs.indexOf("L");
    int R = msgs.indexOf("R");
    if (L<0 or R<0 or R<L) {
      phi_l=0.0;
      phi_r=0.0;
      return ;
    }
    String temp= msgs.substring(L+1,R-1);
    phi_l=temp.toFloat();
    temp=msgs.substring(R+1);
    phi_r=temp.toFloat();         
  }
}

int get_value(float phi_dot){
  int value = (int)(range*v_max/phi_dot)+low_border;
  if (0<value<255) value=0;
  return value;
}
