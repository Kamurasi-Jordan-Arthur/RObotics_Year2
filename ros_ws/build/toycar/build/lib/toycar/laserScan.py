import rclpy
from rclpy.node import Node

from sensor_msgs.msg import LaserScan 
from geometry_msgs.msg import Twist


class Scan_pre_process(Node):

    def __init__(self):
        super().__init__('scan_pre_process')
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.listener_callback,
            10)
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)        
        self.subscription  # prevent unused variable warning

    def listener_callback(self, scan):
        readings = {
            'R' : min(scan.ranges[0:99]),
            'FR' : min(scan.ranges[100:199]),
            'F' : min(scan.ranges[200:299]),
            'FL' : min(scan.ranges[300:399]),
            'L' : min(scan.ranges[400:499]),

        }

        for x in readings:
            if readings[x]>0.380:
                readings[x] = .380;


        self.get_logger().info('L: "%s"' % readings["L"])

        self.get_logger().info('FL: "%s"' % readings["FL"])

        self.get_logger().info('F: "%s"' % readings['F'] )

        self.get_logger().info('FR: "%s"' % readings ['FR'])

        self.get_logger().info('R: "%s"' % readings['R'])

        drive= Twist()
        JustDrive = True

        # checking if any obstacle
        for x in readings.values() :
            if x < 0.372:
                JustDrive = False
                if readings['F'] <= 0.380:
                    if readings['FL'] > readings['FR']:
                        drive.angular.z=0.65
                    elif readings['FL'] < readings['FR']:
                        drive.angular.z = -0.65
                    else:
                        if readings['L'] >= readings['R']:
                            drive.angular.z = 0.65
                        else:
                            drive.angular.z = -0.65
                elif readings['FL'] < 0.380 or readings['FR'] <0.380:
                    drive.linear.x = .25
                    if readings['FL'] > readings['FR']:
                        drive.angular.z = 0.45
                    elif readings['FL'] < readings['FR']:
                        drive.angular.z = -0.45
                    else:
                        if readings['L'] >= readings['R']:
                            drive.angular.z = 0.45
                        else:
                            drive.angular.z = -0.45
                elif readings['L'] < 0.380 or readings['R'] < 0.380:
                    drive.linear.x = .45
                    if readings['L'] > readings['R']:
                            drive.angular.z = 0.35
                    elif readings['L'] < readings['R']:
                            drive.angular.z = -0.35
                    else:
                      drive.linear.x=0.65

                break

        # if no deteted obstacle    
        if JustDrive:
            drive.linear.x=0.8

        self.publisher_.publish(drive)









def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = Scan_pre_process()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()