
/*
 * Project:       Veleon-Project
 * Maintainer:    Andreas Pister
 * Discription:   This Program covers the testscript for using the encoder and debuggung.          
 * Beware:        Do not set the Rate to highe.Couse the integer maby become a overflow while higher rotationspeed.
 *                This error is not catched!!
 *                
 *                
 * This code is the property of Andreas Pister 
 * and may not be copied or changed without explicit permission.
 */
#define enc_green_pin 2 // Encoderpin green wire
#define enc_white_pin 3 //Encoderpin white wire
#define rate 0.05 // detectionrate in s
#define n_per_Puls 0.01745329251 // 2pi/steps_per_round  //steps_per_round=360
#define rotation_switch false //if false output Positiv rotaion while rotates right side, else left sides 
#define transmission 0.25

unsigned int alt=0;   //old encoder counter
volatile unsigned int value=0;  //aktuell encoder count
volatile bool signe= true;  //set the sign to value
int spinningrate =(int) rate*1000; //set rate in ms 
int count=0;
void setup() {
  Serial.begin(9600);
  pinMode(enc_green_pin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(enc_white_pin), countLeft, RISING );  
}

void loop() {
  float rmp = encoding();
  Serial.println(rmp);
  delay(spinningrate);
}

float encoding(){
  float rmp = ((value-alt)/rate)*n_per_Puls;
  value=0; alt= 0;
  if (signe) rmp*=-1;
  return (rmp*transmission);
}
void countLeft(){
  if (digitalRead(enc_green_pin)==rotation_switch) signe= true;
  else signe= false;
  value++;
}
