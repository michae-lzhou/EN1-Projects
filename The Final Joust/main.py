import rclpy
from rclpy.node import Node
import time, os
from rclpy.action import ActionClient

import requests

from rclpy.qos import qos_profile_sensor_data
from irobot_create_msgs.msg import IrIntensityVector
import geometry_msgs.msg

from rcl_interfaces.srv import SetParameters
from rcl_interfaces.msg import ParameterType, ParameterValue, Parameter
from irobot_create_msgs.action import WallFollow
from irobot_create_msgs.action import DriveArc
from irobot_create_msgs.action import RotateAngle
from builtin_interfaces.msg import Duration

APIKey = 'keyBGBJH9U4l7kKyv'
BaseID = 'appR1aI5gGVAWcNjU'
TableName = 'Table 1'
RecID_Start = 'recdYT6DgPHKSpODK'
IDs = [RecID_Start]

def AskAirtable():
    URL = 'https://api.airtable.com/v0/' + BaseID + '/' + TableName + '?api_key=' + APIKey
    signal = ['']

    try:
        r = requests.get(url = URL, params = {})
        data = r.json()
        for command in data['records']:
            signal[IDs.index(command['fields']['recID'])] = command['fields']['Signal']    
        return signal
    except:
        return None

class WallFollower(Node):
    def __init__(self, namespace = '/Merida'):
        #  define an action client for driving the Create
        self.done = False
        super().__init__('wall_follow_action_client')
        self._action = ActionClient(self, WallFollow, namespace + '/wall_follow')
        # note that the action client uses message type DriveDistance and we defined the namespace
        
    def set_goal(self, side = 1, time = 10):
        '''
        Set the goal of speed and distance and sets the callback to know when the goal is accepted
        '''
        self.done = False
        goal_msg = WallFollow.Goal()
        goal_msg.follow_side = side
        goal_msg.max_runtime = Duration(sec = time, nanosec = 0)

        self._action.wait_for_server()  # Wait for the server to be available and then send the goal.
        self._send_goal_future = self._action.send_goal_async(goal_msg)
        self._send_goal_future.add_done_callback(self.goal_request_callback)

    def goal_request_callback(self, future): # A callback that is executed when the future is complete.
        '''
        run this when the action server responds with either go or no-go and set up another callback for when the action is done
        '''
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            self.done = True
            return
        self.get_logger().info('Goal accepted :)')
        # goal accepted - now wait for it to be executed
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        '''
        run this when the action is done
        '''        
        result = future.result().result
        self.get_logger().info('Result: {0}'.format(result))
        self.done = True
        
class Rotate(Node):
    '''
    Set up a node, 'rotate_action_client', that is an action client and 
    will rotate the Create through a desired angle. The methods are very
    similar to those in Drive
    '''
    def __init__(self, namespace = '/Picard'):
        #  define an action client for turning the Create
        self.done = False
        super().__init__('rotate_action_client')
        self._action = ActionClient(self, RotateAngle, namespace + '/rotate_angle')
        
    def set_goal(self, angle=1.57, max_rotation_speed=0.5):
        self.done = False
        goal_msg = RotateAngle.Goal()
        goal_msg.angle = angle 
        goal_msg.max_rotation_speed = max_rotation_speed

        self._action.wait_for_server() # wait for server
        self._send_goal_future = self._action.send_goal_async(goal_msg)
        time.sleep(4)
        self._send_goal_future.add_done_callback(self.goal_response_callback)
        
    def goal_response_callback(self, future):  # execute when action server says go or no-go.
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            self.done = True
            return
        self.get_logger().info('Goal accepted :)')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):  #run when goal is completed
        result = future.result().result
        self.get_logger().info('Result: {0}'.format(result))
        self.done = True
        
class ArcDriver(Node):
    def __init__(self, namespace = '/Merida'):
        #  define an action client for driving the Create
        self.done = False
        super().__init__('drive_arc_action_client')
        self._action = ActionClient(self, DriveArc, namespace + '/drive_arc')
        # note that the action client uses message type DriveDistance and we defined the namespace
        
    def set_goal(self, trans_dir = 1, ang1 = -3.45, ang2 = 3.60, r = 0.55, r2 = 0.52):
        '''
        Set the goal of speed and distance and sets the callback to know when the goal is accepted
        '''
        self.done = False
        goal_msg = DriveArc.Goal()
        goal_msg.translate_direction = trans_dir
        goal_msg.angle = ang1
        goal_msg.radius = r
        goal_msg.max_translation_speed = 0.3

        self._action.wait_for_server()  # Wait for the server to be available and then send the goal.
        self._send_goal_future = self._action.send_goal_async(goal_msg)
        time.sleep(7)
        goal_msg.angle = ang2
        goal_msg.radius = r2
        self._send_goal_future = self._action.send_goal_async(goal_msg)
        time.sleep(7)
        self._send_goal_future.add_done_callback(self.goal_request_callback)

    def goal_request_callback(self, future): # A callback that is executed when the future is complete.
        '''
        run this when the action server responds with either go or no-go and set up another callback for when the action is done
        '''
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            self.done = True
            return
        self.get_logger().info('Goal accepted :)')
        # goal accepted - now wait for it to be executed
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        '''
        run this when the action is done
        '''        
        result = future.result().result
        self.get_logger().info('Result: {0}'.format(result))
        self.done = True
        
def main():    
    os.environ['ROS_DOMAIN_ID'] = "18"
    namespace = '/Merida'
    
    while True:
        key = AskAirtable()
        if key[0] == 'GO':
            rclpy.init()
            try:
                print('spinning up')
                create = ArcDriver(namespace)
                create.set_goal()
                create = Rotate(namespace)
                create.set_goal(-1.65)
                create = WallFollower(namespace)
                create.set_goal(30)
                rclpy.spin(create)
            except KeyboardInterrupt:
                print('\nCaught Keyboard Interrupt')
            finally:
                print("Done")
                create.destroy_node()
                rclpy.shutdown()
            break

main()
