### Summary
The final joust is the most exciting battle of the school year, where a variety of knights take on each other as they navigate through obstacles and reach their lance over a wall in an attempt to knock each other off. Each knight will consist of some sort of a chivalrous knight — one that will gracefully admit defeat and joust fairly. The knight should involve some sort of electronics along with the MakerPi board with the implementation of motors. Lastly, the robot has to communicate to AirTable — which will initiate its movements — and use ROS2 commands to publish actions to the robot.

### What Worked
The final joust is the most exciting battle of the school year, where a variety of knights take on each other as they navigate through obstacles and reach their lance over a wall in an attempt to knock each other off. Each knight will consist of some sort of a chivalrous knight — one that will gracefully admit defeat and joust fairly. The knight should involve some sort of electronics along with the MakerPi board with the implementation of motors. Lastly, the robot has to communicate to AirTable — which will initiate its movements — and use ROS2 commands to publish actions to the robot.

### What Didn't Work
I had issues with running multiple actions consecutively, such as driving a second arc or wall following immediately after. This issue was resolved by using time.sleep(xxx) to pause in between calling each action.

### Partner
Andy Navarro Brenes
