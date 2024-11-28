import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json
from rclpy.qos import QoSProfile, ReliabilityPolicy
import random  # 메뉴를 랜덤으로 업데이트하기 위해 추가


class OrderPublisher(Node):
    def __init__(self):
        super().__init__('order_publisher')
        
        # QoS 설정: Reliable, 큐 크기 10
        qos_profile = QoSProfile(
            depth=10,  # 큐의 크기
            reliability=ReliabilityPolicy.RELIABLE  # 신뢰성 설정 (Reliable)
        )

        # 퍼블리셔 생성
        self.publisher = self.create_publisher(String, 'order_topic', qos_profile)

        # 타이머 설정: 10초마다 publish_order 함수 호출
        self.timer = self.create_timer(10.0, self.publish_order)

        self.get_logger().info("Order Publisher Node has been started.")

        # 초기 주문 데이터
        self.orders = {
            "table_id": 1,
            "orders": [
                {"item": "파스타", "quantity": 3, "price": 10000},
                {"item": "피자", "quantity": 1, "price": 20000},
                {"item": "햄버거", "quantity": 3, "price": 30000}
            ]
        }

        # 업데이트 가능한 메뉴 리스트
        self.menu_items = [
            {"item": "파스타", "price": 10000},
            {"item": "피자", "price": 20000},
            {"item": "햄버거", "price": 30000},
            {"item": "샐러드", "price": 8000},
            {"item": "스테이크", "price": 40000}
        ]

    def publish_order(self):
        """주문 데이터를 업데이트하고 발행"""
        # 주문 데이터를 업데이트
        self.update_orders()

        # 메시지를 JSON 형식으로 직렬화하여 발행
        msg = String()
        msg.data = json.dumps(self.orders)  # JSON 직렬화
        self.publisher.publish(msg)
        self.get_logger().info(f"Published updated order: {msg.data}")

    def update_orders(self):
        """랜덤하게 주문 데이터를 업데이트"""
        # 테이블 ID를 랜덤으로 변경 (1~9번 테이블 중 하나)
        self.orders["table_id"] = random.randint(1, 9)

        # 랜덤한 메뉴 1~3개를 선택하여 새로운 주문 생성
        new_orders = random.sample(self.menu_items, k=random.randint(1, 3))
        for order in new_orders:
            order["quantity"] = random.randint(1, 5)  # 각 메뉴의 수량을 1~5 사이로 설정

        self.orders["orders"] = new_orders  # 업데이트된 주문 데이터 저장


def main():
    rclpy.init()
    node = OrderPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down Order Publisher Node.")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
