#!/usr/bin/env python3
import cv2
import sys
from sensor_msgs.msg import Image
import rospy
from cv_bridge import CvBridge, CvBridgeError


'''
wiki: http://wiki.ros.org/apriltag_ros
'''

def image_pub(cam_device):
    # create a new publisher.
    pub = rospy.Publisher('/camera_rect/image_rect', Image, queue_size=1)
    # initialize a node
    rospy.init_node('webcam_pub', anonymous=True)
    # set the loop rate (#60hz)
    rate = rospy.Rate(10)

    # create a camera object
    cam = cv2.VideoCapture(cam_device)

    # check if camera is available
    if not cam.isOpened():
        sys.stdout.write("Webcam is not available")
        return False
    
    while not rospy.is_shutdown():
        ret, frame = cam.read()
        bridge = CvBridge()
        image_msg = bridge.cv2_to_imgmsg(frame,encoding="bgr8")

        # if ret:
        #     rospy.loginfo("Image Captured")
        
        # publish the image
        pub.publish(image_msg)
        rate.sleep()
    
if __name__ == "__main__":  
    try:
        args = rospy.myargv(argv=sys.argv)
        if len(args) != 2:
            print("ERROR: Please provide the dev for the camera (e.g. /dev/video2)")
            sys.exit(1)
        image_pub(args[1])

    except rospy.ROSInterruptException:
        pass
