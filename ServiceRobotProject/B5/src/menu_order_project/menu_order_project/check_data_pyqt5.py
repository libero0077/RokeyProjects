import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
                             QLabel, QCalendarWidget, QDialog, QTabWidget, QGridLayout)
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

# 메뉴별 판매액 계산 (날짜 인자 추가)
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

# 메뉴별 판매량 계산 (날짜 인자 추가)
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

# 특정 날짜 범위의 일별 매출 계산
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

# 특정 날짜 범위의 일별 판매량 계산
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
        layout = QVBoxLayout()

        # 날짜 선택 및 정보 레이아웃
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

        layout.addLayout(date_info_layout)

        # 그래프 레이아웃
        graph_layout = QGridLayout()
        
        # 그래프 유형 선택 콤보 박스
        self.graph_types = ["Bar", "Line", "Pie"]

        # 첫 번째 그래프: 일별 매출
        self.canvas1 = FigureCanvas(Figure(figsize=(5, 4)))
        graph_layout.addWidget(self.canvas1, 0, 0)

        # 두 번째 그래프: 일별 판매량
        self.canvas2 = FigureCanvas(Figure(figsize=(5, 4)))
        graph_layout.addWidget(self.canvas2, 0, 1)

        # 세 번째 그래프: 메뉴별 매출
        self.canvas3 = FigureCanvas(Figure(figsize=(5, 4)))
        graph_layout.addWidget(self.canvas3, 1, 0)

        # 네 번째 그래프: 메뉴별 판매량
        self.canvas4 = FigureCanvas(Figure(figsize=(5, 4)))
        graph_layout.addWidget(self.canvas4, 1, 1)

        layout.addLayout(graph_layout)

        self.graph_tab.setLayout(layout)

    def open_calendar_popup(self):
        # Create a dialog to show the calendar
        calendar_dialog = QDialog(self)
        calendar_dialog.setWindowTitle("Select a Date")

        # Create and set up the calendar widget
        calendar_widget = QCalendarWidget(calendar_dialog)
        calendar_widget.clicked.connect(self.on_date_selected_from_popup)

        # Set up layout for the dialog
        dialog_layout = QVBoxLayout(calendar_dialog)
        dialog_layout.addWidget(calendar_widget)
        calendar_dialog.setLayout(dialog_layout)

        # Show the dialog
        calendar_dialog.exec_()

    def on_date_selected_from_popup(self, date):
        # Set the selected date from the calendar
        self.selected_date = date.toString('yyyy-MM-dd')

        # Update the display and graphs
        self.clear_graphs()
        year, month, _ = map(int, self.selected_date.split('-'))
        self.plot_daily_graphs(month, year)

        # Update sales labels based on selected date
        self.update_sales_labels()

    def update_sales_labels(self):
        # 선택된 날짜가 있으면 그 날짜로, 없으면 오늘 날짜로 설정
        target_date = self.selected_date or datetime.now().strftime('%Y-%m-%d')
        year, month, _ = map(int, target_date.split('-'))

        # 선택된 달의 시작일과 마지막 날짜 계산
        start_date = datetime(year, month, 1)
        end_date = (start_date.replace(day=calendar.monthrange(year, month)[1]))

        # 월간 판매 데이터와 선택된 날짜의 판매 데이터를 가져옴
        monthly_sales = calculate_daily_sales_range(start_date, end_date)
        today_sales_data = calculate_daily_sales_volume(target_date)

        # 오늘의 매출 및 월간 총 매출 계산
        today_sales = sum(item[1] for item in today_sales_data)
        total_monthly_sales = sum(monthly_sales.values())

        # 포맷팅하여 라벨에 표시
        today_sales_formatted = '{:,}'.format(today_sales)
        total_monthly_sales_formatted = '{:,}'.format(total_monthly_sales)

        # 레이블 업데이트
        self.date_label.setText(f"Date: {target_date}")
        self.sales_label.setText(f"Selected Day's Sales: {today_sales_formatted} KRW")
        self.monthly_sales_label.setText(f"Monthly Sales: {total_monthly_sales_formatted} KRW")

    def clear_table(self, table_widget):
        table_widget.setRowCount(0)

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

    def display_all_tables(self):
        # 각 테이블의 헤더 정보를 설정하여 데이터를 표시
        self.display_table("tables", ["table_id", "x", "y"])
        self.display_table("menu", ["menu_item_id", "name", "price", "image"])
        self.display_table("orders", ["order_id", "table_id", "order_time", "total_amount"])
        self.display_table("order_items", ["order_item_id", "order_id", "menu_item_id", "quantity", "status"])
        self.display_table("deliver_log", ["deliver_id", "order_id", "start_time", "end_time"])

    def plot_daily_graphs(self, month, year):
        start_date = datetime(year, month, 1)
        end_date = (start_date.replace(month=month % 12 + 1, day=1) - timedelta(days=1)) if month < 12 else start_date.replace(day=31)

        daily_sales = calculate_daily_sales_range(start_date, end_date)
        # Convert the daily sales dictionary values to be divided by 10000
        daily_sales = {date: amount / 10000 for date, amount in daily_sales.items()}

        daily_sales_volume = calculate_daily_sales_volume_range(start_date, end_date)
        today_sales_volume = calculate_daily_sales_volume(self.selected_date or datetime.now().strftime('%Y-%m-%d'))
        today_menu_sales_volume = calculate_menu_sales_volume(self.selected_date or datetime.now().strftime('%Y-%m-%d'))

        menu_list = [item[0] for item in today_sales_volume]
        sales_values = [item[1] / 10000 for item in today_sales_volume]

        # x축: 날짜 리스트 생성
        date_list = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d")
                     for i in range((end_date - start_date).days + 1)]

        # 색상 지정: 선택된 날짜는 파란색, 나머지는 빨간색
        bar_colors_sales = ['blue' if date == self.selected_date else 'red' for date in date_list]
        bar_colors_volume = ['blue' if date == self.selected_date else 'purple' for date in date_list]

        # First graph: Daily sales
        ax1 = self.canvas1.figure.add_subplot(111)
        ax1.clear()
        bars = ax1.bar(date_list, [daily_sales.get(date, 0) for date in date_list], color=bar_colors_sales)
        ax1.set_ylabel('Sales (만원)')
        ax1.set_title('Daily Sales')
        ax1.set_xticks(date_list[::3])
        ax1.tick_params(axis='x', rotation=45)

        # 데이터 라벨 추가
        for bar in bars:
            height = bar.get_height()
            ax1.annotate(f'{height:.1f}',
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3),
                         textcoords="offset points",
                         ha='center', va='bottom', fontsize=8)

        # 범례 추가
        ax1.legend(['Selected Date', 'Other Dates'])

        self.canvas1.draw()

        # Second graph: Daily sales volume
        ax2 = self.canvas2.figure.add_subplot(111)
        ax2.clear()
        bars2 = ax2.bar(date_list, [daily_sales_volume.get(date, 0) for date in date_list], color=bar_colors_volume)
        ax2.set_ylabel('Volume')
        ax2.set_title('Daily Sales Volume')
        ax2.set_xticks(date_list[::3])
        ax2.tick_params(axis='x', rotation=45)

        # 데이터 라벨 추가
        for bar in bars2:
            height = bar.get_height()
            ax2.annotate(f'{height:.0f}',
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3),
                         textcoords="offset points",
                         ha='center', va='bottom', fontsize=8)

        ax2.legend(['Selected Date', 'Other Dates'])

        self.canvas2.draw()

        # Third graph: Menu-wise sales
        ax3 = self.canvas3.figure.add_subplot(111)
        ax3.clear()
        bars3 = ax3.bar(menu_list, sales_values, color='turquoise')
        ax3.set_ylabel('Sales (만원)')
        ax3.set_title('Menu-wise Sales')
        ax3.tick_params(axis='x', rotation=45)

        for bar in bars3:
            height = bar.get_height()
            ax3.annotate(f'{height:.1f}',
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3),
                         textcoords="offset points",
                         ha='center', va='bottom', fontsize=8)

        self.canvas3.draw()

        # Fourth graph: Menu-wise sales volume
        ax4 = self.canvas4.figure.add_subplot(111)
        ax4.clear()
        bars4 = ax4.bar([item[0] for item in today_menu_sales_volume], [item[1] for item in today_menu_sales_volume], color='lightgreen')
        ax4.set_ylabel('Volume')
        ax4.set_title('Menu-wise Sales Volume')
        ax4.tick_params(axis='x', rotation=45)

        for bar in bars4:
            height = bar.get_height()
            ax4.annotate(f'{height:.0f}',
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3),
                         textcoords="offset points",
                         ha='center', va='bottom', fontsize=8)

        self.canvas4.draw()

    def clear_graphs(self):
        # 그래프 캔버스를 초기화
        self.canvas1.figure.clear()
        self.canvas2.figure.clear()
        self.canvas3.figure.clear()
        self.canvas4.figure.clear()

        # 캔버스를 새로 그리기
        self.canvas1.draw()
        self.canvas2.draw()
        self.canvas3.draw()
        self.canvas4.draw()

# 실행 코드
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RestaurantApp()
    window.show()
    sys.exit(app.exec_())