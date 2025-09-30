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
		self.timer = self.create_timer(0.1, self.leer_serial)
  
	def listener_callback(self, msg):
		self.get_logger().info("enviando")
		self.enviar_serial(msg.axes[1], msg.axes[0], msg.axes[3])
	
	def enviar_serial(self, x, y, z):
		message = struct.pack(
				'dddddd',
				x/3,      # x
				-y/3,     # y
				-z,    # z
				False,      # start_button
				False,       # back_button
				9912399
			)	
		self.ser.write(message)
		time.sleep(0.01)
  
	def leer_serial(self):
     
		s = self.ser.read(112)        # read up to ten bytes (timeout)
		print("leido de serial = ", s)
		px = struct.unpack('d',s[0:8])[0]
		py = struct.unpack('d',s[8:16])[0]
		rz = struct.unpack('d',s[16:24])[0]

		vx_read = struct.unpack('d',s[24:32])[0]
		vy_read = struct.unpack('d',s[32:40])[0]
		wz_read = struct.unpack('d',s[40:48])[0]

		velWheel1 = struct.unpack('d',s[48:56])[0]
		velWheel2 = struct.unpack('d',s[56:64])[0]
		velWheel3 = struct.unpack('d',s[64:72])[0]
		velWheel4 = struct.unpack('d',s[72:80])[0]

		control1 = struct.unpack('d',s[80:88])[0]
		control2 = struct.unpack('d',s[88:96])[0]
		control3 = struct.unpack('d',s[96:104])[0]
		control4 = struct.unpack('d',s[104:112])[0]

		vx  = vx_read
		vy  = vy_read
		vth = wz_read

		print("Vx = ", vx)
     
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
