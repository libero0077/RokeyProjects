import sys
import sqlite3
import threading
import queue
from datetime import datetime
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String

from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, 
                             QWidget, QScrollArea, QLabel, QGridLayout, QSpinBox, QHeaderView, 
                             QMessageBox, QTableWidget, QDialog, QTableWidgetItem, QLineEdit)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, Qt
from rclpy.qos import QoSProfile, ReliabilityPolicy  # QoS 설정
import json

# 전역 데이터베이스 연결
conn = None

def initialize_database():
    global conn
    try:
        conn = sqlite3.connect('restaurant.db')
        cursor = conn.cursor()
        
        cursor.execute("DROP TABLE IF EXISTS menu")
        
        cursor.execute('''CREATE TABLE menu
                         (id INTEGER PRIMARY KEY,
                          name TEXT,
                          price REAL,
                          availability INTEGER,
                          category TEXT,
                          description TEXT,
                          image_path TEXT)''')
        
        sample_data = [
        ('김치찌개', 12000, 1, '메인메뉴', '국내산 김치를 사용하여 매콤하게 끓였습니다.\n맵기 강도 조절 가능', ""),
        ('된장찌개', 11000, 1, '메인메뉴', '두부, 호박, 돼지고기을 넣어 더욱 식감을 살렸습니다.', ""),
        ('열무비빔밥', 10000, 1, '메인메뉴', '싱싱한 열무와 다른 채소들을 사용하였습니다.', ""),
        ('두루치기', 12000, 1, '메인메뉴', '국내산 김치와 생고기를 사용하여 더욱 맛있습니다', ""),
        ('콜라', 2000, 1, '음료', '코카콜라 또는 펩시로 선택가능합니다', ""),
        ('콜라제로', 2000, 1, '음료', '코카콜라제로 또는 펩시제로로 선택가능합니다', ""),
        ('사이다', 2000, 1, '음료', '칠성사이다 또는 스프라이트로 선택가능합니다', ""),
        ('사이다제로1', 2000, 1, '음료', '칠성사이다 제로 또는 스프라이트 제로로 선택가능합니다', ""),
        ('사이다제로2', 2000, 1, '음료', '칠성사이다 제로 또는 스프라이트 제로로 선택가능합니다', ""),
        ('사이다제로3', 2000, 1, '음료', '칠성사이다 제로 또는 스프라이트 제로로 선택가능합니다', "")
        ]
        
        cursor.executemany("INSERT INTO menu (name, price, availability, category, description, image_path) VALUES (?, ?, ?, ?, ?, ?)", sample_data)
        conn.commit()
    except sqlite3.Error as e:
        print(f"데이터베이스 오류: {e}")
    except Exception as e:
        print(f"예외 발생: {e}")

class MenuDatabase:
    def __init__(self):
        global conn
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.load_menu()

    def load_menu(self):
        try:
            self.cursor.execute('SELECT id, name, price, category, description, image_path FROM menu WHERE availability=1')
            self.menu_items = self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"메뉴 로딩 오류: {e}")

    def get_menu(self):
        return self.menu_items

class NODE(Node):
    def __init__(self):
        super().__init__('node')
        qos_profile = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
        self.message_publisher = self.create_publisher(String, 'order_topic', qos_profile)

        self.queue = queue.Queue()
        self.timer = self.create_timer(0.1, self.publish_message)
        

        ######################## 주문 처리 관련 수정 코드 ############################################
        '''
        테이블 오더 노드는 기존에 주문을 퍼블리시하는 기능 외에도 order_response_topic을 구독하여 
        주방 디스플레이 노드로부터 "Accept" 또는 "Cancel" 메시지를 수신하고 이를 "알림내역"에 표시해야 한다
        따라서 테이블 오더가 "주문 처리"에 대한 서브스크라이버가 된다.
        '''
        # 새로운 서브스크라이버 추가
        self.response_subscriber = self.create_subscription(String,'order_response_topic', self.response_callback, qos_profile)
        self.notification_queue = queue.Queue()  # 알림 메시지 큐
        
    # 콜백함수
    def response_callback(self, msg):
        """주방 디스플레이 노드로부터의 응답 메시지를 처리"""
        self.get_logger().info(f"Received response: {msg.data}")
        self.notification_queue.put(msg.data)  # 알림 큐에 추가
    #############################################################################################


    def publish_message(self):
        while not self.queue.empty():
            message = self.queue.get()
            msg = String()
            msg.data = message
            self.message_publisher.publish(msg)
            self.get_logger().info(f'Published message: {message}')

class MenuItemWidget(QWidget):
    def __init__(self, menu_item, parent=None):
        super().__init__(parent)
        self.menu_item = menu_item
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(5)  # 위젯 간 간격 설정
        
        # 이미지 레이블
        image_label = QLabel()
        pixmap = QPixmap(self.menu_item[5])
        scaled_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # 크기 고정
        image_label.setFixedSize(150, 150)  # 레이블 크기 고정
        image_label.setAlignment(Qt.AlignCenter)  # 중앙 정렬
        image_label.setPixmap(scaled_pixmap)
        layout.addWidget(image_label)

        name_label = QLabel(self.menu_item[1])
        layout.addWidget(name_label)

        price_label = QLabel(f"{int(self.menu_item[2])}원")
        layout.addWidget(price_label)

        select_button = QPushButton("선택")
        select_button.clicked.connect(self.show_popup)
        layout.addWidget(select_button)

        self.setLayout(layout)
        self.setFixedSize(170, 260)  # 위젯 전체 크기 고정

    def show_popup(self):
        popup = MenuItemPopup(self.menu_item, self)
        if popup.exec_() == QDialog.Accepted:
            # GUI 인스턴스를 찾아 add_to_order 메서드 호출
            main_window = self.window()
            if isinstance(main_window, GUI):
                main_window.add_to_order(self.menu_item, popup.quantity_spin.value())

class MenuItemPopup(QDialog):
    def __init__(self, menu_item, parent=None):
        super().__init__(parent)
        self.order_history = []
        self.menu_item = menu_item
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("메뉴 상세")
        layout = QHBoxLayout()
        
        # 이미지 레이블
        image_label = QLabel()
        pixmap = QPixmap(self.menu_item[5])
        scaled_pixmap = pixmap.scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # 크기 고정
        image_label.setFixedSize(250, 250)  # 레이블 크기 고정
        image_label.setAlignment(Qt.AlignCenter)  # 중앙 정렬
        image_label.setPixmap(scaled_pixmap)
        layout.addWidget(image_label)
            
        # 우측 정보 레이아웃
        info_layout = QVBoxLayout()
        
        # 메뉴명
        name_label = QLabel(self.menu_item[1])
        name_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        info_layout.addWidget(name_label)
        
        # 메뉴 설명
        description_label = QLabel(self.menu_item[4])
        description_label.setStyleSheet("font-size: 14px;")
        info_layout.addWidget(description_label)
        
        # 수량 조절 레이아웃
        quantity_layout = QHBoxLayout()
        quantity_layout.addWidget(QLabel("수량"))
        
        # 감소 버튼
        minus_button = QPushButton("-")
        minus_button.setFixedSize(30, 30)
        minus_button.setStyleSheet("""
            QPushButton {
                background-color: #FF4444;
                color: white;
                border-radius: 15px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF6666;
            }
        """)
        minus_button.clicked.connect(self.decrease_quantity)
        quantity_layout.addWidget(minus_button)
        
        # 수량 표시 (SpinBox 대신 QLabel 사용)
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setButtonSymbols(QSpinBox.NoButtons)  # 증가/감소 버튼 제거
        self.quantity_spin.setMinimum(1)
        self.quantity_spin.setFixedWidth(50)
        self.quantity_spin.setAlignment(Qt.AlignCenter)
        self.quantity_spin.setStyleSheet("""
            QSpinBox {
                font-size: 14px;
                padding: 5px;
                border: none;
                background-color: transparent;
            }
        """)
        quantity_layout.addWidget(self.quantity_spin)
        
        # 증가 버튼
        plus_button = QPushButton("+")
        plus_button.setFixedSize(30, 30)
        plus_button.setStyleSheet("""
            QPushButton {
                background-color: #FF4444;
                color: white;
                border-radius: 15px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF6666;
            }
        """)
        plus_button.clicked.connect(self.increase_quantity)
        quantity_layout.addWidget(plus_button)
        
        info_layout.addLayout(quantity_layout)
        
        # 선택 버튼
        select_button = QPushButton("장바구니에 담기")
        select_button.setFixedHeight(40)
        select_button.setStyleSheet("""
            QPushButton {
                background-color: #FF4444;
                color: white;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF6666;
            }
        """)
        select_button.clicked.connect(self.accept)
        info_layout.addWidget(select_button)
        
        layout.addLayout(info_layout)
        self.setLayout(layout)

    def decrease_quantity(self):
        current = self.quantity_spin.value()
        if current > 1:
            self.quantity_spin.setValue(current - 1)

    def increase_quantity(self):
        self.quantity_spin.setValue(self.quantity_spin.value() + 1)



class GUI(QMainWindow):
    def __init__(self, node):
        super().__init__()
        self.node = node
        self.menu_db = MenuDatabase()
        self.order_items = []
        self.order_history = []
        self.current_category = '전체 메뉴'  # 현재 선택된 카테고리 저장
        ########주문 처리 관련 알림 내역 저장을 위한 리스트#####
        self.notifications = []  # 알림 내역 저장 리스트
        ###############################################
        self.setupUi()

        ########################### 알림 메시지 확인을 위한 타이머 설정 ###################
        self.notification_timer = QTimer(self) 
        self.notification_timer.timeout.connect(self.check_notifications)
        self.notification_timer.start(1000)  # 1초마다 확인
        ############################################################################


    def setupUi(self):
        self.setWindowTitle("테이블 오더")
        self.setGeometry(100, 100, 1200, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # 상단 레이아웃
        top_layout = QHBoxLayout()
        self.table_label = QLabel("테이블 번호: 1")
        self.table_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        top_layout.addWidget(self.table_label)
        top_layout.addStretch(1)
        self.time_label = QLabel()
        self.time_label.setStyleSheet("font-size: 14px;")
        top_layout.addWidget(self.time_label)
        main_layout.addLayout(top_layout)
        
        # 중앙 컨텐츠 영역
        content_layout = QHBoxLayout()
        
        # 좌측 카테고리 메뉴
        category_layout = QVBoxLayout()
        category_widget = QWidget()
        category_widget.setMinimumWidth(150)
        
        # 검색바 추가
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("메뉴 검색...")
        self.search_bar.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        self.search_bar.textChanged.connect(self.filter_menu)  # 실시간 검색을 위한 시그널 연결
        category_layout.addWidget(self.search_bar)

        categories = ['전체메뉴', '인기메뉴', '메인메뉴', '음료']
        for category in categories:
            btn = QPushButton(category)
            btn.setMinimumHeight(40)
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding-left: 20px;
                    border: none;
                    background-color: #f0f0f0;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
            """)
            # 버튼 클릭 시 카테고리 필터링 함수 연결
            btn.clicked.connect(lambda checked, cat=category: self.filter_by_category(cat))
            category_layout.addWidget(btn)

        category_layout.addStretch()
        category_widget.setLayout(category_layout)
        content_layout.addWidget(category_widget)
        
        # 중앙 메뉴 표시 영역
        menu_scroll = QScrollArea()
        menu_scroll.setWidgetResizable(True)
        self.menu_display = QWidget()
        self.menu_layout = QGridLayout(self.menu_display)
        self.menu_layout.setSpacing(20)

        # 메뉴 위젯 저장을 위한 리스트
        self.menu_widgets = []

        # 메뉴 위젯 생성 및 배치
        menu_items = self.menu_db.get_menu()
        for i, menu_item in enumerate(menu_items):
            menu_widget = MenuItemWidget(menu_item, self.menu_display)
            self.menu_widgets.append(menu_widget)
            self.menu_layout.addWidget(menu_widget, i // 3, i % 3)

        menu_scroll.setWidget(self.menu_display)
        content_layout.addWidget(menu_scroll, 2)
        
        
        # 우측 주문 목록
        order_layout = QVBoxLayout()
        order_widget = QWidget()
        order_widget.setMinimumWidth(350)

        header_label = QLabel("장바구니")
        header_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        order_layout.addWidget(header_label)
        
        self.order_list = QTableWidget()
        self.order_list.setColumnCount(3)
        self.order_list.setHorizontalHeaderLabels(['메뉴명', '수량', '가격'])
        self.order_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.order_list.verticalHeader().setVisible(False)  # 행 번호 숨기기
        order_layout.addWidget(self.order_list)
        
        self.total_label = QLabel("총계: 0원")
        self.total_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        order_layout.addWidget(self.total_label)
        
        order_button = QPushButton("주문하기")
        order_button.setMinimumHeight(100)
        order_button.setStyleSheet("""
            QPushButton {
                background-color: #FF4444;
                color: white;
                font-size: 14px;
                border-radius: 5px;
            }
        """)
        order_button.clicked.connect(self.place_order)
        order_layout.addWidget(order_button)
        
        order_widget.setLayout(order_layout)
        content_layout.addWidget(order_widget)
        
        main_layout.addLayout(content_layout)
        
        # 하단 버튼 레이아웃 수정
        bottom_layout = QHBoxLayout()
        
        # 알림내역 버튼 추가 (좌측에 배치)
        notification_button = QPushButton("알림내역")
        notification_button.clicked.connect(self.show_notification)
        bottom_layout.addWidget(notification_button)
        
        # 중간 공백 추가
        bottom_layout.addStretch(1)
        
        # 기존 버튼들 우측에 배치
        order_history_button = QPushButton("주문 내역")
        order_history_button.clicked.connect(self.show_order_history)
        bottom_layout.addWidget(order_history_button)
        
        call_staff_button = QPushButton("직원 호출")
        call_staff_button.clicked.connect(self.call_staff)
        bottom_layout.addWidget(call_staff_button)
        main_layout.addLayout(bottom_layout)

        
        # 타이머 설정
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
    
    # 검색어에 맞는 메뉴 필터링
    def filter_menu(self, text):
        search_text = text.lower()

        # 모든 메뉴 위젯을 숨기기
        for widget in self.menu_widgets:
            widget.hide()

        # 검색어에 맞는 메뉴만 표시
        visible_widgets = []
        for widget in self.menu_widgets:
            menu_name = widget.menu_item[1].lower()
            first_char_chosung = self.get_jamo(menu_name[0]).lower()
            if search_text in menu_name or search_text == first_char_chosung:
                visible_widgets.append(widget)

        # 보이는 위젯들을 그리드에 다시 배치
        for i, widget in enumerate(visible_widgets):
            widget.show()
            row = i // 3  # 3열 그리드 가정
            col = i % 3
            self.menu_layout.addWidget(widget, row, col)

        # 남은 셀을 빈 위젯으로 채우기
        for i in range(len(visible_widgets), len(self.menu_widgets)):
            empty_widget = QWidget()
            row = i // 3
            col = i % 3
            self.menu_layout.addWidget(empty_widget, row, col)
                

                
    # 초성 관련 함수
    def get_jamo(self, char):
        CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
        HANGUL_START = 0xAC00
        HANGUL_END = 0xD7A3
        
        if not char:
            return ''
            
        code = ord(char)
        if code < HANGUL_START or code > HANGUL_END:
            return char
            
        chosung_index = (code - HANGUL_START) // (21 * 28)
        return CHOSUNG_LIST[chosung_index]
        
    
    # 카테고리 작동 구현
    def filter_by_category(self, category):
        # 기존 메뉴 위젯 모두 제거
        for i in reversed(range(self.menu_layout.count())):
            widget = self.menu_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # 선택된 카테고리에 해당하는 메뉴 표시
        menu_items = self.menu_db.get_menu()
        filtered_items = []
        if category == '전체메뉴':
            filtered_items = menu_items
        elif category == '메뉴검색':
            filtered_items = menu_items 
        else:
            filtered_items = [item for item in menu_items if item[3] == category]

        # 필터링된 메뉴 위젯 추가
        for i, menu_item in enumerate(filtered_items):
            menu_widget = MenuItemWidget(menu_item, self.menu_display)
            self.menu_layout.addWidget(menu_widget, i // 3, i % 3)

    def update_time(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.setText(f"현재 시간: {current_time}")

    def add_to_order(self, menu_item, quantity):
        item = next((x for x in self.order_items if x['id'] == menu_item[0]), None)
        if item:
            item['quantity'] += quantity
        else:
            self.order_items.append({
                'id': menu_item[0],
                'name': menu_item[1],
                'price': menu_item[2],
                'quantity': quantity
            })
        self.update_order_list()
    
    ########################### 주문 처리 관련 알림 큐에서 메시지 가져오기 ################
    def check_notifications(self):
        """알림 큐에서 메시지를 가져와 알림 리스트에 추가"""
        while not self.node.notification_queue.empty():
            notification = self.node.notification_queue.get()
            self.notifications.append(notification)
    ###############################################################################

    # 알림내역
    def show_notification(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("알림 내역")
        dialog.setGeometry(100, 100, 300, 200)
        
        layout = QVBoxLayout()

        #################################3 알림 목록을 보여줄 테이블 ###########################
        notification_table = QTableWidget()
        notification_table.setRowCount(len(self.notifications))
        notification_table.setColumnCount(1)
        notification_table.setHorizontalHeaderLabels(['알림 내용'])
        notification_table.verticalHeader().setVisible(False)
        notification_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        for i, notification in enumerate(self.notifications):
            item = QTableWidgetItem(notification)
            item.setTextAlignment(Qt.AlignCenter)
            notification_table.setItem(i, 0, item)
        
        layout.addWidget(notification_table)
        
        dialog.setLayout(layout)
        dialog.exec_()
    ###########################################################################################
    
    
    # 장바구니
    def update_order_list(self):
        self.order_list.setRowCount(0)
        total = 0
        
        for i, item in enumerate(self.order_items):
            self.order_list.insertRow(i)
            price = item['price'] * item['quantity']
            
            #  각 열에 아이템 추가 및 가운데 정렬
            menu_item = QTableWidgetItem(item['name'])
            menu_item.setTextAlignment(Qt.AlignCenter)
            self.order_list.setItem(i, 0, menu_item)
            
            quantity_item = QTableWidgetItem(str(item['quantity']))
            quantity_item.setTextAlignment(Qt.AlignCenter)
            self.order_list.setItem(i, 1, quantity_item)
            
            price_item = QTableWidgetItem(f"{int(price)}원")
            price_item.setTextAlignment(Qt.AlignCenter)
            self.order_list.setItem(i, 2, price_item)
            
            total += price
            
            self.total_label.setText(f"합계: {int(total)}원")

    ##############################################################################
    def place_order(self):
        if not self.order_items:
            QMessageBox.warning(self, "주문 오류", "주문 목록이 비어있습니다.")
            return

        # JSON 메시지 구조 생성
        order_message = {
            "table_id": 1,  # 테이블 번호
            "orders": [
                {"item": item["name"], "quantity": item["quantity"], "price": int(item["price"] * item["quantity"])}
                for item in self.order_items
            ]
        }

        # 버튼을 클릭했을 때 주문 내역에 추가
        self.order_history.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": self.order_items.copy()
        })

        # ROS 퍼블리셔로 메시지 전송
        self.node.queue.put(json.dumps(order_message))  # JSON 형식으로 직렬화
        QMessageBox.information(self, "주문 완료", "주문이 완료되었습니다.")
        self.order_items.clear()
        self.update_order_list()
    ##################################################################################
        
    def show_order_history(self):
        # if not hasattr(self, 'order_history'):
        #     self.order_history = []
            
        dialog = QDialog(self)
        dialog.setWindowTitle("주문 내역")
        dialog.setGeometry(100, 100, 600, 400)
        
        layout = QVBoxLayout()
        
        # QTableWidget으로 변경
        order_list = QTableWidget()
        order_list.setColumnCount(3)
        order_list.setHorizontalHeaderLabels(['메뉴명', '수량', '가격'])
        order_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        order_list.verticalHeader().setVisible(False) # 행 번호 숨기기
        
        # 주문 내역 합계 계산
        total_items = {}
        grand_total = 0
        
        for order in self.order_history:
            for item in order['items']:
                if item['name'] in total_items:
                    total_items[item['name']]['quantity'] += item['quantity']
                    total_items[item['name']]['total'] += item['price'] * item['quantity']
                else:
                    total_items[item['name']] = {
                        'quantity': item['quantity'],
                        'total': item['price'] * item['quantity']
                    }
                grand_total += item['price'] * item['quantity']
        
        # 주문 내역 표시
        order_list.setRowCount(len(total_items))
        
        for i, (name, info) in enumerate(total_items.items()):
            # 각 열에 아이템 추가 및 가운데 정렬
            name_item = QTableWidgetItem(name)
            name_item.setTextAlignment(Qt.AlignCenter)
            order_list.setItem(i, 0, name_item)
        
            quantity_item = QTableWidgetItem(str(info['quantity']))
            quantity_item.setTextAlignment(Qt.AlignCenter)
            order_list.setItem(i, 1, quantity_item)
        
            price_item = QTableWidgetItem(f"{int(info['total'])}원")
            price_item.setTextAlignment(Qt.AlignCenter)
            order_list.setItem(i, 2, price_item)
    
        layout.addWidget(order_list)
        
        # 합계를 별도의 라벨로 표시
        total_label = QLabel(f"총 합계: {int(grand_total)}원")
        total_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(total_label)
        
        dialog.setLayout(layout)
        dialog.exec_()
        
        
    def call_staff(self):
        self.node.queue.put("직원 호출")
        QMessageBox.information(self, "직원 호출", "직원을 호출했습니다.")

def main():
    try:
        initialize_database()
        rclpy.init()
        node = NODE()
        ros_thread = threading.Thread(target=lambda : rclpy.spin(node), daemon=True)
        ros_thread.start()

        app = QApplication(sys.argv)
        gui = GUI(node)
        gui.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"프로그램 실행 중 오류 발생: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    main()