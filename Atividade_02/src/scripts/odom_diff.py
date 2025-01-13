# ODOM DIFF
# Author: André Paiva Conrado Rodrigues
# PPGEE - UFBA - 2024.2

import rospy
from tf.transformations import euler_from_quaternion
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, Pose


# Diff Calc Funcion

def diff(measure, gt):
    measure_quat = [measure.orientation.x, measure.orientation.y,
                    measure.orientation.z, measure.orientation.w]
    gt_quat = [gt.orientation.x, gt.orientation.y,
               gt.orientation.z, gt.orientation.w]
    (m_r, m_p, m_y) = euler_from_quaternion(measure_quat)
    (gt_r, gt_p, gt_y) = euler_from_quaternion(gt_quat)
    diff = Twist()
    diff.linear.x = measure.position.x - gt.position.x
    diff.linear.y = measure.position.y - gt.position.y
    diff.linear.z = measure.position.z - gt.position.z
    diff.angular.x = m_r - gt_r
    diff.angular.y = m_p - gt_p
    diff.angular.z = m_y - gt_y
    return diff


# Odom Diff Class

class odom_diff():
    # Class function for creating map relations
    def __init__(self):
        rospy.init_node('odom_diff_node')
        self.rate = rospy.Rate(10)
        self.gt_pose = Pose()
        self.wheel_odom_pose = Pose()
        self.fusion_pose = Pose()
        
        # Publishers
        self.pub_wheel = rospy.Publisher("/odom_diff/wheel", Twist, queue_size=10)
        self.pub_fusion = rospy.Publisher("/odom_diff/fusion", Twist, queue_size=10)
        # Subscribers
        rospy.Subscriber("/gazebo_ground_truth/odom", Odometry, self.ground_truth_callback)
        rospy.Subscriber("/husky_velocity_controller/odom", Odometry, self.wheel_odom_callback)
        rospy.Subscriber("/odometry/filtered", Odometry, self.fusion_callback)

    def ground_truth_callback(self, data):
        self.gt_pose = data.pose.pose
        wheel_diff = diff(self.wheel_odom_pose, self.gt_pose)
        fusion_diff = diff(self.fusion_pose, self.gt_pose)
        rospy.loginfo("Wheel Diff: %f %f %f %f %f %f", wheel_diff.linear.x,
                                                    wheel_diff.linear.y,
                                                    wheel_diff.linear.z,
                                                    wheel_diff.angular.x,
                                                    wheel_diff.angular.y,
                                                    wheel_diff.angular.z)
        self.pub_wheel.publish(wheel_diff)
        self.pub_fusion.publish(fusion_diff)

    def wheel_odom_callback(self, data):
        self.wheel_odom_pose = data.pose.pose

    def fusion_callback(self,data):
        self.fusion_pose = data.pose.pose

    def main(self):
        rospy.spin()

if __name__ == '__main__':
    try:
        diff_node = odom_diff()
        diff_node.main()
    finally:
        pass