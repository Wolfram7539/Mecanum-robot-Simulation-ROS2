#include <joy_cmd_vel_node/joy_cmd_vel_node.hpp>

void JoyToTwistNode::joyCallback(const sensor_msgs::msg::Joy::SharedPtr msg)
{
  geometry_msgs::msg::Twist twist_msg;

  // Assuming axes[0] is linear x, axes[1] is linear y, and axes[2] is angular z
  twist_msg.linear.x = msg->axes[1]*3;
  twist_msg.linear.y = msg->axes[0]*3;
  twist_msg.angular.z = msg->axes[2]*2;

  // Publish the Twist message
  twist_publisher_->publish(twist_msg);
}

int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  
  // Create the node
  auto node = std::make_shared<JoyToTwistNode>();

  // Spin the node to process callbacks
  rclcpp::spin(node);

  // Shutdown ROS
  rclcpp::shutdown();
  return 0;
}
