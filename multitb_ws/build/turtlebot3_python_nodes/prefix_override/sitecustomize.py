import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/rokey/Documents/RokeyProjects/multitb_ws/install/turtlebot3_python_nodes'
