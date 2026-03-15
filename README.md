# Autonomous Warehouse Delivery Robot: ROS 2 & Nav2 

An autonomous, simulated differential-drive delivery robot built with ROS 2 (Humble), Gazebo Classic, and the Nav2 stack. This project demonstrates a complete mechatronics system capable of infinite delivery loops between designated pickup and drop-off zones while dynamically avoiding obstacles.



## Key Features
* **Custom URDF/Xacro:** A custom-built robot chassis (`sam_bot`) with accurate physical links, joints, and inertias.
* **Sensor Fusion (EKF):** Integrates wheel odometry and an IMU (gyroscope) using the `robot_localization` package to eliminate rotational drift.
* **Tuned Localization (AMCL):** Deeply tuned Adaptive Monte Carlo Localization to handle dynamic obstacles (traffic cones) without triggering the "Kidnapped Robot" panic mode.
* **Automated Python Manager:** Uses the Nav2 Simple Commander API to execute continuous, autonomous delivery loops.

---

## Prerequisites & Installation

To run this simulation, you will need Ubuntu 22.04 with **ROS 2 Humble** installed. 

**1. Install Required ROS 2 Packages**
```bash
sudo apt update
sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup
sudo apt install ros-humble-robot-localization
sudo apt install ros-humble-gazebo-ros-pkgs


2. Clone the Repository
Create a workspace and clone this project:

Bash


mkdir -p ~/delivery_bot_ws/src
cd ~/delivery_bot_ws/src
git clone [https://github.com/keera21/autonomous-warehouse-robot.git](https://github.com/keera21/autonomous-warehouse-robot.git) navigation2_tutorials


3. Build the Workspace

Bash


cd ~/delivery_bot_ws
colcon build --symlink-install
source install/setup.bash


🚀 How to Run the Simulation
You will need to open four separate terminals to run the complete system. Be sure to source your workspace (source ~/delivery_bot_ws/install/setup.bash) in every new terminal!
Terminal 1: Launch the Physical World (Gazebo & RViz)
This spawns the warehouse environment and the robot.

Bash


ros2 launch sam_bot_description display.launch.py use_sim_time:=True


(Wait for Gazebo to fully load before moving to the next step).
Terminal 2: Start the Sensor Fusion Brain (EKF)
This silently runs the Extended Kalman Filter to mathematically fuse the wheel odometry and IMU data for drift-free turning.


Bash


ros2 run robot_localization ekf_node --ros-args --params-file ~/delivery_bot_ws/src/navigation2_tutorials/sam_bot_description/config/ekf.yaml


Terminal 3: Start the Navigation Brain (Nav2)
This launches the path planners, costmaps, and localization node (AMCL).

Bash


ros2 launch nav2_bringup bringup_launch.py \
use_sim_time:=True \
autostart:=True \
map:=/home/bashaar/delivery_bot_ws/src/navigation2_tutorials/sam_bot_description/map/warehouse_map.yaml \
params_file:=/home/bashaar/delivery_bot_ws/src/navigation2_tutorials/sam_bot_description/config/nav2_params.yaml


Crucial Step: Initial Localization
Before running the automation script, you must tell the robot where it is:
Go to the RViz window.
Click the 2D Pose Estimate button at the top.
Click and drag the green arrow on the map to perfectly match the robot's actual position and rotation in Gazebo. Ensure the red laser dots align perfectly with the black map lines.
Terminal 4: Start the Autonomous Delivery Loop
Once localized, run the Python manager script to start the infinite loop!

Bash


python3 ~/delivery_bot_ws/delivery_loop.py


 Engineering Challenges & Solutions (The Sim2Real Gap)
Developing this system required overcoming several core physics and localization hurdles that bridge the gap between simulation and real-world robotics.

1. Sensor Fusion: Overcoming Differential Drive Drift
The Problem: Pure wheel odometry on differential-drive robots is inherently flawed due to wheel slip and scrubbing during turns. In Gazebo, high-speed turning causes digital micro-slips, resulting in massive rotational drift and map tearing.
The Solution (EKF): I implemented an Extended Kalman Filter (EKF). The EKF acts as a mathematical judge, fusing data from the lying wheels and the digital IMU gyroscope. I configured the covariance matrix to completely ignore wheel odometry for rotation, relying solely on the IMU for Yaw. This eliminated the drift entirely.

2. Tuning AMCL: Defeating Symmetrical Aliasing & Dynamic Obstacles
The Problem: The robot navigated perfectly near walls, but when turning near identically spaced, unmapped traffic cones, the AMCL localization algorithm would panic. It assumed the cones were misplaced walls, triggering a "Kidnapped Robot" recovery state and teleporting the robot across the map.
The Solution: Deep tuning of nav2_params.yaml.
Trusting the EKF: Lowered the alpha1-4 values to 0.05 to stop AMCL from aggressively scattering guess particles, forcing it to trust the new EKF gyroscope.
Beam Skipping: Enabled do_beamskip and raised z_short to 0.2. This acts as an "anti-cone shield," forcing the robot to ignore early laser hits from unmapped dynamic objects rather than confusing them with walls.
Anti-Panic: Set recovery_alpha_fast and slow to 0.0 to explicitly disable the "Kidnapped Robot" mode, preventing teleportation during minor simulation lag spikes.

3. Gazebo Physics: The "Square Tire" Effect
The Problem: Sharp turns caused the robot to violently micro-bounce, pitching the LiDAR lasers into the ceiling and crashing the localization.
The Solution: Re-engineered the URDF's <collision> geometry. While keeping the visually appealing <cylinder> tags for the wheels, the invisible physics collisions were changed to perfectly smooth <sphere> tags. This provided a single point of contact, allowing the robot to pivot smoothly without its edges digging into the Gazebo floor grid.


Author: Bashaar Ahmed
Mechatronics Engineering Student | Mehran University of Engineering and Technology
