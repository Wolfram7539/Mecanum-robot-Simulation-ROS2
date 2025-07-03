#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/pose_with_covariance_stamped.hpp>
#include <chrono>
#include <thread>

int main(int argc, char** argv) {
  rclcpp::init(argc, argv);
  auto node = rclcpp::Node::make_shared("initial_pose_setter");
  auto pub = node->create_publisher<geometry_msgs::msg::PoseWithCovarianceStamped>(
    "/initialpose", 10);
	
  while (rclcpp::ok() && pub->get_subscription_count() < 1) {
    RCLCPP_INFO(node->get_logger(), "Waiting for subscriber to /initialpose...");
    std::this_thread::sleep_for(std::chrono::milliseconds(500));
  }
  geometry_msgs::msg::PoseWithCovarianceStamped msg;
  msg.header.stamp = node->now();
  msg.header.frame_id = "map";
  msg.pose.pose.position.x = 0.0;
  msg.pose.pose.position.y = 0.0;
  msg.pose.pose.orientation.z = 0.0;
  msg.pose.pose.orientation.w = 1.0;
  // Covariance は適当な 36 要素を設定
  msg.pose.covariance = {0.25, 0, 0, 0, 0, 0,
                         0, 0.25, 0, 0, 0, 0,
                         0, 0, 0.25, 0, 0, 0,
                         0, 0, 0, 0.25, 0, 0,
                         0, 0, 0, 0, 0.25, 0,
                         0, 0, 0, 0, 0, 0.25};
                         
  std::this_thread::sleep_for(std::chrono::milliseconds(15000));
  pub->publish(msg);
  RCLCPP_INFO(node->get_logger(), "Published initial pose");
  rclcpp::shutdown();
  return 0;
}
