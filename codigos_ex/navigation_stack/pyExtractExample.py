#!/usr/bin/env python
#ROS Wiki: http://wiki.ros.org/cv_bridge/Tutorials/ConvertingBetweenROSImagesAndOpenCVImagesPython
from __future__ import print_function

import roslib
import numpy as np
from numpy import asarray
from numpy import savetxt
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

arq = open("database.csv", "a")

class image_converter:

  def __init__(self):
    self.image_pub = rospy.Publisher("image_topic",Image)

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.callback)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)
    
    cv2.imshow("Image window", cv_image)
    teste =cv_image.flatten()
    print(teste[1])
    savetxt(arq, teste, delimiter=',')
    arq.write("\n")
    #savetxt('struct_array.csv', cv_image, delimiter=',', fmt=['%d' , '%d', '%d'], header='x,y,channel', comments='')
    #arq.write(teste)
    #arq.write("\n")
    #print(teste)
    cv2.waitKey(3)

    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    except CvBridgeError as e:
      print(e)

def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
arq.close()
