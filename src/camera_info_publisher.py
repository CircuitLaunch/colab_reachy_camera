#!/usr/bin/env python3
import cv2
import rospy
import yaml
import sys
from sensor_msgs.msg import CameraInfo



# # create a new publisher.
# # pub = rospy.Publisher('/camera/camera_info', CameraInfo, queue_size=10)
# pub = rospy.Publisher('/camera_rect/camera_info', CameraInfo, queue_size=10)
# # initialize a node
# rospy.init_node('webcam_info_pub', anonymous=True)
# # set the loop rate (#60hz)
# rate = rospy.Rate(60)

# while not rospy.is_shutdown():
#     q=CameraInfo()
#     rospy.loginfo("Camera Info Published.")
#     q.header.frame_id='usb_cam'
#     q.height=480
#     q.width=640
#     q.D=[0.13796983883551275, -0.26531557744957884, -0.0024557862383360854, -0.004792840172407027, 0.0]
#     q.K=[676.2408716695641, 0.0, 292.4401046002648, 0.0, 673.748683410425, 241.1649747844938, 0.0, 0.0, 1.0]
#     q.R=[1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]
#     q.P=[687.402099609375, 0.0, 289.540304396025, 0.0, 0.0, 686.8453369140625, 239.766321703617, 0.0, 0.0, 0.0, 1.0, 0.0]
#     q.binning_x=0
#     q.binning_y=0
#     q.roi.y_offset=0
#     q.roi.x_offset=0
#     q.roi.height=0
#     q.roi.width=0
#     q.roi.do_rectify=False
#     pub.publish(q)
#     rate.sleep()









def image_info_pub(yaml_path):
    # create a new publisher.
    pub = rospy.Publisher('/camera_rect/camera_info', CameraInfo, queue_size=10)
    # initialize a node
    rospy.init_node('webcam_info_pub', anonymous=True)
    # set the loop rate (#60hz)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        info = parse_camera_info(yaml_path)   
        
        # publish the image
        pub.publish(info)
        rospy.loginfo("Camera Info Published.")
        rate.sleep()
    

def parse_camera_info(path):
    with open(path, "r") as file_handle:
        calibration_data = yaml.safe_load(file_handle)

    # Parse
    camera_info_msg = CameraInfo()
    camera_info_msg.header.frame_id = calibration_data["camera_name"]
    camera_info_msg.width = calibration_data["image_width"]
    camera_info_msg.height = calibration_data["image_height"]
    camera_info_msg.K = calibration_data["camera_matrix"]["data"]
    camera_info_msg.D = calibration_data["distortion_coefficients"]["data"]
    camera_info_msg.R = calibration_data["rectification_matrix"]["data"]
    camera_info_msg.P = calibration_data["projection_matrix"]["data"]
    # camera_info_msg.distortion_model = calibration_data["distortion_model"]
    return camera_info_msg


if __name__ == "__main__":  
    try:
        args = rospy.myargv(argv=sys.argv)
        if len(args) != 2:
            print("ERROR: Please provide the path for the camera calibration ost.yaml file")
            sys.exit(1)
        image_info_pub(args[1])
    except rospy.ROSInterruptException:
        pass
