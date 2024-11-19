import rospy
from geometry_msgs.msg import Twist

def husky_circular():
    rospy.init_node('husky_circular_cmd_vel', anonymous=True)
    pub = rospy.Publisher('/husky_velocity_controller/cmd_vel', Twist, queue_size=10)
    twist = Twist()
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        twist.linear.x = 0.2
        twist.angular.z = 0.6
        pub.publish(twist)
        rate.sleep()

if __name__ == '__main__':
    try:
        husky_circular()
    except rospy.ROSInterruptException:
        pass