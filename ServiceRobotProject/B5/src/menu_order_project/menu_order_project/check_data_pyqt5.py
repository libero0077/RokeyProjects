import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
                             QLabel, QCalendarWidget, QDialog, QTabWidget, QGridLayout, QComboBox)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime, timedelta
import calendar

# 데이터베이스 연결
def db_connection():
    return sqlite3.connect('restaurant_db.db')

# 데이터를 가져오는 함수
def fetch_data_from_table(table_name):
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        return cursor.fetchall()

# 평균 배송 시간 계산
def calculate_average_delivery_time():
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT AVG(julianday(end_time) - julianday(start_time)) * 24 * 60 AS average_delivery_time
        FROM deliver_log
        WHERE end_time IS NOT NULL AND start_time IS NOT NULL
        ''')
        result = cursor.fetchone()
        return round(result[0], 2) if result[0] else 0

# 총 판매량 기준 TOP 3 메뉴
def get_top_3_sales_volume():
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT menu.name, SUM(order_items.quantity) AS total_quantity
        FROM menu
        JOIN order_items ON menu.menu_item_id = order_items.menu_item_id
        GROUP BY menu.menu_item_id
        ORDER BY total_quantity DESC
        LIMIT 3
        ''')
        return cursor.fetchall()

# 총 매출액 기준 TOP 3 메뉴
def get_top_3_sales_amount():
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT menu.name, SUM(order_items.quantity * menu.price) AS total_sales
        FROM menu
        JOIN order_items ON menu.menu_item_id = order_items.menu_item_id
        GROUP BY menu.menu_item_id
        ORDER BY total_sales DESC
        LIMIT 3
        ''')
        return cursor.fetchall()

# 특정 날짜에 대한 메뉴별 판매액 계산 함수
# 지정된 날짜를 기준으로 각 메뉴에 대해 판매된 총 금액을 계산합니다.
def calculate_daily_sales_volume(date):
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT menu.name, SUM(order_items.quantity * menu.price)
        FROM menu
        JOIN order_items ON menu.menu_item_id = order_items.menu_item_id
        JOIN orders ON orders.order_id = order_items.order_id
        WHERE orders.order_time LIKE ?
        GROUP BY menu.menu_item_id
        ''', (f'{date}%',))
        return cursor.fetchall()

# 특정 날짜에 대한 메뉴별 판매량 계산 함수
# 지정된 날짜를 기준으로 각 메뉴에 대해 판매된 총 수량을 계산합니다.
def calculate_menu_sales_volume(date):
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT menu.name, SUM(order_items.quantity)
        FROM menu
        JOIN order_items ON menu.menu_item_id = order_items.menu_item_id
        JOIN orders ON orders.order_id = order_items.order_id
        WHERE orders.order_time LIKE ?
        GROUP BY menu.menu_item_id
        ''', (f'{date}%',))
        return cursor.fetchall()

# 특정 날짜 범위의 일별 매출 계산 함수
# 시작 날짜와 종료 날짜 사이의 일별 매출 총액을 계산합니다.
def calculate_daily_sales_range(start_date, end_date):
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT DATE(order_time), SUM(total_amount)
        FROM orders
        WHERE DATE(order_time) BETWEEN ? AND ?
        GROUP BY DATE(order_time)
        ''', (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
        results = cursor.fetchall()
        sales = {row[0]: row[1] for row in results}
        return sales

# 특정 날짜 범위의 일별 판매량 계산 함수
# 시작 날짜와 종료 날짜 사이의 일별 판매량을 계산합니다.
def calculate_daily_sales_volume_range(start_date, end_date):
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT DATE(order_time), SUM(order_items.quantity)
        FROM order_items
        JOIN orders ON order_items.order_id = orders.order_id
        WHERE DATE(order_time) BETWEEN ? AND ?
        GROUP BY DATE(order_time)
        ''', (start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
        results = cursor.fetchall()
        volumes = {row[0]: row[1] for row in results}
        return volumes

class RestaurantApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Restaurant Data")
        self.setGeometry(100, 100, 1600, 900)
        self.selected_date = datetime.now().strftime('%Y-%m-%d')  # 현재 날짜로 초기화
        
        # 그래프 타입 설정 변수 추가
        self.daily_sales_chart_type = 'bar'  # 'bar' 또는 'line'
        self.menu_sales_chart_type = 'bar'  # 'bar' 또는 'pie'
        
        # 스타일 시트 적용
        self.setStyleSheet("""
            QWidget {
                font-family: Arial;
                font-size: 12pt;
            }
            QTabWidget::pane { /* The tab widget frame */
                border-top: 2px solid #C2C7CB;
            }
            QTabBar::tab {
                background: #E0E0E0;
                border: 1px solid #C4C4C3;
                padding: 10px;
            }
            QTabBar::tab:selected {
                background: #F0F0F0;
                margin-bottom: -1px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        # 테이블 위젯 딕셔너리 초기화
        self.table_widgets = {}

        # 메인 레이아웃 생성
        main_layout = QVBoxLayout()

        # 탭 위젯 생성
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # 테이블 탭 추가
        self.table_tab = QWidget()
        self.create_table_tab()
        self.tabs.addTab(self.table_tab, "Data Tables")

        # 그래프 탭 추가
        self.graph_tab = QWidget()
        self.create_graph_tab()
        self.tabs.addTab(self.graph_tab, "Statistics")

        self.setLayout(main_layout)

        # 초기 데이터 로드 및 그래프 표시
        self.display_all_tables()
        today = datetime.now()
        self.plot_daily_graphs(today.month, today.year)
        self.update_sales_labels()
        self.update_summary_info()

    def create_table_tab(self):
        layout = QVBoxLayout()

        # 각 테이블을 표시할 탭 위젯 생성
        self.table_tabs = QTabWidget()
        layout.addWidget(self.table_tabs)

        # 각 테이블별로 탭 생성
        for table_name in ["tables", "menu", "orders", "order_items", "deliver_log"]:
            table_widget = QTableWidget()
            self.table_widgets[table_name] = table_widget
            tab = QWidget()
            tab_layout = QVBoxLayout()
            tab_layout.addWidget(table_widget)
            tab.setLayout(tab_layout)
            self.table_tabs.addTab(tab, table_name.capitalize())

        self.table_tab.setLayout(layout)

    def create_graph_tab(self):
        layout = QHBoxLayout()  # 가로 레이아웃으로 변경해서 그래프와 요약 정보 레이아웃을 나란히 배치

        # 그래프 타입 선택 및 날짜 선택 레이아웃
        graph_type_layout = QVBoxLayout()

        date_info_layout = QHBoxLayout()
        self.date_label = QLabel("Date: ", self)
        self.sales_label = QLabel("Today's Sales: ", self)
        self.monthly_sales_label = QLabel("Monthly Sales: ", self)
        self.select_date_button = QPushButton("Select Date", self)
        self.select_date_button.clicked.connect(self.open_calendar_popup)

        date_info_layout.addWidget(self.date_label)
        date_info_layout.addWidget(self.sales_label)
        date_info_layout.addWidget(self.monthly_sales_label)
        date_info_layout.addWidget(self.select_date_button)

        graph_type_layout.addLayout(date_info_layout)

        self.daily_sales_combo = QComboBox()
        self.daily_sales_combo.addItems(["Bar Chart", "Line Chart"])
        self.daily_sales_combo.currentIndexChanged.connect(self.update_daily_sales_and_volume_chart_type)

        self.menu_sales_combo = QComboBox()
        self.menu_sales_combo.addItems(["Bar Chart", "Pie Chart"])
        self.menu_sales_combo.currentIndexChanged.connect(self.update_menu_sales_and_volume_chart_type)

        graph_type_select_layout = QHBoxLayout()
        graph_type_select_layout.addWidget(QLabel("Daily Sales & Volume Graph Type:"))
        graph_type_select_layout.addWidget(self.daily_sales_combo)
        graph_type_select_layout.addWidget(QLabel("Menu Sales & Volume Graph Type:"))
        graph_type_select_layout.addWidget(self.menu_sales_combo)

        graph_type_layout.addLayout(graph_type_select_layout)

        # 그래프 레이아웃
        graph_layout = QGridLayout()
        self.canvas1 = FigureCanvas(Figure(figsize=(5, 4)))
        self.canvas2 = FigureCanvas(Figure(figsize=(5, 4)))
        self.canvas3 = FigureCanvas(Figure(figsize=(5, 4)))
        self.canvas4 = FigureCanvas(Figure(figsize=(5, 4)))

        graph_layout.addWidget(self.canvas1, 0, 0)
        graph_layout.addWidget(self.canvas2, 0, 1)
        graph_layout.addWidget(self.canvas3, 1, 0)
        graph_layout.addWidget(self.canvas4, 1, 1)

        graph_type_layout.addLayout(graph_layout)

        # 요약 정보 레이아웃 - 그래프 오른쪽에 배치
        summary_layout = QVBoxLayout()
        summary_widget = QWidget()
        summary_widget.setFixedWidth(300)  # 고정된 너비로 설정 (너무 커지지 않도록)
        summary_widget.setLayout(summary_layout)

        self.avg_delivery_label = QLabel("Average Delivery Time: ", self)
        self.top3_sales_volume_label = QLabel("Top 3 Sales Volume: ", self)
        self.top3_sales_amount_label = QLabel("Top 3 Sales Amount: ", self)

        # 글자 크기를 키워 더 잘 보이도록 설정
        summary_layout.setSpacing(20)  # 섹션 간 간격 추가
        self.avg_delivery_label.setStyleSheet("font-size: 16pt;")
        self.top3_sales_volume_label.setStyleSheet("font-size: 16pt;")
        self.top3_sales_amount_label.setStyleSheet("font-size: 16pt;")

        summary_layout.addWidget(self.avg_delivery_label)
        summary_layout.addWidget(self.top3_sales_volume_label)
        summary_layout.addWidget(self.top3_sales_amount_label)

        # 전체 레이아웃에 추가
        layout.addLayout(graph_type_layout, stretch=3)  # 그래프가 3배 비율을 차지하도록 설정
        layout.addWidget(summary_widget, stretch=1)  # 요약 정보가 1배 비율을 차지하도록 설정

        self.graph_tab.setLayout(layout)

    # 그래프 타입을 변경했을 때 호출되는 함수들 (일별 판매 & 판매량)
    def update_daily_sales_and_volume_chart_type(self):
        selected_type = self.daily_sales_combo.currentText()
        if selected_type == "Bar Chart":
            self.daily_sales_chart_type = 'bar'
        elif selected_type == "Line Chart":
            self.daily_sales_chart_type = 'line'
        # 두 그래프가 함께 변경되도록 업데이트
        self.update_graphs()

    # 그래프 타입을 변경했을 때 호출되는 함수들 (메뉴별 판매 & 판매량)
    def update_menu_sales_and_volume_chart_type(self):
        selected_type = self.menu_sales_combo.currentText()
        if selected_type == "Bar Chart":
            self.menu_sales_chart_type = 'bar'
        elif selected_type == "Pie Chart":
            self.menu_sales_chart_type = 'pie'
        # 두 그래프가 함께 변경되도록 업데이트
        self.update_graphs()

    # 그래프 업데이트를 위한 함수
    def update_graphs(self):
        year, month, _ = map(int, self.selected_date.split('-'))
        self.plot_daily_graphs(month, year)

    def update_summary_info(self):
        # 평균 배송 시간 업데이트
        avg_delivery_time = calculate_average_delivery_time()
        avg_delivery_text = f"Average\nDelivery Time: {avg_delivery_time:.2f} mins"
        self.avg_delivery_label.setText(avg_delivery_text)

        # 총 판매량 TOP 3 메뉴 업데이트
        top_3_volume = get_top_3_sales_volume()
        volume_lines = [f"{item[0]} ({item[1]:,})" for item in top_3_volume]  # 천 단위 콤마 추가
        volume_text = "Top 3 Sales Volume:\n" + "\n".join(volume_lines)
        self.top3_sales_volume_label.setText(volume_text)
        self.top3_sales_volume_label.setWordWrap(True)

        # 총 매출액 TOP 3 메뉴 업데이트
        top_3_sales = get_top_3_sales_amount()
        sales_lines = [f"{item[0]} ({item[1]:,} won)" for item in top_3_sales]  # 천 단위 콤마 추가
        sales_text = "Top 3 Sales Amount:\n" + "\n".join(sales_lines)
        self.top3_sales_amount_label.setText(sales_text)
        self.top3_sales_amount_label.setWordWrap(True)

    # 캘린더 팝업을 열어 날짜를 선택하게 하는 함수
    def open_calendar_popup(self):
        calendar_dialog = QDialog(self)
        calendar_dialog.setWindowTitle("Select a Date")

        calendar_widget = QCalendarWidget(calendar_dialog)
        calendar_widget.clicked.connect(self.on_date_selected_from_popup)

        dialog_layout = QVBoxLayout(calendar_dialog)
        dialog_layout.addWidget(calendar_widget)
        calendar_dialog.setLayout(dialog_layout)

        calendar_dialog.exec_()

    # 선택된 날짜를 기준으로 그래프 및 레이블을 업데이트하는 함수
    def on_date_selected_from_popup(self, date):
        self.selected_date = date.toString('yyyy-MM-dd')
        self.clear_graphs()
        year, month, _ = map(int, self.selected_date.split('-'))
        self.plot_daily_graphs(month, year)
        self.update_sales_labels()

    # 매출 라벨을 업데이트하는 함수
    def update_sales_labels(self):
        target_date = self.selected_date or datetime.now().strftime('%Y-%m-%d')
        year, month, _ = map(int, target_date.split('-'))

        start_date = datetime(year, month, 1)
        end_date = (start_date.replace(day=calendar.monthrange(year, month)[1]))

        monthly_sales = calculate_daily_sales_range(start_date, end_date)
        today_sales_data = calculate_daily_sales_volume(target_date)

        today_sales = sum(item[1] for item in today_sales_data)
        total_monthly_sales = sum(monthly_sales.values())

        today_sales_formatted = '{:,}'.format(today_sales)
        total_monthly_sales_formatted = '{:,}'.format(total_monthly_sales)

        self.date_label.setText(f"Date: {target_date}")
        self.sales_label.setText(f"Selected Day's Sales: {today_sales_formatted} KRW")
        self.monthly_sales_label.setText(f"Monthly Sales: {total_monthly_sales_formatted} KRW")

    # 그래프 그리기 함수
    def plot_daily_graphs(self, month, year):
        start_date = datetime(year, month, 1)
        end_date = (start_date.replace(month=month % 12 + 1, day=1) - timedelta(days=1)) if month < 12 else start_date.replace(day=31)

        daily_sales = calculate_daily_sales_range(start_date, end_date)
        daily_sales = {date: amount / 10000 for date, amount in daily_sales.items()}

        daily_sales_volume = calculate_daily_sales_volume_range(start_date, end_date)
        today_sales_volume = calculate_daily_sales_volume(self.selected_date or datetime.now().strftime('%Y-%m-%d'))
        today_menu_sales_volume = calculate_menu_sales_volume(self.selected_date or datetime.now().strftime('%Y-%m-%d'))

        # 그래프 캔버스를 새로 설정하여 이전 데이터를 모두 삭제
        self.canvas1.figure.clf()
        self.canvas2.figure.clf()
        self.canvas3.figure.clf()
        self.canvas4.figure.clf()

        # 일별 매출 그래프 그리기
        date_list = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end_date - start_date).days + 1)]
        bar_colors = ['blue' if date == self.selected_date else 'red' for date in date_list]  # 오늘 날짜만 파란색으로 표시
        ax1 = self.canvas1.figure.add_subplot(111)
        ax1.clear()
        sales_values = [daily_sales.get(date, 0) for date in date_list]
        if self.daily_sales_chart_type == 'bar':
            ax1.bar(date_list, sales_values, color=bar_colors)
        elif self.daily_sales_chart_type == 'line':
            ax1.plot(date_list, sales_values, color='blue', marker='o')
            ax1.scatter([date for date in date_list if date == self.selected_date], [daily_sales.get(self.selected_date, 0)], color='red')

        ax1.set_ylabel('Sales (10,000won)')
        ax1.set_title('Daily Sales')
        ax1.set_xticks(date_list[::3])
        ax1.tick_params(axis='x', rotation=45)
        self.canvas1.draw()

        # 일별 판매량 그래프 그리기
        ax2 = self.canvas2.figure.add_subplot(111)
        ax2.clear()
        volume_values = [daily_sales_volume.get(date, 0) for date in date_list]
        bar_colors_volume = ['green' if date == self.selected_date else 'purple' for date in date_list]

        if self.daily_sales_chart_type == 'bar':
            ax2.bar(date_list, volume_values, color=bar_colors_volume)
        elif self.daily_sales_chart_type == 'line':
            ax2.plot(date_list, volume_values, color='green', marker='o')
            ax2.scatter([date for date in date_list if date == self.selected_date], [daily_sales_volume.get(self.selected_date, 0)], color='red')

        ax2.set_ylabel('Volume')
        ax2.set_title('Daily Sales Volume')
        ax2.set_xticks(date_list[::3])
        ax2.tick_params(axis='x', rotation=45)
        self.canvas2.draw()

        # 메뉴별 매출 그래프 그리기
        ax3 = self.canvas3.figure.add_subplot(111)
        ax3.clear()

        menu_list = [item[0] for item in today_sales_volume]
        sales_values = [item[1] / 10000 for item in today_sales_volume]

        if self.menu_sales_chart_type == 'bar':
            ax3.bar(menu_list, sales_values, color='turquoise')
            ax3.set_ylabel('Sales (10,000won)')
            ax3.set_title('Menu-wise Sales')
        elif self.menu_sales_chart_type == 'pie':
            ax3.pie(sales_values, labels=menu_list, autopct='%1.1f%%', startangle=140)
            ax3.set_title('Menu-wise Sales Distribution')

        self.canvas3.draw()

        # 메뉴별 판매량 그래프 그리기
        ax4 = self.canvas4.figure.add_subplot(111)
        ax4.clear()

        menu_volume_list = [item[0] for item in today_menu_sales_volume]
        volume_values = [item[1] for item in today_menu_sales_volume]

        if self.menu_sales_chart_type == 'bar':
            ax4.bar(menu_volume_list, volume_values, color='lightgreen')
            ax4.set_ylabel('Volume')
            ax4.set_title('Menu-wise Sales Volume')
        elif self.menu_sales_chart_type == 'pie':
            ax4.pie(volume_values, labels=menu_volume_list, autopct='%1.1f%%', startangle=140)
            ax4.set_title('Menu-wise Sales Volume Distribution')

        self.canvas4.draw()

    # 그래프를 모두 초기화하는 함수
    def clear_graphs(self):
        self.canvas1.figure.clear()
        self.canvas2.figure.clear()
        self.canvas3.figure.clear()
        self.canvas4.figure.clear()
        self.canvas1.draw()
        self.canvas2.draw()
        self.canvas3.draw()
        self.canvas4.draw()

    # 모든 테이블을 표시하는 함수
    def display_all_tables(self):
        self.display_table("tables", ["table_id", "x", "y"])
        self.display_table("menu", ["menu_item_id", "name", "price", "image"])
        self.display_table("orders", ["order_id", "table_id", "order_time", "total_amount"])
        self.display_table("order_items", ["order_item_id", "order_id", "menu_item_id", "quantity", "status"])
        self.display_table("deliver_log", ["deliver_id", "order_id", "start_time", "end_time"])

    # 특정 테이블을 표시하는 함수
    def display_table(self, table_name, headers):
        rows = fetch_data_from_table(table_name)
        table_widget = self.table_widgets.get(table_name)

        if not rows:
            table_widget.setRowCount(0)
            table_widget.setColumnCount(0)
            table_widget.setHorizontalHeaderLabels(["No Data Available"])
            return

        table_widget.setRowCount(len(rows))
        table_widget.setColumnCount(len(headers))
        table_widget.setHorizontalHeaderLabels(headers)

        for row_idx, row in enumerate(rows):
            for col_idx, item in enumerate(row):
                table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(item)))

# 실행 코드
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RestaurantApp()
    window.show()
    sys.exit(app.exec_())