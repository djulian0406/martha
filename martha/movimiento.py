import time
import serial
import struct
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy

# Use with: ros2 run joy joy_node

class movimiento(Node):
	def __init__(self):
		super().__init__('Movimiento')
		self.get_logger().info("Nodo Movimiento iniciado")
		self.subscription = self.create_subscription(
			Joy,
			'joy',
			self.listener_callback,
			10
		)
		self.subscription
		self.get_logger().info("Nodo Test suscrito al tópico 'teclas'.")
		self.ser = serial.Serial('/dev/ttyACM1', 115200, timeout=0.0025)
  
	def listener_callback(self, msg):
		self.get_logger().info("enviando")
		self.enviar_serial(msg.axes[1], msg.axes[0], msg.axes[3])
	
	def enviar_serial(self, x, y, z):
		message = struct.pack(
				'dddddd',
				x/2,      # x
				y/2,     # y
				-z/2,    # z
				False,      # start_button
				False,       # back_button
				9912399
			)	
		self.ser.write(message)
		time.sleep(0.01)
     
def main(args=None):
	rclpy.init(args=args)
	nodo = movimiento()
	try:
		rclpy.spin(nodo)
	except KeyboardInterrupt:
		pass
	finally:
		message = struct.pack(
				'dddddd',
				0.0,      # x
				0.0,     # y
				0.0,    # z
				False,      # start_button
				False,       # back_button
				9912399
			)
		nodo.ser.write(message)
		nodo.ser.close()
		nodo.destroy_node()
		rclpy.shutdown()
   
if __name__ == '__main__':
    main()
