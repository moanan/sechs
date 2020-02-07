#include <ros/ros.h>
#include <test_communication/Student.h>

void gpsCallback(const test_communication::Student::ConstPtr &msg)
{
    ROS_INFO("Student name: %s, age: %d", msg->Name.data(), msg->age); //输出
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "listener");
    ros::NodeHandle nh;
    ros::Subscriber sub = nh.subscribe("student_info", 5, gpsCallback);  //buffer size: 5
    ros::spin(); //ros::spin()用于调用所有可触发的回调函数，将进入循环，不会返回，类似于在循环里反复调用spinOnce()
    //而ros::spinOnce()只会去触发一次
    return 0;
}
