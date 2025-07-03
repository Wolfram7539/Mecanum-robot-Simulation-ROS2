#!/usr/bin/env python3
import tkinter as tk
from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node

class TeleopGUI(Node):
    def __init__(self):
        super().__init__('teleop_gui')
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.root = tk.Tk()
        self.root.title('Cmd_vel Teleop')
        self.build_ui()
        # rclpy spin がブロックしないよう起動後は手動で Tk のループ

    def build_ui(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        btn_forward = tk.Button(frame, text='↑前進', width=8,
                                command=lambda: self.send_cmd(0.5, 0.0))
        btn_backward = tk.Button(frame, text='↓後退', width=8,
                                command=lambda: self.send_cmd(-0.5, 0.0))
        btn_left = tk.Button(frame, text='←左移動', width=8,
                                command=lambda: self.send_cmd(0.0, 0.5))
        btn_right = tk.Button(frame, text='→右移動', width=8,
                                command=lambda: self.send_cmd(0.0, -0.5))
        btn_ccw = tk.Button(frame, text='⟲左回転', width=8,
                                command=lambda: self.send_cmd(0.0, 0.0, 0.5))
        btn_cw = tk.Button(frame, text='⟳右回転', width=8,
                                command=lambda: self.send_cmd(0.0, 0.0, -0.5))
        btn_stop = tk.Button(frame, text='停止', width=8,
                                command=self.send_stop)

        btn_forward.grid(row=0, column=1)
        btn_left.grid(row=1, column=0)
        btn_stop.grid(row=1, column=1)
        btn_right.grid(row=1, column=2)
        btn_backward.grid(row=2, column=1)
        btn_ccw.grid(row=3, column=0, columnspan=2)
        btn_cw.grid(row=3, column=1, columnspan=2)

    def send_cmd(self, lin_x=0.0, lin_y=0.0, ang_z=0.0):
        msg = Twist()
        msg.linear.x = lin_x
        msg.linear.y = lin_y
        msg.angular.z = ang_z
        self.pub.publish(msg)
        self.get_logger().info(f'cmd_vel → linear({lin_x:.2f}, {lin_y:.2f}) angular({ang_z:.2f})')

    def send_stop(self):
        self.send_cmd(0.0, 0.0, 0.0)

    def run(self):
        # tkinter と rclpy の並列処理：tkinter イベントループ内で定期的に spin_once
        def periodic_spin():
            rclpy.spin_once(self, timeout_sec=0)
            self.root.after(50, periodic_spin)
        self.root.after(50, periodic_spin)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def on_close(self):
        self.destroy_node()
        rclpy.shutdown()
        self.root.destroy()

def main():
    rclpy.init()
    gui = TeleopGUI()
    gui.run()

if __name__ == '__main__':
    main()
