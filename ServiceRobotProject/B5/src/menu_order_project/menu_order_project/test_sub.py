import sys
import threading
import json
import re

# ROS2 관련 모듈 임포트
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy  # QoS 설정을 위해 필요
from std_msgs.msg import String  # ROS 메시지 타입

# PyQt5 관련 모듈 임포트
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QDialog, QCheckBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QObject

########################### 서비스 인터페이스 임포트 #############################
from menu_order_interfaces.srv import MenuUpdate, MenuTable  # 메뉴 정보, 주문 결과를 보내기 위한 서비스
from menu_order_project.check_data_pyqt5 import RestaurantApp
import menu_order_project.db_manager as db

'''
주문 처리 결과를 테이블 오더 노드로 전달하기 위해서는 주방 디스플레이 노드가 테이블 오더 노드에게 "주문 처리 결과를 받아달라"라고 요청을 보냄
따라서, 주방 디스플레이 노드가 서비스 클라이언트, 테이블 오더 노드가 서비스 서버가 됨
'''

# 시그널을 정의하기 위한 클래스
class Signaler(QObject):
    # 문자열을 전달하는 시그널 정의
    order_received = pyqtSignal(str)

# Signaler 인스턴스 생성
signaler = Signaler()

# ROS 노드 클래스 정의
class KitchenSubscriber(Node):
    def __init__(self):
        super().__init__('kitchen_subscriber')  # 노드 이름 설정

        # 메시지 전달 품질(QoS) 설정 (신뢰성 보장)
        qos_profile = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)

        # 'order_topic' 토픽을 구독하는 구독자 생성
        self.subscription = self.create_subscription(
            String,
            'order_topic',
            self.order_callback,
            qos_profile
        )

        ########################## 메뉴 테이블을 제공하기 위한 서비스 서버 생성 #############################
        self.menu_service = self.create_service(
            MenuTable,  # 서비스 타입
            'menu_table_service',  # 서비스 이름
            self.handle_table_request  # 요청 처리 콜백 함수
        )
        self.get_logger().info("Menu table service ready.")
        ###############################################################################################

        ########################## 주문 결과를 보내기 위한 서비스 클라이언트 생성 #############################
        self.cli = self.create_client(MenuUpdate, 'order_result_service')

        # 서비스가 준비될 때까지 대기
        '''
        서비스 서버가 준비될 때까지 대기
        서비스 서버가 실행되기 전에 클라이언트가 요청을 보내면 에러가 발생할 수 있으므로, 안전하게 대기하는 과정
        '''
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for order_result_service...')

        # 서비스 요청 객체 생성
        self.req = MenuUpdate.Request()
        ###############################################################################################

        #################### 'robot_command' 토픽에 퍼블리셔 생성 #########################################
        self.robot_command_publisher = self.create_publisher(String, 'robot_command', qos_profile)
        self.get_logger().info("Robot Command Publisher Initialized.")
        ##############################################################################################

    def publish_robot_command(self, command_dict):  # 로봇 제어 명령과 관련하여 토픽 퍼브리시
        """로봇 제어 명령을 'robot_command' 토픽으로 퍼블리시하는 함수"""
        msg = String()
        msg.data = json.dumps(command_dict)
        self.robot_command_publisher.publish(msg)
        self.get_logger().info(f"Published robot command: {msg.data}")

    def handle_table_request(self, request, response):
        """ 메뉴 테이블 요청 처리 """
        if request.request_type == 'get_menu_table':
            try:
                # 데이터베이스 연결 및 메뉴 데이터 가져오기
                conn = db.db_connection()
                cursor = conn.cursor()

                cursor.execute('SELECT * FROM menu')
                table_rows = cursor.fetchall()

                # 컬럼 이름 가져오기
                columns = [desc[0] for desc in cursor.description]

                conn.close()

                # 테이블 데이터를 딕셔너리로 변환하여 직렬화
                response.table_data = [json.dumps(dict(zip(columns, row))) for row in table_rows]
                self.get_logger().info(f"Sending full table data with {len(table_rows)} rows.")
            except Exception as e:
                self.get_logger().error(f"Failed to fetch table data: {e}")
                # 에러 메시지를 문자열 리스트로 설정
                response.table_data = ["Error: Unable to fetch table data"]
        else:
            # 잘못된 요청 유형 처리
            response.table_data = ["Error: Invalid request type"]

        return response

    def send_order_result(self, result_message):
        # 결과 메시지를 서비스 요청에 설정
        self.req.result_message = result_message

        # 비동기 방식으로 서비스 호출
        self.future = self.cli.call_async(self.req)

        # 서비스 응답이 도착하면 호출될 콜백 함수 등록
        self.future.add_done_callback(self.response_callback)

    def response_callback(self, future):
        try:
            # 서비스 응답 결과 받기
            response = future.result()

            # 응답 결과를 로그로 출력
            self.get_logger().info(f"Order result acknowledged: {response.success}")
        except Exception as e:
            # 에러 발생 시 로그로 출력
            self.get_logger().error(f"Service call failed: {e}")

    def order_callback(self, msg):
        """주문 메시지를 받으면 호출되는 콜백 함수"""
        # 받은 메시지를 로그로 출력
        self.get_logger().info(f"Received order: {msg.data}")

        # 시그널을 통해 GUI로 메시지를 전달
        signaler.order_received.emit(msg.data)

# 팝업 창 클래스 정의
class ControlPopup(QDialog):
    def __init__(self, subscriber_node, table_id, orders):
        super().__init__()
        self.subscriber_node = subscriber_node
        self.table_id = table_id
        self.orders = orders  # 주문 데이터를 저장합니다.
        self.checkbox_widgets = []  # 체크박스 위젯들을 저장할 리스트 추가 : 해당 메뉴들을 배송했다면, 체크박스가 선택된채로 고정되게 하기 위함
        self.init_ui()

    def init_ui(self):
        """팝업 창의 UI 설정"""
        if isinstance(self.table_id, int):
            self.setWindowTitle(f"Control Robot - Table {self.table_id}")
        else:
            self.setWindowTitle(f"Control Robot - {self.table_id.capitalize()} Position")
        self.setFixedSize(600, 600)  # 창 크기를 늘립니다.

        layout = QVBoxLayout()

        # 팝업 설명 레이블
        if isinstance(self.table_id, int):
            label = QLabel(f"Order Details for Table {self.table_id}")
        else:
            label = QLabel(f"Order Details for {self.table_id.capitalize()} Position")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # 주문 데이터를 주문 번호 순서대로 정렬
        sorted_orders = sorted(self.orders, key=lambda x: x['order_number'])

        # 주문 내용을 표시하는 테이블 위젯을 추가합니다.
        self.order_table = QTableWidget()
        self.order_table.setRowCount(len(sorted_orders))
        self.order_table.setColumnCount(6)
        self.order_table.setHorizontalHeaderLabels(["Select", "Order Number", "Table Number", "Menu", "Quantity", "Price"])
        self.order_table.verticalHeader().setVisible(False)
        self.order_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for row, order in enumerate(sorted_orders):
            # 주문 데이터를 가져옵니다.
            order_number = order['order_number']
            menu = order['item']
            quantity = order['quantity']
            price = order['price']
            checked = order.get('checked', False)
            disabled = order.get('disabled', False)

            # 체크박스 추가
            checkbox = QCheckBox()
            checkbox.setChecked(checked)
            checkbox.setEnabled(not disabled)  # 비활성화 상태 적용
            self.order_table.setCellWidget(row, 0, checkbox)
            self.checkbox_widgets.append(checkbox)  # 체크박스를 리스트에 추가

            self.order_table.setItem(row, 1, QTableWidgetItem(str(order_number)))
            self.order_table.setItem(row, 2, QTableWidgetItem(str(self.table_id)))
            self.order_table.setItem(row, 3, QTableWidgetItem(menu))
            self.order_table.setItem(row, 4, QTableWidgetItem(str(quantity)))
            self.order_table.setItem(row, 5, QTableWidgetItem(str(price)))

        layout.addWidget(self.order_table)

        # 로봇 제어 버튼들을 추가합니다.
        self.waiting_button = QPushButton("Move to Waiting Position")
        self.waiting_button.clicked.connect(self.move_to_waiting)

        self.kitchen_button = QPushButton("Move to Kitchen Position")
        self.kitchen_button.clicked.connect(self.move_to_kitchen)

        self.start_button = QPushButton("Start Robot")
        self.start_button.clicked.connect(self.start_robot)

        # 버튼들을 가로로 배치합니다.
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.waiting_button)
        button_layout.addWidget(self.kitchen_button)
        button_layout.addWidget(self.start_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def move_to_waiting(self):
        """대기 위치로 이동 명령 퍼블리시"""
        command = {
            "command": "move",
            "position": "waiting"
        }
        self.subscriber_node.publish_robot_command(command)
        QMessageBox.information(self, "Robot Control", "Robot is moving to Waiting Position.")
        self.close()

    def move_to_kitchen(self):
        """주방 위치로 이동 명령 퍼블리시"""
        command = {
            "command": "move",
            "position": "kitchen"
        }
        self.subscriber_node.publish_robot_command(command)
        QMessageBox.information(self, "Robot Control", "Robot is moving to Kitchen Position.")
        self.close()

    def start_robot(self):
        """해당 테이블로 이동 명령 퍼블리시"""
        if isinstance(self.table_id, int):
            position_key = f"table_{self.table_id}"
            command = {
                "command": "move",
                "position": position_key
            }
            self.subscriber_node.publish_robot_command(command)
            QMessageBox.information(self, "Robot Control", f"Robot is moving to Table {self.table_id}.")

            ################## 선택된 체크박스를 비활성화하고 상태를 주문 데이터에 저장 ################################
            for checkbox, order in zip(self.checkbox_widgets, self.orders):
                if checkbox.isChecked():
                    checkbox.setEnabled(False)  # 체크된 체크박스를 비활성화
                    order['checked'] = True
                    order['disabled'] = True
            # 팝업 창을 닫지 않고 그대로 유지하여 상태 변화를 보여줍니다.
            # self.close()
        else:
            QMessageBox.warning(self, "Robot Control", "Invalid Table ID.")

# GUI 클래스 정의
class KitchenMonitoring(QMainWindow):
    def __init__(self, subscriber_node):
        super().__init__()
        self.subscriber_node = subscriber_node  # ROS 노드 저장

        # 시그널과 슬롯 연결
        signaler.order_received.connect(self.update_order_details)

        # 테이블별 주문 데이터 초기화 (테이블 1~9번)
        self.table_data = {i + 1: [] for i in range(9)}

        # 주문 대기 번호 초기화
        self.order_counter = 1

        # 테이블 번호를 위치 키로 매핑
        self.table_position_keys = {
            1: 'table_1',
            2: 'table_2',
            3: 'table_3',
            4: 'table_4',
            5: 'table_5',
            6: 'table_6',
            7: 'table_7',
            8: 'table_8',
            9: 'table_9',
        }

        # 총 가격을 표시할 레이블 생성
        self.total_price_label = QLabel("Total price: 0원", alignment=Qt.AlignRight)
        self.order_total_price_label = QLabel("Total price: 0원", alignment=Qt.AlignRight)

        # 창 제목과 크기 설정
        self.setWindowTitle("Kitchen Display")
        self.setGeometry(100, 100, 1120, 600)

        # 메인 레이아웃 생성
        main_widget = QWidget(self)
        main_layout = QGridLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # 왼쪽 패널: 테이블 상태 표시 및 Statistics 버튼 추가
        self.left_layout = QVBoxLayout()
        self.table_status_widget = self.create_table_status_panel()
        self.left_layout.addWidget(self.table_status_widget)

        # Statistics 버튼 추가
        self.statistics_button = QPushButton("Statistics")
        self.statistics_button.clicked.connect(self.show_statistics)
        self.left_layout.addWidget(self.statistics_button)

        left_widget = QWidget()
        left_widget.setLayout(self.left_layout)
        main_layout.addWidget(left_widget, 0, 0)

        # 오른쪽 패널: 주문 상세 정보 및 대기 주문 정보, 서빙 로봇 제어 버튼들 추가
        self.right_layout = QVBoxLayout()
        self.order_detail_widget = self.create_order_detail_panel()
        self.cumulative_order_widget = self.create_cumulative_order_panel()

        self.right_layout.addWidget(self.order_detail_widget)
        self.right_layout.addWidget(self.cumulative_order_widget)

        right_widget = QWidget()
        right_widget.setLayout(self.right_layout)
        main_layout.addWidget(right_widget, 0, 1)

        # 테이블 버튼 클릭 시 팝업 창을 여는 시그널 연결
        for button in self.table_buttons:
            button.clicked.connect(self.open_control_popup)

    def create_table_status_panel(self):
        """테이블 상태를 보여주는 패널 생성"""
        layout = QVBoxLayout()

        # 패널 제목 레이블 생성
        table_status_label = QLabel("Table Status", alignment=Qt.AlignCenter)
        table_status_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(table_status_label)

        # 테이블 버튼을 담을 그리드 레이아웃 생성
        grid_layout = QGridLayout()
        self.table_buttons = []  # 테이블 버튼 리스트

        for i in range(9):
            # 각 테이블에 대한 버튼 생성
            button = QPushButton(f"Table {i + 1}\n0")  # 초기 상태는 0
            button.setFixedSize(180, 180)  # 버튼 크기 설정
            grid_layout.addWidget(button, i // 3, i % 3)  # 그리드에 버튼 추가
            self.table_buttons.append(button)  # 버튼 리스트에 추가

        layout.addLayout(grid_layout)

        # 총 가격 레이블 추가
        layout.addWidget(self.total_price_label)

        # 레이아웃을 위젯으로 감싸서 반환
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def create_order_detail_panel(self):
        """주문 상세 정보를 보여주는 패널 생성"""
        layout = QVBoxLayout()

        # 패널 제목 레이블 생성
        order_detail_label = QLabel("Specific order information", alignment=Qt.AlignCenter)
        order_detail_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(order_detail_label)

        # 주문 상세 정보를 표시할 테이블 위젯 생성
        self.order_table = QTableWidget()
        self.order_table.setRowCount(0)  # 초기 행 개수는 0
        self.order_table.setColumnCount(5)  # 열 개수는 4개
        self.order_table.setHorizontalHeaderLabels(["Order Number", "Table Number", "Menu", "Quantity", "Price"])  # 열 제목 설정
        self.order_table.verticalHeader().setVisible(False)  # 왼쪽 행 번호 숨기기

        # 열 크기를 균등하게 조절
        header = self.order_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.order_table)

        # 주문 총 가격 레이블 추가
        layout.addWidget(self.order_total_price_label)

        # 'Accept'와 'Cancel' 버튼 생성 및 레이아웃에 추가
        button_layout = QHBoxLayout()
        self.accept_button = QPushButton("Accept")
        self.cancel_button = QPushButton("Cancel")
        self.accept_button.clicked.connect(self.handle_accept)  # 'Accept' 버튼 클릭 시 처리 함수 연결
        self.cancel_button.clicked.connect(self.handle_cancel)  # 'Cancel' 버튼 클릭 시 처리 함수 연결
        button_layout.addWidget(self.accept_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        # 레이아웃을 위젯으로 감싸서 반환
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def create_cumulative_order_panel(self):
        """대기 주문 정보를 보여주는 패널 생성"""
        layout = QVBoxLayout()

        # 패널 제목 레이블 생성
        cumulative_order_label = QLabel("Waiting order information", alignment=Qt.AlignCenter)
        cumulative_order_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(cumulative_order_label)

        # 대기 주문 정보를 표시할 테이블 위젯 생성
        self.cumulative_table = QTableWidget()
        self.cumulative_table.setRowCount(0)  # 초기 행 개수는 0
        self.cumulative_table.setColumnCount(5)  # 열 개수는 5개
        self.cumulative_table.setHorizontalHeaderLabels(["Order number", "Table number", "Menu", "Quantity", "Price"])
        self.cumulative_table.verticalHeader().setVisible(False)  # 왼쪽 행 번호 숨기기

        # 열 크기를 균등하게 조절
        header = self.cumulative_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.cumulative_table)

        # 레이아웃을 위젯으로 감싸서 반환
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def update_order_details(self, message):
        """ROS 토픽으로부터 받은 주문 정보를 화면에 업데이트"""
        try:
            # 받은 메시지를 JSON 형식으로 파싱
            data = json.loads(message)
            table_id = data["table_id"]  # 테이블 번호
            orders = data["orders"]      # 주문 목록

            ###### 주문 번호 할당 : 한 번에 들어온 주문은 주문 번호가 같아야 함####
            order_number = self.order_counter
            self.order_counter += 1  # 주문 번호 증가
            ############################################################

            # 주문에 'order_number'와 상태 필드 추가
            for order in orders:
                order['order_number'] = order_number
                order['checked'] = False
                order['disabled'] = False

            if self.order_table.rowCount() == 0:
                # 현재 처리 중인 주문이 없으면 주문 상세 정보에 추가
                for order in orders:
                    row_count = self.order_table.rowCount()
                    self.order_table.insertRow(row_count)
                    self.order_table.setItem(row_count, 0, QTableWidgetItem(str(order['order_number'])))  # Order Number
                    self.order_table.setItem(row_count, 1, QTableWidgetItem(str(table_id)))
                    self.order_table.setItem(row_count, 2, QTableWidgetItem(order["item"]))
                    self.order_table.setItem(row_count, 3, QTableWidgetItem(str(order["quantity"])))
                    self.order_table.setItem(row_count, 4, QTableWidgetItem(str(order["price"])))
            
                # 데이터베이스에 주문 기록 저장
                '''
                self.save_order_to_database(table_id, orders)
                '''

            else:
                # 현재 처리 중인 주문이 있으면 대기 주문 정보에 추가
                for order in orders:
                    row_count = self.cumulative_table.rowCount()
                    self.cumulative_table.insertRow(row_count)
                    self.cumulative_table.setItem(row_count, 0, QTableWidgetItem(str(order['order_number'])))  # Order Number
                    self.cumulative_table.setItem(row_count, 1, QTableWidgetItem(str(table_id)))
                    self.cumulative_table.setItem(row_count, 2, QTableWidgetItem(order["item"]))
                    self.cumulative_table.setItem(row_count, 3, QTableWidgetItem(str(order["quantity"])))
                    self.cumulative_table.setItem(row_count, 4, QTableWidgetItem(str(order["price"])))

                ################3 데이터베이스에 대기 주문 기록 저장 #########################
                '''
                self.save_waiting_order_to_database(order_number, table_id, orders)
                '''

        except json.JSONDecodeError:
            # 메시지 파싱 실패 시 에러 로그 출력
            self.subscriber_node.get_logger().error("Failed to decode JSON message")


        # 총 가격 업데이트
        self.update_total_price()
        self.update_order_total_price()
        
    def update_total_price(self):
        """모든 테이블의 총 가격을 계산하고 업데이트"""
        total_price = 0
        for orders in self.table_data.values():
            for order in orders:
                total_price += order['price']
        self.total_price_label.setText(f"Total price: {total_price}원")

    def update_order_total_price(self):
        """현재 주문의 총 가격을 계산하고 업데이트"""
        total_price = 0
        for row in range(self.order_table.rowCount()):
            price_item = self.order_table.item(row, 4)
            if price_item is not None:
                try:
                    price = int(price_item.text())
                    total_price += price
                except ValueError:
                    pass  # 숫자로 변환할 수 없는 경우 무시
        self.order_total_price_label.setText(f"Total price: {total_price}원")
        
    def handle_accept(self):
        """'Accept' 버튼 클릭 시 주문을 접수하고 화면을 업데이트"""
        if self.order_table.rowCount() == 0:
            return

        # 테이블 번호 가져오기
        table_id = int(self.order_table.item(0, 1).text())

        # 주문 데이터를 테이블 데이터에 합산
        for row in range(self.order_table.rowCount()):
            order_number = int(self.order_table.item(row, 0).text())
            menu = self.order_table.item(row, 2).text()
            quantity = int(self.order_table.item(row, 3).text())
            price = int(self.order_table.item(row, 4).text())

            # 기존에 동일한 메뉴가 있는지 확인
            menu_found = False
            for existing_order in self.table_data[table_id]:
                if existing_order['item'] == menu:
                    # 수량과 가격을 업데이트
                    existing_order['quantity'] += quantity
                    existing_order['price'] += price
                    menu_found = True
                    break

            if not menu_found:
                # 새로운 메뉴 추가 (order_number 포함)
                self.table_data[table_id].append({
                    'order_number': order_number,
                    'item': menu,
                    'quantity': quantity,
                    'price': price,
                    'checked': False,
                    'disabled': False
                })

        # 버튼 텍스트 업데이트
        if 1 <= table_id <= len(self.table_buttons):
            button = self.table_buttons[table_id - 1]
            button.setText(
                f"Table {table_id}\n" +
                "\n".join([
                    f"{order['item']} {order['quantity']}개 {order['price']}원"
                    for order in self.table_data[table_id]
                ])
            )

        # 주문 상세 정보 테이블 초기화
        self.order_table.setRowCount(0)

        # 데이터베이스에 주문 저장
        db.insert_order_with_items(table_id, self.table_data[table_id])

        # 대기 주문 처리 (생략된 부분은 기존 코드 유지)

        # 총 가격 업데이트
        self.update_total_price()
        self.update_order_total_price()

        # 주문 결과를 서비스로 전송
        response_message = f"Order Accepted for Table {table_id}"
        self.send_order_result(response_message)

    def handle_cancel(self):
        """'Cancel' 버튼 클릭 시 현재 주문을 취소하고 화면을 업데이트"""
        if self.order_table.rowCount() == 0:
            return

        # 테이블 번호 가져오기
        table_id = int(self.order_table.item(0, 1).text())

        # "Specific order information"에서 주문 정보를 삭제
        self.order_table.setRowCount(0)

        ################ 데이터베이스에서 해당 주문 삭제 #####################
        '''
        self.cursor.execute(
            "DELETE FROM orders WHERE table_id = ? AND status = 'processing'",
            (table_id,)
        )
        self.conn.commit()
        '''

        # 대기 주문 정보에서 다음 주문 가져오기
        if self.cumulative_table.rowCount() > 0:
            next_order_numbers = []
            first_order_number = self.cumulative_table.item(0, 0).text()

            # 다음 주문 번호와 동일한 주문 모두 가져오기
            for row in range(self.cumulative_table.rowCount()):
                order_number = self.cumulative_table.item(row, 0).text()
                if order_number == first_order_number:
                    next_order_numbers.append(row)

            for row in next_order_numbers:
                row_count = self.order_table.rowCount()
                self.order_table.insertRow(row_count)
                for col in range(self.cumulative_table.columnCount()):
                    item = self.cumulative_table.item(row, col)
                    if item:
                        self.order_table.setItem(row_count, col, QTableWidgetItem(item.text()))

            ####################### 데이터베이스에서 대기 주문 삭제 #############################
            '''
            self.cursor.execute(
                "DELETE FROM waiting_orders WHERE wait_number = ?",
                (first_wait_number,)
            )
            self.conn.commit()
            '''

            # 대기 주문에서 해당 주문 삭제
            for row in reversed(next_order_numbers):
                self.cumulative_table.removeRow(row)


        # 주문 가격 총합 업데이트
        self.update_order_total_price()

        # 서비스 요청 전송
        response_message = f"Order Canceled for Table {table_id}"
        self.send_order_result(response_message)

    def parse_order(self, order_text):
        """주문 문자열을 파싱하여 메뉴명, 수량, 가격을 반환"""
        # 예: "햄버거 3개 15000원" -> ("햄버거", 3, 15000)
        parts = order_text.split()
        menu = parts[0]
        quantity = int(parts[1].replace("개", ""))
        price = int(parts[2].replace("원", ""))
        return menu, quantity, price

    def send_order_result(self, message):
        """주문 결과 메시지를 ROS 노드로 전송"""
        self.subscriber_node.send_order_result(message)

    def open_control_popup(self):
        """테이블 버튼 클릭 시 팝업 창을 여는 함수"""
        button = self.sender()
        if button:
            text = button.text()
            # 정규표현식을 사용하여 'Table ' 다음에 오는 숫자를 추출
            match = re.match(r'Table (\d+)', text)
            if match:
                table_id = int(match.group(1))
                # 해당 테이블의 주문 데이터를 가져옵니다.
                orders = self.table_data.get(table_id, [])
                # ControlPopup 창 열기, 주문 데이터 전달
                self.control_popup = ControlPopup(self.subscriber_node, table_id, orders)
                self.control_popup.exec_()
            else:
                print("Failed to extract table_id from button text.")

    def move_robot_to_waiting_position(self):
        # 서빙 로봇을 대기 위치로 이동시키는 기능을 구현
        print("서빙 로봇을 대기 위치로 이동합니다.")
        QMessageBox.information(self, "서빙 로봇 제어", "서빙 로봇을 대기 위치로 이동합니다.")
        # ROS 메시지 퍼블리시 또는 서비스 호출을 통해 로봇을 제어할 수 있습니다.

    def move_robot_to_kitchen_position(self):
        # 서빙 로봇을 주방 위치로 이동시키는 기능을 구현
        print("서빙 로봇을 주방 위치로 이동합니다.")
        QMessageBox.information(self, "서빙 로봇 제어", "서빙 로봇을 주방 위치로 이동합니다.")
        # ROS 메시지 퍼블리시 또는 서비스 호출을 통해 로봇을 제어할 수 있습니다.

    def start_robot(self):
        # 서빙 로봇을 출발시키는 기능을 구현
        print("서빙 로봇을 출발합니다.")
        QMessageBox.information(self, "서빙 로봇 제어", "서빙 로봇을 출발합니다.")
        # ROS 메시지 퍼블리시 또는 서비스 호출을 통해 로봇을 제어할 수 있습니다.

    def show_statistics(self):
        # 통계 팝업 창을 표시하는 기능을 구현
        print("통계 팝업 창을 표시합니다.")

        # 새로운 창으로 'RestaurantApp' 띄우기
        self.statistics_window = RestaurantApp()  # QWidget 기반의 창을 띄움
        self.statistics_window.show()  # show()를 사용하면 새로운 창으로 표시됨

    '''
    def closeEvent(self, event):
        """창이 닫힐 때 데이터베이스 연결 종료"""
        self.conn.close()
        event.accept()
    '''

def ros_spin(node):
    """ROS 노드를 별도의 스레드에서 실행하는 함수"""
    rclpy.spin(node)
    rclpy.shutdown()

def main():
    """프로그램의 메인 함수"""
    rclpy.init()  # ROS2 초기화
    subscriber_node = KitchenSubscriber()  # ROS 노드 생성

    app = QApplication(sys.argv)  # QApplication 객체 생성

    window = KitchenMonitoring(subscriber_node)  # GUI 창 생성
    window.show()  # 창 표시

    # ROS2 노드를 별도의 스레드에서 실행
    ros_thread = threading.Thread(target=ros_spin, args=(subscriber_node,), daemon=True)
    ros_thread.start()

    sys.exit(app.exec_())  # GUI 이벤트 루프 실행

if __name__ == "__main__":
    main()
