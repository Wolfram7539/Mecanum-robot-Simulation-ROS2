##  4‑Wheel Mecanum Robot Simulation with Nav2 in Ignition Gazebo

###  Prerequisites
- **OS**: Ubuntu 22.04 LTS  
- **ROS 2**: humble  
- **Ignition Gazebo**: Fortress (v6+)  
- Install required ROS 2 packages:
  ```bash
  sudo apt install \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    ros-humble-ros-ign-gazebo \
    ros-humble-ros-ign-bridge
  ```
### Set Environment Variable
```bash
export IGN_GAZEBO_RESOURCE_PATH=$IGN_GAZEBO_RESOURCE_PATH:\
"/path/to/your/Mecanum-robot-Simulation-ROS2/4wd_mecanum_sim_ws/\
install/mecanum_description/share/mecanum_description/worlds/warehouse"
```
tip: add this to your `~/.bashrc` to make it permanent.

### Launch Simulation + Nav2 + RViz
`ros2 launch mecanum_robot_sim_launch simulation.launch.xml`

### Demo
[demo.webm](https://github.com/user-attachments/assets/18453a04-79be-41f3-a013-007423557abd)

