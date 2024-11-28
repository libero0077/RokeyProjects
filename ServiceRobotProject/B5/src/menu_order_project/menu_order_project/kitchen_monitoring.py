import sys
import rclpy
from rclpy.node import Node
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGridLayout, QLabel, QPushButton,
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from std_msgs.msg import String
import json
from rclpy.qos import QoSProfile, ReliabilityPolicy  # QoS 설정
from PyQt5.QtWidgets import QHeaderView


# 1. ROS 메시지를 받는 역할을 하는 클래스
class KitchenSubscriber(Node, QThread):
    # GUI로 데이터를 보내기 위해 "Signal"을 사용
    order_received = pyqtSignal(str)

    def __init__(self):
        QThread.__init__(self)  # 백그라운드에서 실행될 스레드 초기화
        Node.__init__(self, 'kitchen_subscriber')  # ROS 노드 이름 설정

        # 메시지 전달 품질(QoS)을 설정 (신뢰성 보장)
        qos_profile = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)

        ########## 퍼블리셔로부터 'order_topic'이라는 토픽을 받아 구독한다##############
        self.subscription = self.create_subscription(String, 'order_topic', self.order_callback, qos_profile)

    def order_callback(self, msg):
        """메시지를 받으면 실행되는 함수"""
        self.get_logger().info(f"Received order: {msg.data}")  # 터미널에 받은 메시지를 출력
        self.order_received.emit(msg.data)  # 받은 메시지를 GUI로 전달 (Signal 사용)

    def run(self):
        """ROS 이벤트를 백그라운드에서 실행"""
        rclpy.spin(self)  # 노드가 종료될 때까지 계속 실행


# 2. GUI(화면)를 관리하는 클래스
class KitchenMonitoring(QMainWindow):
    def __init__(self, subscriber_node):
        super().__init__()
        self.subscriber_node = subscriber_node  # ROS 구독자를 저장
        self.subscriber_node.order_received.connect(self.update_order_details)  # 메시지 수신 시 연결
        
        ####### 주문 상세 정보를 접수 했을때, 기존 테이블 상태가 리셋 되는 것을 방지하기 위하여 추가 #########
        self.table_data = {i + 1: [] for i in range(9)}  # 테이블 1~9번의 데이터를 저장
        #####################################################################################


        # 주문 대기 번호를 관리하기 위한 변수 초기화
        self.order_counter = 1
        ####################################
        
        ####################### 가격 총합 레이블 추가###########################################
        self.total_price_label = QLabel("Total price: 0원", alignment=Qt.AlignRight)
        self.order_total_price_label = QLabel("Total price: 0원", alignment=Qt.AlignRight)
        #####################################################################################

        # 창 제목과 크기 설정
        self.setWindowTitle("Kitchen Display")
        self.setGeometry(100, 100, 1120, 600)

        # 화면 전체를 구성할 레이아웃 설정
        main_widget = QWidget(self)           # 메인 화면 위젯 생성
        main_layout = QGridLayout()           # 메인 화면의 레이아웃 생성
        main_widget.setLayout(main_layout)    # 메인 위젯에 레이아웃 설정
        self.setCentralWidget(main_widget)    # 메인 화면을 중앙에 배치

        # 왼쪽: 테이블 상태 표시
        self.table_status_widget = self.create_table_status_panel()
        main_layout.addWidget(self.table_status_widget, 0, 0)

        # 오른쪽: 주문 상세 정보 및 대기 주문 정보
        self.right_layout = QVBoxLayout()  # 오른쪽 레이아웃 추가
        self.order_detail_widget = self.create_order_detail_panel()
        self.cumulative_order_widget = self.create_cumulative_order_panel()

        self.right_layout.addWidget(self.order_detail_widget)  # 상단: 주문 상세 정보
        self.right_layout.addWidget(self.cumulative_order_widget)  # 하단: 대기 주문 정보

        right_widget = QWidget()
        right_widget.setLayout(self.right_layout)
        main_layout.addWidget(right_widget, 0, 1)  # 오른쪽 섹션 추가

    """왼쪽: 테이블 상태를 보여주는 부분"""
    def create_table_status_panel(self):
        layout = QVBoxLayout()  # 세로로 배치
        table_status_label = QLabel("Table Status", alignment=Qt.AlignCenter)
        table_status_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(table_status_label)

        # 3x3 테이블 상태 버튼 생성
        grid_layout = QGridLayout()
        self.table_buttons = []  # 테이블 버튼 리스트
        for i in range(9):  # 1번부터 9번까지 버튼 생성
            button = QPushButton(f"Table {i + 1}\n0")  # "테이블 번호 + 초기 상태"
            button.setFixedSize(180, 180)  # 버튼 크기 설정
            grid_layout.addWidget(button, i // 3, i % 3)  # 3x3 배열로 배치
            self.table_buttons.append(button)  # 버튼을 리스트에 저장
        layout.addLayout(grid_layout)

        # 가격 총합 레이블 추가
        layout.addWidget(self.total_price_label)

        widget = QWidget()  # 레이아웃을 위젯으로 감쌈
        widget.setLayout(layout)
        return widget

    """오른쪽: 주문 세부 정보를 보여주는 부분"""
    def create_order_detail_panel(self):
        layout = QVBoxLayout()
        order_detail_label = QLabel("Specific order information", alignment=Qt.AlignCenter)
        order_detail_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(order_detail_label)

        # 주문 세부 정보를 보여줄 테이블
        self.order_table = QTableWidget()
        self.order_table.setRowCount(0)  # 초기 행 개수 0
        self.order_table.setColumnCount(4)  # 열 개수 4개
        self.order_table.setHorizontalHeaderLabels(["Table Number", "Menu", "Quantity", "Price"])
        self.order_table.verticalHeader().setVisible(False)  # 왼쪽 행 번호 숨김
        
        ################## 열 크기 비율 설정
        header = self.order_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # 테이블 번호
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # 메뉴
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # 수량
        header.setSectionResizeMode(3, QHeaderView.Stretch)  # 가격
        ###################################################################

        layout.addWidget(self.order_table)

        # 주문 가격 총합 레이블 추가
        layout.addWidget(self.order_total_price_label)

        # 접수/취소 버튼 추가
        button_layout = QHBoxLayout()
        self.accept_button = QPushButton("Accept")
        self.cancel_button = QPushButton("Cancle")
        self.accept_button.clicked.connect(self.handle_accept)  # 접수 버튼 클릭 이벤트
        button_layout.addWidget(self.accept_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        widget = QWidget()  # 레이아웃을 위젯으로 감쌈
        widget.setLayout(layout)
        return widget

    """가격 총합 계산 및 업데이트"""
    def update_total_price(self):
        # 모든 테이블의 가격 총합 계산
        total_price = 0
        for table_id, orders in self.table_data.items():
            for order in orders:
                _, _, price = self.parse_order(order)  # 주문 데이터에서 가격만 추출
                total_price += price

        # 총합 레이블 업데이트
        self.total_price_label.setText(f"Total price: {total_price}")


    """주문 세부 정보의 가격 총합 계산 및 업데이트"""
    def update_order_total_price(self):
        # "주문 세부 정보"의 가격 총합 계산
        total_price = 0
        for row in range(self.order_table.rowCount()):
            price = int(self.order_table.item(row, 3).text())  # 가격 데이터 가져오기
            total_price += price

        # 총합 레이블 업데이트
        self.order_total_price_label.setText(f"Total price: {total_price}")
    
    """새로운 대기 주문 정보 패널 생성"""
    def create_cumulative_order_panel(self):
        layout = QVBoxLayout()
        cumulative_order_label = QLabel("Waiting order information", alignment=Qt.AlignCenter)
        cumulative_order_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(cumulative_order_label)

        # 대기 주문 정보를 보여줄 테이블
        self.cumulative_table = QTableWidget()
        self.cumulative_table.setRowCount(0)
        self.cumulative_table.setColumnCount(5)  # 대기 정보는 3열만 사용
        self.cumulative_table.setHorizontalHeaderLabels(["Order number","Table number", "Menu", "Quantity","Price"])
        self.cumulative_table.verticalHeader().setVisible(False)

        ###### 테이블 스타일 조정 ( 여백 공간 없이 테이블을 채우려는 목적)
        header = self.cumulative_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # 주문 번호
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # 테이블 번호
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # 메뉴
        header.setSectionResizeMode(3, QHeaderView.Stretch)  # 수량
        header.setSectionResizeMode(4, QHeaderView.Stretch)  # 가격
        #########################################################################################

        layout.addWidget(self.cumulative_table)

        widget = QWidget()
        widget.setLayout(layout)
        return widget

    """ROS Subscription으로부터 받은 메시지를 화면에 업데이트"""
    def update_order_details(self, message):
        try:
            # 메시지를 JSON 형식으로 변환
            data = json.loads(message)
            table_id = data["table_id"]  # 테이블 번호
            orders = data["orders"]  # 주문 목록

            # 새 메시지 단위로 대기 번호 할당
            current_wait_number = self.order_counter

            if self.order_table.rowCount() == 0:
                # "주문 세부 정보"가 비어 있으면, 새 주문을 여기에 추가
                for order in orders:
                    row_count = self.order_table.rowCount()
                    self.order_table.insertRow(row_count)
                    self.order_table.setItem(row_count, 0, QTableWidgetItem(str(table_id)))  # 테이블 번호
                    self.order_table.setItem(row_count, 1, QTableWidgetItem(order["item"]))  # 메뉴
                    self.order_table.setItem(row_count, 2, QTableWidgetItem(str(order["quantity"])))  # 수량
                    self.order_table.setItem(row_count, 3, QTableWidgetItem(str(order["price"])))  # 가격

                # "주문 세부 정보"에 데이터가 추가된 경우, 대기 번호 증가
                self.order_counter += 1
            else:
                # "주문 세부 정보"가 비어 있지 않으면, 새 주문을 "대기 주문 정보"에 추가
                for order in orders:
                    row_count = self.cumulative_table.rowCount()
                    self.cumulative_table.insertRow(row_count)
                    self.cumulative_table.setItem(row_count, 0, QTableWidgetItem(str(current_wait_number)))  # 동일 대기 번호
                    self.cumulative_table.setItem(row_count, 1, QTableWidgetItem(str(table_id)))  # 테이블 번호
                    self.cumulative_table.setItem(row_count, 2, QTableWidgetItem(order["item"]))  # 메뉴
                    self.cumulative_table.setItem(row_count, 3, QTableWidgetItem(str(order["quantity"])))  # 수량
                    self.cumulative_table.setItem(row_count, 4, QTableWidgetItem(str(order["price"])))  # 가격

                # 한 번의 메시지 처리 후, 대기 번호 증가
                self.order_counter += 1

            # 가격 총합 업데이트
            self.update_total_price()
            self.update_order_total_price()

        except json.JSONDecodeError:
            self.subscriber_node.get_logger().error("Failed to decode JSON message")

    """'접수' 버튼 클릭 시 테이블 상태를 업데이트"""
    def handle_accept(self):
        if self.order_table.rowCount() == 0:  # "주문 세부 정보"가 비어 있으면 종료
            return

        # 테이블 번호 가져오기
        table_id = int(self.order_table.item(0, 0).text())  # 모든 주문의 테이블 번호는 동일

        # 새 주문 데이터 합산 처리
        for row in range(self.order_table.rowCount()):
            menu = self.order_table.item(row, 1).text()  # 메뉴
            quantity = int(self.order_table.item(row, 2).text())  # 수량
            price = int(self.order_table.item(row, 3).text())  # 가격

            # 기존 테이블 데이터에서 동일 메뉴 검색
            menu_found = False
            for i, existing_order in enumerate(self.table_data[table_id]):
                existing_menu, existing_quantity, existing_price = self.parse_order(existing_order)

                if existing_menu == menu:  # 동일 메뉴 발견
                    # 수량과 가격을 합산
                    new_quantity = existing_quantity + quantity
                    new_price = existing_price + price
                    self.table_data[table_id][i] = f"{menu} {new_quantity}개 {new_price}원"
                    menu_found = True
                    break

            # 기존 메뉴에 없으면 새로 추가
            if not menu_found:
                self.table_data[table_id].append(f"{menu} {quantity}개 {price}원")

        # 테이블 버튼에 상태 업데이트
        if 1 <= table_id <= len(self.table_buttons):
            button = self.table_buttons[table_id - 1]
            button.setText(f"Table {table_id}\n" + "\n".join(self.table_data[table_id]))

        # "주문 세부 정보" 비우기
        self.order_table.setRowCount(0)

        # "대기 주문 정보"에서 가장 작은 대기 번호 가져오기
        if self.cumulative_table.rowCount() > 0:
            # 가장 작은 대기 번호를 가져옴
            first_wait_number = self.cumulative_table.item(0, 0).text()

            # 동일 대기 번호의 항목들을 모두 "주문 세부 정보"로 이동
            rows_to_move = []
            for row in range(self.cumulative_table.rowCount()):
                if self.cumulative_table.item(row, 0).text() == first_wait_number:
                    rows_to_move.append(row)

            # "주문 세부 정보"에 추가
            for row in rows_to_move:
                row_count = self.order_table.rowCount()
                self.order_table.insertRow(row_count)
                self.order_table.setItem(row_count, 0, QTableWidgetItem(self.cumulative_table.item(row, 1).text()))  # 테이블 번호
                self.order_table.setItem(row_count, 1, QTableWidgetItem(self.cumulative_table.item(row, 2).text()))  # 메뉴
                self.order_table.setItem(row_count, 2, QTableWidgetItem(self.cumulative_table.item(row, 3).text()))  # 수량
                self.order_table.setItem(row_count, 3, QTableWidgetItem(self.cumulative_table.item(row, 4).text()))  # 가격

            # "대기 주문 정보"에서 해당 행 제거 (뒤에서부터 제거해야 인덱스 꼬임 방지)
            for row in reversed(rows_to_move):
                self.cumulative_table.removeRow(row)

        # 가격 총합 업데이트
        self.update_total_price()
        self.update_order_total_price()

    """주문 데이터 파싱 함수"""
    def parse_order(self, order_text):
        """
        주어진 주문 텍스트를 파싱하여 메뉴, 수량, 가격을 추출합니다.
        예: "햄버거 3개 15000원" -> ("햄버거", 3, 15000)
        """
        parts = order_text.split()
        menu = parts[0]
        quantity = int(parts[1].replace("개", ""))
        price = int(parts[2].replace("원", ""))
        return menu, quantity, price


def main():
    """프로그램 실행"""
    rclpy.init()  # ROS2 초기화
    subscriber_node = KitchenSubscriber()
    subscriber_node.start()  # ROS 구독자 실행

    app = QApplication(sys.argv)

    window = KitchenMonitoring(subscriber_node)  # GUI 생성
    window.show()

    app.exec_()  # GUI 실행
    rclpy.shutdown()  # ROS2 종료


if __name__ == "__main__":
    main()