#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
global energy
energy = 100
class move_bot:
    def __init__(self) -> None:
        rospy.init_node("move_node", anonymous=True)
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        rospy.Subscriber("/nadeef_command", String, self.callback)
    def callback(self, command):
        rospy.loginfo("Command received: " + command.data)

        direction = command.data
        velocity = Twist()
        global energy
        if direction.lower()=='forward':
            velocity.linear.x = 1.0
            velocity.linear.y = 0.0
            velocity.linear.z = 0.0
            energy = energy - 1
        elif direction.lower()=='backward':
            velocity.linear.x = -1.0
            velocity.linear.y = 0.0
            velocity.linear.z = 0.0
            energy = energy - 1
        elif direction.lower()=='left':
            velocity.angular.z = 1.0
            velocity.linear.y = 0.0
            velocity.linear.z = 0.0
            energy = energy - 1
        elif direction.lower()=='right':
            velocity.angular.z = -1.0
            velocity.linear.y = 0.0
            velocity.linear.z = 0.0
            energy = energy - 1
        elif direction.lower()=='stop':
            velocity.linear.x = 0.0
            velocity.linear.y = 0.0
            velocity.linear.z = 0.0
            velocity.angular.z = 0.0
        elif direction.lower()=='kaboom':
            energy = 100
        else:
            rospy.loginfo("Wrong command")
        try:
            if energy > 0:
                
                self.pub.publish(velocity)
                
            else:
                rospy.loginfo("Energy finished.")
        except:
            rospy.loginfo("AN ERROR OCCURED")
        rospy.loginfo("Remaining energy: " + str(energy))
if __name__=='__main__':
    node = move_bot()
    rospy.spin()