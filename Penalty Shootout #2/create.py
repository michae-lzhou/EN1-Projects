ros2 action send_goal Syndrome/move_forward irobot_create_msgs/action/MoveForward "{distance: 1,max_movement_speed: 0.5}"

ros2 action send_goal Syndrome/rotate_angle irobot_create_msgs/action/RotateAngle "{angle: 0.3,max_rotation_speed: 0.5}"
