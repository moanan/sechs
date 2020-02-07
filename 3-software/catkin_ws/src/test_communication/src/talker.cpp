#include <ros/ros.h>
#include <test_communication/Student.h>

int main(int argc, char** argv)
{
    ros::init(argc, argv, "talker"); 
    ros::NodeHandle nh;
    
    test_communication::Student msg;
    msg.Name = "Tom";
    msg.age = 1;

    ros::Publisher pub = nh.advertise<test_communication::Student>("student_info",5 ); // buffer size: 5
    ros::Rate loopRate(1.0); // 1.0s

    while (ros::ok()) {
        pub.publish(msg);
        msg.age += 1;
        loopRate.sleep();
    }

    // ros::spin();//用于触发topic、service的响应队列
    return 0;
}