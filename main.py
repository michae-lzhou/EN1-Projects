!export ROS_DOMAIN_ID=6

import os
os.environ['ROS_DOMAIN_ID']="6"

!printenv ROS_DOMAIN_ID
!ros2 topic list
!ros2 topic pub --once /Woody/cmd_audio irobot_create_msgs/msg/AudioNoteVector "{append: false, notes: [{frequency: 440, max_runtime: {sec: 1,nanosec: 0}}, {frequency: 880, max_runtime: {sec: 1,nanosec: 0}}]}"

from Subs.CreateLib import Create

fred = Create('/Woody')
fred.LED(6)
fred.beep(440)
fred.turn(90)
fred.forward(0.5)
fred.close()

from Subs.CreateLib import Create

MyCreate = Create('/Woody')

MyCreate.beep()
MyCreate.LED(2)
MyCreate.forward(0.5)
MyCreate.turn(90)
# and more - add on and mix them up
MyCreate.close()
