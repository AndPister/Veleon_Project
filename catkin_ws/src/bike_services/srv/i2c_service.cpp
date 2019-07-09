#include<ros/ros.h>
#include<Wire.h>
#include<bike_services/i2c_service.h>
#include<string>

string recive_data(bike_services::i2C_service:Request &req){
    BYTE ergebnis[7];
    count =0;
    while(Wire.available()){
        ergebnis[count]=Wire.read(eq.device_id);
        count++;
    }
    string out(reinterpret_cast< char const* >(ergebnis),7)
    return out
}

string send_data(bike_services::i2C_service:Request &req){
    Wire.beginTransmission(req.device_id);
    Wire.send(req.data);
    bool respons = Wire.endTransmission();
    return (string)respons
}

bool callback(bike_services::i2C_service:Request &req, bike_services::i2c_service::Response &rep){
    if(req.send)
        rep.data=send_data(req);
    )
    else{
        rep.data=recive_data(req);
    }
    
}

int main(){
    ros::init(argc,argv,"service_server");
    Wire.begin();
    ros::NodeHandle nh;
    ros::ServiceServer service_server=nh.advertiseService("i2c_service", callback)
}