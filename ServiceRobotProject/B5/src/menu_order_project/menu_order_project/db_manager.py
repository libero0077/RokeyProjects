import sqlite3
from datetime import datetime, timedelta

# 공용 함수: 현재 타임스탬프 반환
def get_current_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 데이터베이스 연결 관리 함수
def db_connection():
    return sqlite3.connect('restaurant_db.db')

# 데이터베이스 초기화 함수
def create_db():
    with db_connection() as conn:
        cursor = conn.cursor()

        # 테이블 생성: 테이블 정보
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tables (
            table_id INTEGER PRIMARY KEY,
            x FLOAT NOT NULL,
            y FLOAT NOT NULL
        );
        ''')
        
        # 테이블 생성: 메뉴 정보
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu (
            menu_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100),
            price INTEGER,
            type_id INTEGER,
            category VARCHAR(50),
            description TEXT,
            image TEXT,
            sales_count INTEGER DEFAULT 0
        );
        ''')

        # 테이블 생성: 주문 정보
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_id INTEGER,
            order_time TIMESTAMP,
            total_amount INTEGER,
            FOREIGN KEY (table_id) REFERENCES tables(table_id)
        );
        ''')

        # 테이블 생성: 주문 상세 정보
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            menu_item_id INTEGER,
            quantity INTEGER,
            status VARCHAR(50),
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (menu_item_id) REFERENCES menu(menu_item_id)
        );
        ''')


        # 테이블 생성: 서빙 상세 정보
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS deliver_log (
            deliver_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_item_id INTEGER,
            start_time TIMESTAMP,
            end_time TIMESTAMP,
            FOREIGN KEY (order_item_id) REFERENCES order_items(order_item_id)
        );
        ''')

        conn.commit()

# 데이터 삽입 함수들
def insert_table(table_id, x, y):
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO tables (table_id, x, y)
        VALUES (?, ?, ?)
        ''', (table_id, x, y))
        conn.commit()

def insert_menu(name, price, type_id, category, description, image, sales_count):
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO menu (name, price, type_id, category, description, image, sales_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, price, type_id, category, description, image, sales_count))
        conn.commit()

def insert_order_with_items(table_id, items):
    """
    :param table_id: 주문이 발생한 테이블 ID
    :param items: 주문 항목의 리스트 (menu_item_id, quantity)
    :return: 생성된 order_id, order_item_ids
    """
    with db_connection() as conn:
        cursor = conn.cursor()
        total_amount = 0
        order_item_ids = []

        # 주문 추가
        order_time = get_current_timestamp()
        cursor.execute('''
        INSERT INTO orders (table_id, order_time, total_amount)
        VALUES (?, ?, ?)
        ''', (table_id, order_time, "Received"))

        order_id = cursor.lastrowid

        # 주문 아이템 추가 및 총액 계산
        for menu_item_id, quantity in items:
            status = "Received"
            cursor.execute('''
            INSERT INTO order_items (order_id, menu_item_id, quantity, status)
            VALUES (?, ?, ?, ?)
            ''', (order_id, menu_item_id, quantity, status))
            order_item_id = cursor.lastrowid
            order_item_ids.append(order_item_id)

            # 메뉴 가격 조회 및 총액 계산
            cursor.execute('SELECT price FROM menu WHERE menu_item_id = ?', (menu_item_id,))
            price = cursor.fetchone()[0]
            total_amount += price * quantity

            # 판매량 업데이트 (연결을 공유하여 업데이트)
            cursor.execute('''
            UPDATE menu
            SET sales_count = sales_count + ?
            WHERE menu_item_id = ?
            ''', (quantity, menu_item_id))

        # 총액 업데이트
        cursor.execute('''
        UPDATE orders
        SET total_amount = ?
        WHERE order_id = ?
        ''', (total_amount, order_id))

        conn.commit()
        return order_id, order_item_ids

    
def insert_delivery_log(order_item_id, end=False):
    """
    배달 시작 및 종료 시 delivery_log와 order_items 상태 업데이트
    :param order_item_id: 배달과 연결된 주문 아이템 ID
    :param end: True이면 배달 완료, False이면 배달 시작
    """
    with db_connection() as conn:
        cursor = conn.cursor()
        if end:
            try:
                end_time = get_current_timestamp()
                
                # SELECT 쿼리
                print(f"Checking if end_time is already set for order_item_id: {order_item_id}")
                cursor.execute('''
                SELECT end_time FROM deliver_log WHERE order_item_id = ? AND end_time IS NULL
                ''', (order_item_id,))
                result = cursor.fetchone()
                print(f"Query result: {result}")
                
                # end_time이 이미 설정된 경우
                if result and result[0] is not None:  
                    print(f"Order item {order_item_id} already marked as delivered.")
                    return
                
                # UPDATE deliver_log
                print("Executing UPDATE deliver_log query")
                cursor.execute('''
                UPDATE deliver_log
                SET end_time = ?
                WHERE order_item_id = ? AND end_time IS NULL
                ''', (end_time, order_item_id))

                # UPDATE order_items
                print("Executing UPDATE order_items query")
                cursor.execute('''
                UPDATE order_items
                SET status = "Delivered"
                WHERE order_item_id = ?
                ''', (order_item_id,))

            except sqlite3.Error as e:
                print(f"SQLite error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

        else:
            # 배달 시작
            start_time = get_current_timestamp()
            cursor.execute('''
            INSERT INTO deliver_log (order_item_id, start_time)
            VALUES (?, ?)
            ''', (order_item_id, start_time))
            cursor.execute('''
            UPDATE order_items
            SET status = "Delivering"
            WHERE order_item_id = ?
            ''', (order_item_id,))
        conn.commit()

def update_sales_count(menu_item_id, quantity):
    """
    주어진 menu_item_id의 판매량(sales_count)을 업데이트합니다.
    :param menu_item_id: 판매된 메뉴 ID
    :param quantity: 판매 수량
    """
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE menu
        SET sales_count = sales_count + ?
        WHERE menu_item_id = ?
        ''', (quantity, menu_item_id))
        conn.commit()

# 총액 계산 함수
def calculate_total_amount(order_id):
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT SUM(oi.quantity * m.price)
        FROM order_items oi
        JOIN menu m ON oi.menu_item_id = m.menu_item_id
        WHERE oi.order_id = ?
        ''', (order_id,))
        result = cursor.fetchone()
        return result[0] if result[0] is not None else 0

# 데이터 확인 함수
def check_db():
    with db_connection() as conn:
        cursor = conn.cursor()

        # 모든 테이블 조회
        tables = ["tables", "menu"]
        for table in tables:
            print(f"--- {table} ---")
            try:
                cursor.execute(f"SELECT * FROM {table}")
                rows = cursor.fetchall()

                # 출력
                for row in rows:
                    print(row)
            except sqlite3.OperationalError as e:
                print(f"Error accessing table {table}: {e}")
            print()


if __name__ == "__main__":
    check_db()