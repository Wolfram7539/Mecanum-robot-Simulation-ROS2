#ifndef JOY_CMD_VEL_NODE_HPP_
#define JOY_CMD_VEL_NODE_HPP_
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/joy.hpp"
#include "geometry_msgs/msg/twist.hpp"

class JoyToTwistNode : public rclcpp::Node
{
public:
  JoyToTwistNode()
  : Node("joy_to_twist_node")
  {
    // Publisher for geometry_msgs::msg::Twist
    twist_publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("cmd_vel", 10);
    joy_subscription_ = this->create_subscription<sensor_msgs::msg::Joy>(
      "joy", 10, std::bind(&JoyToTwistNode::joyCallback, this, std::placeholders::_1));
  }

private:
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr twist_publisher_;
  rclcpp::Subscription<sensor_msgs::msg::Joy>::SharedPtr joy_subscription_;
  void joyCallback(const sensor_msgs::msg::Joy::SharedPtr msg);
};

#endif