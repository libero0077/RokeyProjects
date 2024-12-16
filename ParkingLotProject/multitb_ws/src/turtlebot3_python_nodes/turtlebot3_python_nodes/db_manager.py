# src/turtlebot3_multi_robot/src/turtlebot3_multi_robot/db_manager.py

import sqlite3
import os
from contextlib import closing
from datetime import datetime

from ament_index_python.packages import get_package_share_directory

class DBManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.initialize_database()

    def initialize_database(self):
        """Initializes the database by creating required tables."""
        with closing(self.conn.cursor()) as cursor:
            # Create Parking_Slot table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Parking_Slot (
                slot_id INTEGER PRIMARY KEY,
                slot_name TEXT NOT NULL,
                location_x REAL NOT NULL,
                location_y REAL NOT NULL,
                vehicle_id TEXT,
                FOREIGN KEY (vehicle_id) REFERENCES Task_Log(vehicle_id)
            );
            ''')
            
            # Create Task_Log table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Task_Log (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                robot_id INTEGER NOT NULL,
                vehicle_id TEXT NOT NULL,
                vehicle_img TEXT NOT NULL,
                slot_id INTEGER,
                task_type TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT,
                status TEXT NOT NULL,
                FOREIGN KEY (robot_id) REFERENCES Robot_Info(robot_id),
                FOREIGN KEY (slot_id) REFERENCES Parking_Slot(slot_id)
            );
            ''')


            # Create Robot_Info table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Robot_Info (
                robot_id INTEGER PRIMARY KEY,
                initial_location_x REAL NOT NULL,
                initial_location_y REAL NOT NULL,
                status TEXT NOT NULL,
                last_task_id INTEGER,
                FOREIGN KEY (last_task_id) REFERENCES Task_Log(task_id)
            );
            ''')

            # Create Parking_Fee_Policy table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Parking_Fee_Policy (
                policy_id INTEGER PRIMARY KEY AUTOINCREMENT,
                policy_name TEXT NOT NULL,
                base_time INTEGER NOT NULL,
                base_fee INTEGER NOT NULL,
                additional_time INTEGER NOT NULL,
                additional_fee INTEGER NOT NULL,
                active BOOLEAN NOT NULL
            );
            ''')

            # Create Payment_Log table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Payment_Log (
                payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehicle_id TEXT NOT NULL,
                entry_time TEXT NOT NULL,
                exit_time TEXT NOT NULL,
                total_fee INTEGER NOT NULL,
                payment_method TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (vehicle_id) REFERENCES Task_Log(vehicle_id)
            );
            ''')

            # Create System_Logs table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS System_Logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                event_details TEXT NOT NULL,
                timestamp TEXT NOT NULL
            );
            ''')
        self.conn.commit()

    def insert_data(self, table, data):
        # 데이터 삽입 함수

        # data = {
        #     "slot_name": "A-0",
        #     "location_x": "10.1",
        #     "location_y": "10.3",
        #     "vehicle_id": "1234"
        # }
        # db_manager.insert_data("Parking_Slot", data)

        """Inserts a row into the specified table."""
        with closing(self.conn.cursor()) as cursor:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?'] * len(data))
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            cursor.execute(query, list(data.values()))
        self.conn.commit()

    def update_data(self, table, data, conditions, parameters=None):
        # 데이터 업데이트 함수

        # data = {
        #     "slot_name": "D-1",
        #     "location_x": 12.5
        # }
        # conditions = ["slot_id = 1", "vehicle_id = 5678"]
        # db_manager.update_data("Parking_Slot", data, condition)

        """Updates rows in the specified table based on multiple conditions."""
        with closing(self.conn.cursor()) as cursor:
            updates = ', '.join([f"{key} = ?" for key in data.keys()])
            condition_str = ' AND '.join(conditions)
            all_parameters = list(data.values())
            if parameters:
                all_parameters += parameters
            query = f"UPDATE {table} SET {updates} WHERE {condition_str}"
            cursor.execute(query, all_parameters)
        self.conn.commit()

    def delete_data(self, table, conditions, parameters=None):
        # 데이터 삭제 함수

        # conditions = ["slot_id = 1", "vehicle_id = 5678"]
        # db_manager.update_data("Parking_Slot", data, condition)

        """Deletes rows from the specified table based on multiple conditions."""
        with closing(self.conn.cursor()) as cursor:
            condition_str = ' AND '.join(conditions)
            query = f"DELETE FROM {table} WHERE {condition_str}"
            if parameters:
                cursor.execute(query, parameters)
            else:
                cursor.execute(query)
        self.conn.commit()

    def fetch_data(self, table, columns="*", conditions=None, parameters=None):
        # 데이터 조회 함수

        # conditions = ["slot_id = 1", "vehicle_id = 5678"]
        # data = db_manager.fetch_data("Parking_Slot", conditions=conditions)

        """Fetches data from the specified table based on multiple conditions."""
        with closing(self.conn.cursor()) as cursor:
            query = f"SELECT {columns} FROM {table}"
            if conditions:
                condition_str = ' AND '.join(conditions)
                query += f" WHERE {condition_str}"
            cursor.execute(query, parameters if parameters else [])
            return cursor.fetchall()

    def check_table_exists(self, table):
        # 테이블 존재 유무 확인 함수

        """Checks if a table exists in the database."""
        with closing(self.conn.cursor()) as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
            return cursor.fetchone() is not None
        
    def print_table_contents(self, table):
        # 테이블 출력 함수

        """Fetches and prints all rows from the specified table."""
        print(f"[{table}]")

        data = self.fetch_data(table)

        # Fetch column names
        with closing(self.conn.cursor()) as cursor:
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [description[1] for description in cursor.fetchall()]

        print(columns)

        if data:
            for row in data:
                print(row)
        else:
            print(f"No data found in {table} table.")

    def calculate_fee(self, vehicle_id):
        """Calculates parking fee based on vehicle_id."""
        # 최신 Task_Log 조회
        task_logs = self.fetch_data(
            table="Task_Log",
            columns="task_id, start_time, end_time, status",
            conditions=[f"vehicle_id = '{vehicle_id}'"]
        )

        if not task_logs:
            print(f"No Task_Log found for vehicle_id: {vehicle_id}")
            return 0

        # 가장 최근 Task_Log 사용
        task_id, start_time, end_time, status = task_logs[-1]

        # 시작 시간과 종료 시간 파싱
        start = datetime.fromisoformat(start_time)
        if end_time:
            end = datetime.fromisoformat(end_time)
        else:
            end = datetime.now()
        
        duration_minutes = (end - start).total_seconds() / 60  # 분 단위

        # 활성화된 요금 정책 조회
        fee_policies = self.fetch_data(
            table="Parking_Fee_Policy",
            conditions=["active = 1"]
        )
        if not fee_policies:
            print("활성화된 요금 정책이 없습니다.")
            return 0

        # 예시로 첫 번째 활성화된 요금 정책 사용
        policy = fee_policies[0]
        _, policy_name, base_time, base_fee, additional_time, additional_fee, active = policy

        # 요금 계산
        if duration_minutes <= base_time:
            total_fee = base_fee
        else:
            additional = (duration_minutes - base_time) / additional_time
            total_fee = base_fee + (int(additional) + 1) * additional_fee

        print(f"Vehicle ID: {vehicle_id}, Duration: {duration_minutes}분, Total Fee: {total_fee}원")
        return total_fee
    
    def get_slot_id_by_vehicle_id(self, vehicle_id):
        """vehicle_id를 기반으로 Parking_Slot에서 slot_id를 조회합니다."""
        slot = self.fetch_data(
            table="Parking_Slot",
            columns="slot_id",
            conditions=["vehicle_id = ?"],
            parameters=[vehicle_id]
        )
        if slot:
            return slot[-1][0]  # 가장 최근 슬롯 ID 반환
        else:
            print(f"No Parking_Slot found for vehicle_id: {vehicle_id}")
            return None
            
    def execute_transaction(self, operations):
        """여러 DB 작업을 원자적으로 실행합니다."""
        try:
            self.conn.execute('BEGIN')
            for operation in operations:
                query, params = operation
                self.conn.execute(query, params)
            self.conn.commit()
        except sqlite3.Error as e:
            self.conn.rollback()
            self.get_logger().error(f"Transaction failed: {e}")
            raise

    def get_last_parking_image(self, vehicle_id):
        """
        특정 차량의 가장 최근 'Park' 작업에서 vehicle_img를 가져옵니다.
        """
        task_logs = self.fetch_data(
            table="Task_Log",
            columns="vehicle_img",
            conditions=["vehicle_id = ?", "task_type = ?"],
            parameters=[vehicle_id, "Park"]
        )
        if task_logs:
            return task_logs[-1][0]  # 가장 최근 작업의 vehicle_img 반환
        else:
            print(f"No Parking Task found for vehicle_id: {vehicle_id}")
            return "default_img.jpg"  # 기본 이미지 경로 반환하거나 다른 처리를 할 수 있음
    

if __name__ == "__main__":
    # Launch 파일과 동일한 경로를 사용하도록 수정
    db_path = "/home/rokey/Documents/RokeyProjects/multitb_ws/src/turtlebot3_python_nodes/db/parking_system.db"
    db_manager = DBManager(db_path)
    data = {
    'vehicle_id': "9160"
    }
    condition = ["slot_name = 'A-916'"]
    db_manager.update_data('Parking_Slot', data, condition)
    # # data = {
    # # 'end_time' : None,
    # # 'status' : "주차 완료",
    # # }
    # # conditions = ["task_id = 1"]
    # # db_manager.update_data('Task_Log', data, conditions)
    # data = {
    # 'robot_id' : 1,
    # 'vehicle_id' : '9160',
    # 'vehicle_img' : '/home/rokey/Documents/RokeyProjects/multitb_ws/src/turtlebot3_python_nodes/db/img/car_1111.jpeg',
    # 'slot_id' : 49,
    # 'task_type' : '주차',
    # 'start_time' : '2024-12-15T10:45:00',
    # 'end_time' : '2024-12-15T10:48:00',
    # 'statu    data = {
    'vehicle_id': "9160"
    }
    condition = ["slot_name = 'A-916'"]
    db_manager.update_data('Parking_Slot', data, condition)s' : '주차 완료'
    # }
    # db_manager.insert_data('Task_Log', data)
    db_manager.delete_data('Task_Log', {'vehicle_img = "default_img.jpg"'})
    

    db_manager.print_table_contents("Parking_Slot")
    db_manager.print_table_contents("Parking_Fee_Policy")
    db_manager.print_table_contents("Robot_Info")
    db_manager.print_table_contents("Task_Log")
    db_manager.print_table_contents("Payment_Log")

