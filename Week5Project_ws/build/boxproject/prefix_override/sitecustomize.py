import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/yjh/Doosan/Real_project_ws/Week5/Week5Project_ws/install/boxproject'
