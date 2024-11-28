import sys
import threading
import json

# ROS2 관련 모듈 임포트
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy  # QoS 설정을 위해 필요
from std_msgs.msg import String  # ROS 메시지 타입

# PyQt5 관련 모듈 임포트
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QObject

########################### 서비스 인터페이스 임포트 #############################
from menu_order_interfaces.srv import MenuUpdate  # 주문 결과를 보내기 위한 서비스
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

        ########################## 주문 결과를 보내기 위한 서비스 클라이언트 생성 #############################
        self.cli = self.create_client(MenuUpdate, 'order_result_service')

        # 서비스가 준비될 때까지 대기
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for order_result_service...')

        # 서비스 요청 객체 생성
        self.req = MenuUpdate.Request()
        ###############################################################################################

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

        # 서빙 로봇 제어 버튼들을 담을 레이아웃 생성
        self.robot_control_layout = QHBoxLayout()

        # "서빙 로봇 대기 위치로" 버튼 생성
        self.robot_waiting_button = QPushButton("서빙 로봇 대기 위치로")
        self.robot_waiting_button.clicked.connect(self.move_robot_to_waiting_position)
        self.robot_control_layout.addWidget(self.robot_waiting_button)

        # "서빙 로봇 주방 위치로" 버튼 생성
        self.robot_kitchen_button = QPushButton("서빙 로봇 주방 위치로")
        self.robot_kitchen_button.clicked.connect(self.move_robot_to_kitchen_position)
        self.robot_control_layout.addWidget(self.robot_kitchen_button)

        # "서빙 로봇 출발" 버튼 생성
        self.robot_start_button = QPushButton("서빙 로봇 출발")
        self.robot_start_button.clicked.connect(self.start_robot)
        self.robot_control_layout.addWidget(self.robot_start_button)

        # 로봇 제어 버튼들을 오른쪽 패널에 추가
        self.right_layout.addLayout(self.robot_control_layout)

        right_widget = QWidget()
        right_widget.setLayout(self.right_layout)
        main_layout.addWidget(right_widget, 0, 1)

        '''
        ############################## 데이터베이스 연결 설정 ################################
        import sqlite3  # SQLite 데이터베이스를 사용하기 위한 모듈 임포트

        # 데이터베이스 연결 설정
        self.conn = sqlite3.connect('restaurant.db')
        self.cursor = self.conn.cursor()

        # 주문 및 대기 주문 테이블 생성 (존재하지 않을 경우)
        self.create_tables()
        ####################################################################################
        '''

    '''
    def create_tables(self):
        """주문 및 대기 주문 테이블 생성"""
        # orders 테이블 생성
        ############ 맨 앞,뒤 괄호에 주석을 추가해야함 ##############3
        self.cursor.execute(
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_id INTEGER,
                menu TEXT,
                quantity INTEGER,
                price INTEGER,
                status TEXT
            )
        )

        # waiting_orders 테이블 생성
        ############ 맨 앞,뒤 괄호에 주석을 추가해야함 ##############3
        self.cursor.execute(
            CREATE TABLE IF NOT EXISTS waiting_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                wait_number INTEGER,
                table_id INTEGER,
                menu TEXT,
                quantity INTEGER,
                price INTEGER
            )
        )

        self.conn.commit()
    '''

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
        self.order_table.setColumnCount(4)  # 열 개수는 4개
        self.order_table.setHorizontalHeaderLabels(["Table Number", "Menu", "Quantity", "Price"])  # 열 제목 설정
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

            # 현재 대기 번호 할당
            current_wait_number = self.order_counter

            if self.order_table.rowCount() == 0:
                # 현재 처리 중인 주문이 없으면 주문 상세 정보에 추가
                for order in orders:
                    row_count = self.order_table.rowCount()
                    self.order_table.insertRow(row_count)
                    self.order_table.setItem(row_count, 0, QTableWidgetItem(str(table_id)))
                    self.order_table.setItem(row_count, 1, QTableWidgetItem(order["item"]))
                    self.order_table.setItem(row_count, 2, QTableWidgetItem(str(order["quantity"])))
                    self.order_table.setItem(row_count, 3, QTableWidgetItem(str(order["price"])))

                # 데이터베이스에 주문 기록 저장
                '''
                self.save_order_to_database(table_id, orders)
                '''

                # 대기 번호 증가
                self.order_counter += 1
            else:
                # 현재 처리 중인 주문이 있으면 대기 주문 정보에 추가
                for order in orders:
                    row_count = self.cumulative_table.rowCount()
                    self.cumulative_table.insertRow(row_count)
                    self.cumulative_table.setItem(row_count, 0, QTableWidgetItem(str(current_wait_number)))
                    self.cumulative_table.setItem(row_count, 1, QTableWidgetItem(str(table_id)))
                    self.cumulative_table.setItem(row_count, 2, QTableWidgetItem(order["item"]))
                    self.cumulative_table.setItem(row_count, 3, QTableWidgetItem(str(order["quantity"])))
                    self.cumulative_table.setItem(row_count, 4, QTableWidgetItem(str(order["price"])))

                ################3 데이터베이스에 대기 주문 기록 저장 #########################
                '''
                self.save_waiting_order_to_database(current_wait_number, table_id, orders)
                '''

                # 대기 번호 증가
                self.order_counter += 1

            # 총 가격 업데이트
            self.update_total_price()
            self.update_order_total_price()

        except json.JSONDecodeError:
            # 메시지 파싱 실패 시 에러 로그 출력
            self.subscriber_node.get_logger().error("Failed to decode JSON message")

    '''
    def save_order_to_database(self, table_id, orders):
        """데이터베이스에 주문을 저장하는 함수"""
        for order in orders:
            menu = order["item"]
            quantity = order["quantity"]
            price = order["price"]

            # 데이터베이스에 INSERT 쿼리 실행
            self.cursor.execute(
                "INSERT INTO orders (table_id, menu, quantity, price, status) VALUES (?, ?, ?, ?, ?)",
                (table_id, menu, quantity, price, 'processing')
            )
        self.conn.commit()  # 변경 사항 저장

    def save_waiting_order_to_database(self, wait_number, table_id, orders):
        """데이터베이스에 대기 주문을 저장하는 함수"""
        for order in orders:
            menu = order["item"]
            quantity = order["quantity"]
            price = order["price"]

            # 데이터베이스에 INSERT 쿼리 실행
            self.cursor.execute(
                "INSERT INTO waiting_orders (wait_number, table_id, menu, quantity, price) VALUES (?, ?, ?, ?, ?)",
                (wait_number, table_id, menu, quantity, price)
            )
        self.conn.commit()  # 변경 사항 저장
    '''

    def update_total_price(self):
        """모든 테이블의 총 가격을 계산하고 업데이트"""
        total_price = 0
        for orders in self.table_data.values():
            for order in orders:
                _, _, price = self.parse_order(order)
                total_price += price
        self.total_price_label.setText(f"Total price: {total_price}원")

    def update_order_total_price(self):
        """현재 주문의 총 가격을 계산하고 업데이트"""
        total_price = 0
        for row in range(self.order_table.rowCount()):
            price = int(self.order_table.item(row, 3).text())
            total_price += price
        self.order_total_price_label.setText(f"Total price: {total_price}원")

    def handle_accept(self):
        """'Accept' 버튼 클릭 시 주문을 접수하고 화면을 업데이트"""
        if self.order_table.rowCount() == 0:
            return

        # 테이블 번호 가져오기
        table_id = int(self.order_table.item(0, 0).text())

        # 주문 데이터를 테이블 데이터에 합산
        for row in range(self.order_table.rowCount()):
            menu = self.order_table.item(row, 1).text()
            quantity = int(self.order_table.item(row, 2).text())
            price = int(self.order_table.item(row, 3).text())

            # 기존에 동일한 메뉴가 있는지 확인
            menu_found = False
            for i, existing_order in enumerate(self.table_data[table_id]):
                existing_menu, existing_quantity, existing_price = self.parse_order(existing_order)

                if existing_menu == menu:
                    # 수량과 가격을 업데이트
                    new_quantity = existing_quantity + quantity
                    new_price = existing_price + price
                    self.table_data[table_id][i] = f"{menu} {new_quantity}개 {new_price}원"
                    menu_found = True
                    break

            if not menu_found:
                # 새로운 메뉴 추가
                self.table_data[table_id].append(f"{menu} {quantity}개 {price}원")

        # 테이블 버튼 업데이트
        if 1 <= table_id <= len(self.table_buttons):
            button = self.table_buttons[table_id - 1]
            button.setText(f"Table {table_id}\n" + "\n".join(self.table_data[table_id]))

        # 주문 상세 정보 테이블 초기화
        self.order_table.setRowCount(0)

        ##################3 데이터베이스에서 해당 주문 상태 업데이트 (processing -> accepted) #####################
        '''
        self.cursor.execute(
            "UPDATE orders SET status = 'accepted' WHERE table_id = ? AND status = 'processing'",
            (table_id,)
        )
        self.conn.commit()
        '''

        # 대기 주문 정보에서 다음 주문을 가져와 주문 상세 정보에 표시
        if self.cumulative_table.rowCount() > 0:
            first_wait_number = self.cumulative_table.item(0, 0).text()

            rows_to_move = []
            for row in range(self.cumulative_table.rowCount()):
                if self.cumulative_table.item(row, 0).text() == first_wait_number:
                    rows_to_move.append(row)

            for row in rows_to_move:
                row_count = self.order_table.rowCount()
                self.order_table.insertRow(row_count)
                self.order_table.setItem(row_count, 0, QTableWidgetItem(self.cumulative_table.item(row, 1).text()))
                self.order_table.setItem(row_count, 1, QTableWidgetItem(self.cumulative_table.item(row, 2).text()))
                self.order_table.setItem(row_count, 2, QTableWidgetItem(self.cumulative_table.item(row, 3).text()))
                self.order_table.setItem(row_count, 3, QTableWidgetItem(self.cumulative_table.item(row, 4).text()))

            ######################33 데이터베이스에서 대기 주문 삭제 및 주문으로 이동 #######################
            '''
            self.cursor.execute(
                "DELETE FROM waiting_orders WHERE wait_number = ?",
                (first_wait_number,)
            )
            self.conn.commit()
            '''

            # 대기 주문 정보에서 해당 행 삭제
            for row in reversed(rows_to_move):
                self.cumulative_table.removeRow(row)

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
        table_id = int(self.order_table.item(0, 0).text())

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
            first_wait_number = self.cumulative_table.item(0, 0).text()

            rows_to_move = []
            for row in range(self.cumulative_table.rowCount()):
                if self.cumulative_table.item(row, 0).text() == first_wait_number:
                    rows_to_move.append(row)

            for row in rows_to_move:
                row_count = self.order_table.rowCount()
                self.order_table.insertRow(row_count)
                self.order_table.setItem(row_count, 0, QTableWidgetItem(self.cumulative_table.item(row, 1).text()))
                self.order_table.setItem(row_count, 1, QTableWidgetItem(self.cumulative_table.item(row, 2).text()))
                self.order_table.setItem(row_count, 2, QTableWidgetItem(self.cumulative_table.item(row, 3).text()))
                self.order_table.setItem(row_count, 3, QTableWidgetItem(self.cumulative_table.item(row, 4).text()))

            ####################### 데이터베이스에서 대기 주문 삭제 #############################
            '''
            self.cursor.execute(
                "DELETE FROM waiting_orders WHERE wait_number = ?",
                (first_wait_number,)
            )
            self.conn.commit()
            '''

            # 대기 주문 정보에서 해당 행 삭제
            for row in reversed(rows_to_move):
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
        QMessageBox.information(self, "Statistics", "통계 팝업 창을 표시합니다.")
        # 실제 통계 데이터를 표시하는 창을 구현할 수 있습니다.

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
