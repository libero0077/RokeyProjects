import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import serial
import time
import os
import subprocess

class ConveyorNode(Node):
    def __init__(self):
        super().__init__('conveyor_node')
        self.get_logger().info("Conveyor Node Initialized")

        # ROS 2 Subscriber for Start/Stop Commands
        self.subscription = self.create_subscription(
            String,
            '/conveyor_command',
            self.command_callback,
            10
        )

        # USB Disconnection Publisher
        self.usb_disconnect_publisher = self.create_publisher(String, '/usb_disconnect', 10)

        # Arduino Serial Communication
        self.serial_port = '/dev/ttyACM0'  # Update with your Arduino port
        self.baud_rate = 115200
        self.arduino = None
        self.usb_disconnected = False  # Track USB disconnection status

        # Conveyor Control Flags
        self.running = False
        self.steps_to_run = 0  # Number of steps for the conveyor
        self.ensure_serial_permissions()  # Set serial permissions before connecting
        self.connect_to_arduino()

        # Timer to Monitor Arduino Status
        self.status_timer = self.create_timer(0.1, self.check_arduino_status)

    def ensure_serial_permissions(self):
        """Ensure the correct permissions for the serial port."""
        try:
            self.get_logger().info(f"Setting permissions for {self.serial_port}")
            subprocess.run(['sudo', 'chmod', '666', self.serial_port], check=True)
            self.get_logger().info(f"Permissions set for {self.serial_port}")
        except subprocess.CalledProcessError as e:
            self.get_logger().error(f"Failed to set permissions for {self.serial_port}: {e}")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {e}")

    def connect_to_arduino(self):
        """Try to connect to the Arduino serial port. Retry until successful."""
        while True:
            try:
                self.ensure_serial_permissions()  # Ensure correct permissions before connecting
                self.arduino = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
                self.get_logger().info("Connected to Arduino")
                self.usb_disconnected = False  # Reset disconnection flag
                return  # 성공적으로 연결되면 종료
            except serial.SerialException as e:
                if not self.usb_disconnected:
                    self.publish_usb_disconnect()
                    self.usb_disconnected = True
                self.get_logger().error(f"Failed to connect to Arduino: {e}")
                self.get_logger().warn("Waiting for USB reconnection...")
                time.sleep(1)  # 1초 대기 후 재시도
            
    def publish_usb_disconnect(self):
        """Publish a message indicating the USB is disconnected."""
        usb_disconnect_msg = String()
        usb_disconnect_msg.data = "USB disconnected"
        self.get_logger().warn("USB disconnected - publishing message.")
        # Add a publisher for USB disconnection events
        self.usb_disconnect_publisher.publish(usb_disconnect_msg)

    def command_callback(self, msg):
        """Handle commands from ROS to control the conveyor."""
        command = msg.data.lower()
        if command.startswith("start"):
            try:
                # Extract steps from command (e.g., "start:1000")
                self.steps_to_run = int(command.split(":")[1])
                self.start_conveyor()
            except (IndexError, ValueError):
                self.get_logger().error("Invalid start command format. Use 'start:<steps>'")
        elif command == "stop":
            self.stop_conveyor()
        else:
            self.get_logger().warn(f"Received unknown command: {command}")

    def start_conveyor(self):
        """Send steps to the Arduino to start the conveyor."""
        if not self.running:
            self.get_logger().info(f"Starting Conveyor with {self.steps_to_run} steps")
            if self.arduino and self.arduino.is_open:
                try:
                    command = f"{self.steps_to_run}\n"
                    self.arduino.write(command.encode())  # Send steps to Arduino
                    self.running = True
                except serial.SerialException as e:
                    self.get_logger().error(f"Error sending data to Arduino: {e}")
            else:
                self.get_logger().error("Arduino connection not available")
        else:
            self.get_logger().warn("Conveyor is already running")

    def stop_conveyor(self):
        """Stop the conveyor motor."""
        if self.running:
            self.get_logger().info("Stopping Conveyor")
            # Arduino doesn't have a stop command, so just log and set state
            self.running = False
        else:
            self.get_logger().warn("Conveyor is not running")

    def check_arduino_status(self):
        """Check the Arduino status and handle connection errors."""
        try:
            if self.arduino and self.arduino.is_open:
                if self.arduino.in_waiting > 0:
                    status = self.arduino.read().decode().strip()
                    if status == ".":
                        if self.running:
                            self.get_logger().info("Conveyor stopped (Ready)")
                            self.running = False
                    elif status == "_":
                        if not self.running:
                            self.get_logger().info("Conveyor Running")
                            self.running = True
                    else:
                        self.get_logger().warn(f"Unexpected Arduino status: {status}")
            else:
                self.get_logger().error("Arduino connection lost")
                if not self.usb_disconnected:
                    self.publish_usb_disconnect()
                    self.usb_disconnected = True
                self.connect_to_arduino()
        except (serial.SerialException, OSError) as e:
            self.get_logger().error(f"Error interacting with Arduino: {e}")
            if self.arduino:
                try:
                    self.arduino.close()
                except Exception as close_error:
                    self.get_logger().warn(f"Error closing Arduino connection: {close_error}")
                self.arduino = None
            if not self.usb_disconnected:
                self.publish_usb_disconnect()
                self.usb_disconnected = True
            self.get_logger().warn("Arduino disconnected. Trying to reconnect...")
            self.connect_to_arduino()

def main(args=None):
    rclpy.init(args=args)
    node = ConveyorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down Conveyor Node")
    finally:
        if node.arduino:
            node.arduino.close()
        rclpy.shutdown()
