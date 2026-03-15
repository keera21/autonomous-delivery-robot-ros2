import rclpy
from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped
import time

def main():
    # Start the ROS 2 Python interface
    rclpy.init()
    navigator = BasicNavigator()

    # Wait for the Nav2 brain to fully wake up
    print(" Waiting for Nav2 to become active...")
    navigator.waitUntilNav2Active()
    print("Nav2 is active! Starting delivery shift.")

    # --- SETUP PICKUP POINT (By the cones) ---
    pickup = PoseStamped()
    pickup.header.frame_id = 'map'
    pickup.pose.position.x = -3.654480457305908
    pickup.pose.position.y = 3.1697909832000732
    pickup.pose.orientation.z = 0.002680810012222123
    pickup.pose.orientation.w = 0.999996406622383

    # --- SETUP DROP-OFF POINT ---
    dropoff = PoseStamped()
    dropoff.header.frame_id = 'map'
    dropoff.pose.position.x = 5.241306304931641
    dropoff.pose.position.y = -2.6874771118164062
    dropoff.pose.orientation.z = -0.9996602511426764
    dropoff.pose.orientation.w = 0.026064962792242293

    # --- THE INFINITE DELIVERY LOOP ---
    while rclpy.ok():
        print("\n Heading to PICKUP point...")
        navigator.goToPose(pickup)
        
        # Keep checking if it has arrived yet
        while not navigator.isTaskComplete():
            time.sleep(1)
            
        print(" Arrived at Pickup! Loading cargo... (Waiting 5 seconds)")
        time.sleep(5)

        print("\n Heading to DROP-OFF point...")
        navigator.goToPose(dropoff)
        
        # Keep checking if it has arrived yet
        while not navigator.isTaskComplete():
            time.sleep(1)
            
        print(" Arrived at Drop-off! Unloading cargo... (Waiting 5 seconds)")
        time.sleep(5)

if __name__ == '__main__':
    main()

