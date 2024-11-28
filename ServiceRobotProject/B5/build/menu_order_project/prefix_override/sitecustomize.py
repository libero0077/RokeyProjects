import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/rokey/Documents/RokeyProjects/ServiceRobotProject/B5/install/menu_order_project'
