import sqlite3
import random
from datetime import datetime, timedelta

def get_current_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def db_connection():
    return sqlite3.connect('restaurant_db.db')

def drop_tables():
    with db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS deliver_log')
        cursor.execute('DROP TABLE IF EXISTS order_items')
        cursor.execute('DROP TABLE IF EXISTS orders')
        cursor.execute('DROP TABLE IF EXISTS menu')
        cursor.execute('DROP TABLE IF EXISTS tables')
        conn.commit()

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
            image TEXT
        );
        ''')

        # 테이블 생성: 주문 정보 (status 필드 제거)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_id INTEGER,
            order_time TIMESTAMP,
            total_amount INTEGER,
            FOREIGN KEY (table_id) REFERENCES tables(table_id)
        );
        ''')

        # 테이블 생성: 주문 상세 정보 (status 필드 추가)
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

def insert_tables_data():
    with db_connection() as conn:
        cursor = conn.cursor()
        tables_data = [
            (1, 0.0, 0.0),
            (2, 10.0, 0.0),
            (3, 20.0, 0.0),
            (4, 0.0, 10.0),
            (5, 10.0, 10.0),
            (6, 20.0, 10.0),
            (7, 0.0, 20.0),
            (8, 10.0, 20.0),
            (9, 20.0, 20.0)
        ]
        cursor.executemany('''
            INSERT INTO tables (table_id, x, y) VALUES (?, ?, ?)
        ''', tables_data)
        conn.commit()

def insert_menu_data():
    with db_connection() as conn:
        cursor = conn.cursor()
        menu_data = [
            (1, 'Pasta', 12000, 1, 'FOOD', '매콤하고 고소한 맛이 어우러진 파스타입니다.', ''),
            (2, 'Pizza', 35000, 1, 'FOOD', '풍부한 치즈와 신선한 재료들이 조화를 이루는 클래식한 피자입니다.', ''),
            (3, 'Steak', 50000, 1, 'FOOD', '육즙이 풍부한 스테이크, 부드럽고 깊은 맛을 자랑하는 고급스러운 한 끼를 선사합니다.', ''),
            (4, 'Salad', 10000, 1, 'FOOD', '신선한 채소와 함께하는 상큼하고 건강한 샐러드, 다른 음식과 깔끔하게 어우러집니다.', ''),
            (5, 'Chicken', 25000, 1, 'FOOD', '겉은 바삭하고 속은 촉촉한 치킨, 최고급 무항생제 닭을 사용해 건강한 한 끼를 즐길 수 있습니다.', ''),
            (6, 'Hamburger', 8000, 1, 'FOOD', '두툼한 패티와 신선한 채소가 어우러진 풍미 가득한 햄버거입니다.', ''),
            (7, 'Coke', 2000, 1, 'DRINK', '시원하고 청량한 콜라, 한 모금 마시면 입 안 가득 상쾌함이 퍼져나갑니다.', ''),
            (8, 'Sprite', 2000, 1, 'DRINK', '상큼하고 기분 좋은 청량감을 주는 스프라이트, 목을 시원하게 적셔줍니다.', ''),
            (9, 'House Wine', 6000, 1, 'DRINK', '부드럽고 우아한 향이 돋보이는 하우스 와인, 입 안에서 길게 여운이 남습니다.', ''),
            (10, 'Beer', 5000, 1, 'DRINK', '차가운 맥주 한 잔, 깊고 풍부한 맛이 목을 타고 넘어갑니다.', '')
        ]
        cursor.executemany('''
            INSERT INTO menu (menu_item_id, name, price, type_id, category, description, image)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', menu_data)
        conn.commit()
def insert_orders_and_order_items():
    with db_connection() as conn:
        cursor = conn.cursor()

        # 랜덤 주문 생성
        num_orders = 500  # 생성할 주문 수
        start_date = datetime(2024, 10, 1)
        end_date = datetime(2024, 11, 30)

        orders_data = []
        order_items_data = []
        deliver_log_data = []
        order_item_id_counter = 1  # order_item_id를 할당하기 위한 카운터
        deliver_id_counter = 1     # deliver_id를 할당하기 위한 카운터

        for order_id in range(1, num_orders + 1):
            # 랜덤 테이블 번호 (1 ~ 9)
            table_id = random.randint(1, 9)
            # 랜덤 주문 시간 (10월 1일 ~ 11월 30일)
            order_time = start_date + timedelta(
                seconds=random.randint(0, int((end_date - start_date).total_seconds()))
            )
            order_time_str = order_time.strftime('%Y-%m-%d %H:%M:%S')

            # 주문 아이템 수 (1 ~ 5개)
            num_items = random.randint(1, 5)
            total_amount = 0

            order_items_for_this_order = []

            for _ in range(num_items):
                # 랜덤 메뉴 아이템 ID (1 ~ 10)
                menu_item_id = random.randint(1, 10)
                # 랜덤 수량 (1 ~ 3)
                quantity = random.randint(1, 3)
                # 메뉴 가격 조회
                cursor.execute('SELECT price FROM menu WHERE menu_item_id = ?', (menu_item_id,))
                price = cursor.fetchone()[0]
                total_amount += price * quantity

                # 주문 아이템 상태 결정
                item_status = "Delivered"

                # 주문 아이템 데이터 추가
                order_items_for_this_order.append((
                    order_item_id_counter,
                    order_id,
                    menu_item_id,
                    quantity,
                    item_status
                ))

                # 배달 로그 생성 (Delivering 또는 Delivered 상태인 경우)
                if item_status in ['Delivering', 'Delivered']:
                    # 주문 시간 이후의 랜덤 시작 시간
                    start_time = order_time + timedelta(minutes=random.randint(1, 30))
                    start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
                    # Delivered 상태인 경우 종료 시간 설정
                    if item_status == 'Delivered':
                        end_time = start_time + timedelta(minutes=random.randint(5, 30))
                        end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        end_time_str = None

                    # 배달 로그 데이터 추가
                    deliver_log_data.append((
                        deliver_id_counter,
                        order_item_id_counter,
                        start_time_str,
                        end_time_str
                    ))
                    deliver_id_counter += 1

                order_item_id_counter += 1

            # 주문 데이터 추가 (total_amount 포함)
            orders_data.append((
                order_id,
                table_id,
                order_time_str,
                total_amount
            ))

            # 주문 아이템 데이터 추가
            order_items_data.extend(order_items_for_this_order)

        # 날짜를 기준으로 정렬 후, 같은 날짜 내에서 시간 순으로 정렬
        # 날짜와 시간을 분리하여 정렬하는 과정
        orders_data.sort(key=lambda x: (x[2][:10], x[2][11:]))  # 먼저 날짜, 그다음 시간으로 정렬

        # 주문 데이터 삽입
        cursor.executemany('''
            INSERT INTO orders (order_id, table_id, order_time, total_amount)
            VALUES (?, ?, ?, ?)
        ''', orders_data)

        # 주문 아이템 데이터 삽입
        cursor.executemany('''
            INSERT INTO order_items (order_item_id, order_id, menu_item_id, quantity, status)
            VALUES (?, ?, ?, ?, ?)
        ''', order_items_data)

        # 배달 로그 데이터 삽입
        cursor.executemany('''
            INSERT INTO deliver_log (deliver_id, order_item_id, start_time, end_time)
            VALUES (?, ?, ?, ?)
        ''', deliver_log_data)

        conn.commit()

def check_db():
    with db_connection() as conn:
        cursor = conn.cursor()

        # 모든 테이블 조회
        tables = ["tables", "menu", "orders", "order_items", "deliver_log"]
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
    # 기존 테이블 삭제 및 새로 생성
    drop_tables()
    create_db()

    # 데이터 삽입
    insert_tables_data()
    insert_menu_data()
    insert_orders_and_order_items()

    # 데이터 확인
    check_db()
