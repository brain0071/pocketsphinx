#!/usr/bin/env python3

import rospy
import math

from geometry_msgs.msg import Twist
# import rospy, os, sys
# from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient
from std_msgs.msg import String


class Robot_server:

    def __init__(self):
        
        # robot state: wait, query, cooking.
        self.state = "wait"
        rospy.Subscriber('recognizer_1/output', String, self.receive_voice)
        self.moving_publisher = rospy.Publisher('robot_moving', Twist, queue_size=10)
        self.food_publisher = rospy.Publisher('food', String, queue_size= 1)
        self.cooking_publisher = rospy.Publisher('cooking', String, queue_size= 1)

        self.soundhandle = SoundClient()
        rospy.sleep(1)
        self.soundhandle.stopAll()
        rospy.spin()

    def receive_voice(self, msg):
        voice_text=msg.data
        rospy.loginfo("I said:: %s",voice_text)

        if self.state == "wait":
            twist = Twist()              
            # moving command
            if voice_text == "go":
                twist.linear.x = 2 
                self.moving_publisher.publish(twist)
            elif voice_text == "back":
                twist.linear.x = -2 
                self.moving_publisher.publish(twist)
            elif voice_text == "left":
                twist.angular.y = 2 
                self.moving_publisher.publish(twist)
            elif voice_text == "right":
                twist.angular.y = -2
                self.moving_publisher.publish(twist)
            elif voice_text == "stop":
                twist.linear.x = 0
                twist.linear.y = 0
                twist.linear.z = 0
                twist.angular.x = 0
                twist.angular.y = 0
                twist.angular.z = 0
                self.moving_publisher.publish(twist)

            # start query peopler  
            elif voice_text == "please":
                response = "Hello, May I help you? What food do you need?"
                self.soundhandle.say(response)
                
                self.state = "query"
                # velocity set zero
                twist.linear.x = 0
                twist.linear.y = 0
                twist.linear.z = 0
                twist.angular.x = 0
                twist.angular.y = 0
                twist.angular.z = 0
                self.moving_publisher.publish(twist)
            
            else:
                pass
               
            
        elif self.state == "query":
            
            rospy.loginfo("robot state: %s", self.state)

            food = String()
            voice_text = msg.data
            if voice_text == "apple":
                food.data = "Apple"
                self.food_publisher.publish(food)

            elif voice_text == "tomato":
                food.data = "Tomato"
                self.food_publisher.publish(food)

            elif voice_text == "sandwich":
                food.data = "Sandwich"
                self.food_publisher.publish(food)
            
            if voice_text == "ok":
                self.state = "cooking"
                
        elif self.state == "cooking":

            response = "OK, I already know what you need.I will start cooking for you"
            self.soundhandle.say(response)
            cook_state = String()
            cook_state = "start cooking"
            self.cooking_publisher.publish(cook_state)
            
            self.state = "ok"
        
        elif self.state == "ok":
            pass

if __name__=="__main__":
    rospy.init_node('robot server')
    try:
        Robot_server()
    except:
        pass

