#!/usr/bin/env python3
import cv2
import sys
from sensor_msgs.msg import Image
import rospy
from cv_bridge import CvBridge, CvBridgeError


'''
wiki: http://wiki.ros.org/apriltag_ros
         '''

def image_pub():
    # create a new publisher.
    pub = rospy.Publisher('/camera_rect/image_rect', Image, queue_size=1)
    # initialize a node
    rospy.init_node('webcam_pub', anonymous=True)
    # set the loop rate (#60hz)
    rate = rospy.Rate(60)

    # create a camera object
    cam = cv2.VideoCapture("/dev/video2")

    # check if camera is available
    if not cam.isOpened():
        sys.stdout.write("Webcam is not available")
        return False
    
    while not rospy.is_shutdown():
        ret, frame = cam.read()
        bridge = CvBridge()
        image_msg = bridge.cv2_to_imgmsg(frame,encoding="bgr8")

        if ret:
            rospy.loginfo("Image Captured")
        
        # publish the image
        pub.publish(image_msg)
        rate.sleep()
    
if __name__ == "__main__":  
    try:
        image_pub()
    except rospy.ROSInterruptException:
        pass
