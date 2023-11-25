import rclpy
from rclpy.node import Node
import time, os
from rclpy.action import ActionClient

from rclpy.qos import qos_profile_sensor_data
from irobot_create_msgs.msg import IrIntensityVector
import geometry_msgs.msg

from rcl_interfaces.srv import SetParameters
from rcl_interfaces.msg import ParameterType, ParameterValue, Parameter

class Move(Node):
    def __init__(self, namespace = '/Merida'):
        '''
        define the node and the publisher
        '''
        super().__init__('twist_publisher')
        self.twist_publisher = self.create_publisher(geometry_msgs.msg.Twist, namespace + '/cmd_vel', 10)
        
    def move(self, x,y,z,th, speed, turn):
        '''
        publish the desired twist
        '''
        twist = geometry_msgs.msg.Twist()
        twist.linear.x = x * speed
        twist.linear.y = y * speed
        twist.linear.z = z * speed
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = th * turn
        self.twist_publisher.publish(twist)

class Proximity(Node):
    '''
    Set up a node that lets you subscribe to the battery level
    '''
    def __init__(self, namespace = '/Merida'):   
        '''
        define the node and set up the subscriber
        '''
        super().__init__('proximity_sensor_subscription') #name it anything you want - this is what will appear in the ros topic list
        
        self.subscription = self.create_subscription(IrIntensityVector, namespace + '/ir_intensity', self.callback, qos_profile_sensor_data)
        self.done = False
        
    def callback(self, msg: IrIntensityVector):
        self.names = [h.header.frame_id for h in msg.readings]
        self.value = [h.value for h in msg.readings]
        self.done = True   # tell the parent program you are done - you have data
        
class Safety(Node):
    def __init__(self, namespace = '/Merida'):
        super().__init__('linefollow');
        self.params_client = self.create_client(SetParameters, namespace + '/motion_control/set_parameters')
        
    def Set(self, task):
        options = ['full','backup_only','none']
        if not task in options:
            return None
        request = SetParameters.Request()
        param = Parameter()
        param.name = "safety_override"
        param.value.type = ParameterType.PARAMETER_STRING
        param.value.string_value = task
        request.parameters.append(param)
        
        print('setting safety to ' + task,end='')
        self.params_client.wait_for_service()
        print(' ... ',end='')
        self.future = self.params_client.call_async(request)
        print('done')
        
    def AllOn(self):
        self.Set('none')
        
    def Backup(self):
        self.Set('backup_only')
        
    def AllOff(self):
        self.Set('full')
        
def main():
    rclpy.init()
    
    os.environ['ROS_DOMAIN_ID'] = "18"
    namespace = '/Merida'
    
    create = Proximity(namespace)
    
    try:
        #create.safety.Set('backup_only')
        print('spinning up')
        rclpy.spin(create)
    except KeyboardInterrupt:
        print('\nCaught Keyboard Interrupt')
    finally:
        print("Done")
        #create.safety.Set('none')
        create.destroy_node()
        rclpy.shutdown()
        
main()
