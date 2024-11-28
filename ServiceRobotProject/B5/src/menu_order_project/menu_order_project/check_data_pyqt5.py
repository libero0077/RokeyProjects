import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QCalendarWidget, QDialog
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
        ''', (start_date, end_date))
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
        ''', (start_date, end_date))
        results = cursor.fetchall()
        volumes = {row[0]: row[1] for row in results}
        return volumes

# 날짜 선택 시 월별 그래프 업데이트
def date_selected(self):
    selected_date = self.calendar.selectedDate().toString('yyyy-MM-dd')
    year, month, _ = map(int, selected_date.split('-'))
    self.plot_monthly_graphs(month, year)

class RestaurantApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Restaurant Data")
        self.setGeometry(100, 100, 1600, 900)
        self.selected_date = None
        
        # Main layout (horizontal layout for table and graph)
        main_layout = QHBoxLayout()

        # Table layout (vertical for multiple tables)
        left_layout = QVBoxLayout()

        # Create and add table widgets for different tables
        self.table_widgets = {
            "tables": QTableWidget(),
            "menu": QTableWidget(),
            "orders": QTableWidget(),
            "order_items": QTableWidget(),
            "deliver_log": QTableWidget()
        }

        # Add each table widget to the vertical layout
        for table_name, table_widget in self.table_widgets.items():
            left_layout.addWidget(table_widget)

        # Graph layout (for displaying graphs)
        right_layout = QVBoxLayout()

        # Create a layout for 2x2 graph grid
        graph_layout = QVBoxLayout()
        
        # Create a horizontal layout for two graphs in a row
        top_graph_layout = QHBoxLayout()

        # Create a button for selecting the date
        self.select_date_button = QPushButton("Select Date", self)
        self.select_date_button.clicked.connect(self.open_calendar_popup)

        # Labels to display today's date, sales, and monthly sales
        self.date_label = QLabel("Date: ", self)
        self.sales_label = QLabel("Today's Sales: ", self)
        self.monthly_sales_label = QLabel("Monthly Sales: ", self)
        
        # Create a layout to display the labels and the button horizontally
        date_info_layout = QHBoxLayout()
        date_info_layout.addWidget(self.date_label)
        date_info_layout.addWidget(self.sales_label)
        date_info_layout.addWidget(self.monthly_sales_label)
        date_info_layout.addWidget(self.select_date_button)

        right_layout.addLayout(date_info_layout)

        # First row: first two graphs
        self.canvas1 = FigureCanvas(Figure(figsize=(6, 4)))
        self.canvas2 = FigureCanvas(Figure(figsize=(6, 4)))
        top_graph_layout.addWidget(self.canvas1)
        top_graph_layout.addWidget(self.canvas2)
        
        # Second row: last two graphs
        bottom_graph_layout = QHBoxLayout()
        self.canvas3 = FigureCanvas(Figure(figsize=(6, 4)))
        self.canvas4 = FigureCanvas(Figure(figsize=(6, 4)))
        bottom_graph_layout.addWidget(self.canvas3)
        bottom_graph_layout.addWidget(self.canvas4)
        
        # Add the horizontal layouts to the main graph layout
        graph_layout.addLayout(top_graph_layout)
        graph_layout.addLayout(bottom_graph_layout)
        
        right_layout.addLayout(graph_layout)

        # Add table layout to the left and graph layout to the right
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)

        # Set the overall layout
        self.setLayout(main_layout)

        # Display tables and initialize graphs
        self.display_all_tables()
        today = datetime.now()
        self.plot_daily_graphs(today.month, today.year)

        # Initial update of the sales labels
        self.update_sales_labels()

    def update_sales_labels(self):
        # 선택된 날짜가 있으면 그 날짜로, 없으면 오늘 날짜로 설정
        target_date = self.selected_date or datetime.now().strftime('%Y-%m-%d')
        year, month, _ = map(int, target_date.split('-'))
        
        # 선택된 달의 시작일과 마지막 날짜 계산
        start_date = datetime(year, month, 1).strftime('%Y-%m-%d')
        end_date = (datetime(year, month, calendar.monthrange(year, month)[1])).strftime('%Y-%m-%d')

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
        self.display_table("menu", ["menu_item_id", "name", "price"])
        self.display_table("orders", ["order_id", "table_id", "order_time", "status", "total_amount"])
        self.display_table("order_items", ["order_item_id", "order_id", "menu_item_id", "quantity"])
        self.display_table("deliver_log", ["deliver_id", "order_id", "start_time", "end_time"])

    def plot_daily_graphs(self, month, year):
        start_date = datetime(year, month, 1)
        end_date = (start_date.replace(month=month % 12 + 1, day=1) - timedelta(days=1))

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
        ax1 = self.canvas1.figure.axes[0] if self.canvas1.figure.axes else self.canvas1.figure.add_subplot(111)
        ax1.clear()  # 이전 내용 지우기
        ax1.bar(date_list, [daily_sales.get(date, 0) for date in date_list], color=bar_colors_sales)
        ax1.set_ylabel('sales(KRW)')
        ax1.set_title('Daily Sales')
        ax1.set_xticks(date_list[::3])  # x축 레이블 조정
        ax1.tick_params(axis='x', rotation=45)
        self.canvas1.draw()  # 그래프 새로 그리기

        # Second graph: Daily sales volume
        ax2 = self.canvas2.figure.axes[0] if self.canvas2.figure.axes else self.canvas2.figure.add_subplot(111)
        ax2.clear()  # 이전 내용 지우기
        ax2.bar(date_list, [daily_sales_volume.get(date, 0) for date in date_list], color=bar_colors_volume)
        ax2.set_ylabel('volume')
        ax2.set_title('Daily Sales Volume')
        ax2.set_xticks(date_list[::3])  # x축 레이블 조정
        ax2.tick_params(axis='x', rotation=45)
        self.canvas2.draw()  # 그래프 새로 그리기

        # Third graph: Menu-wise sales
        ax3 = self.canvas3.figure.axes[0] if self.canvas3.figure.axes else self.canvas3.figure.add_subplot(111)
        ax3.clear()
        ax3.bar(menu_list, sales_values, color='turquoise')
        ax3.set_ylabel('sales(KRW)')
        ax3.set_title('Menu-wise Sales')
        ax3.tick_params(axis='x', rotation=45)
        self.canvas3.draw()

        # Fourth graph: Menu-wise sales volume
        ax4 = self.canvas4.figure.axes[0] if self.canvas4.figure.axes else self.canvas4.figure.add_subplot(111)
        ax4.clear()  # 이전 내용 지우기
        ax4.bar([item[0] for item in today_menu_sales_volume], [item[1] for item in today_menu_sales_volume], color='lightgreen')
        ax4.set_ylabel('volume')
        ax4.set_title('Menu-wise Sales Volume')
        ax4.tick_params(axis='x', rotation=45)
        self.canvas4.draw()  # 그래프 새로 그리기

    def on_date_selected(self):
        # 선택된 날짜 저장
        self.selected_date = self.calendar.selectedDate().toString('yyyy-MM-dd')

        # 그래프 초기화
        self.clear_graphs()  # 그래프 초기화 함수 호출

        # 그래프 업데이트
        year, month, _ = map(int, self.selected_date.split('-'))
        self.plot_daily_graphs(month, year)

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

    def setup_graph_layout(self):
        # 기존 레이아웃을 제거
        layout = self.layout()
        if layout.itemAt(1):  # 오른쪽 레이아웃이 존재하는지 확인
            layout.itemAt(1).widget().deleteLater()  # 오른쪽 레이아웃 위젯 삭제

        # 새로 그래프 레이아웃 만들기
        right_layout = QVBoxLayout()

        # 달력 위젯 추가
        right_layout.addWidget(self.calendar)

        # 새로 생성된 그래프들을 추가
        graph_layout = QVBoxLayout()
        graph_layout.addWidget(self.canvas1)
        graph_layout.addWidget(self.canvas2)
        graph_layout.addWidget(self.canvas3)
        graph_layout.addWidget(self.canvas4)

        right_layout.addLayout(graph_layout)

        # 기존 오른쪽 레이아웃을 새로 생성한 레이아웃으로 교체
        layout.addLayout(right_layout, 2)  # 여기서 2는 오른쪽 영역을 차지하게 함


# 실행 코드
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RestaurantApp()
    window.show()
    sys.exit(app.exec_())
