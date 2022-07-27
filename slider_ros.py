#! /usr/bin/env python3

import rospy
from std_msgs.msg import Int32
import azm_slider

class SliderController():

    def __init__(self):
        self.ip = rospy.get_param('~ip')
        self.port = rospy.get_param('~port')
        self.driver = azm_slider.SliderDriver(self.ip, self.port)
        rospy.Subscriber("slider_location_cmd", Int32, self.direct_operation)

    def direct_operation(self, location):
        self.driver.direct_operation(location)


if __name__ == '__main__':
    rospy.init_node('slider')
    ctrl = SliderController()
    rospy.spin()
