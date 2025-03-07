#오류 발생시 터미널에서 실행
# export QT_QPA_PLATFORM=wayland

import os
from datetime import datetime

import sys
import json
import numpy as np
import cv2
from cv_bridge import CvBridge

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import CompressedImage  # CompressedImage 메시지 타입 추가
from std_msgs.msg import String  # String 메시지 타입 추가

import threading  # threading 모듈 추가
from threading import Thread

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel,
    QDesktopWidget, QMessageBox, QDialog, QTextEdit, QRadioButton, QCheckBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer, QTime, QThread, QObject, pyqtSignal

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Signal 클래스 정의
class Signals(QObject):
    update_status = pyqtSignal(str)  # 상태 메시지를 전달할 시그널
    update_image = pyqtSignal(QtGui.QPixmap)  # 이미지 업데이트를 위한 시그널

class ClickableLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            print("ClickableLabel was clicked")  # 디버그 로그
            self.clicked.emit()
        super().mousePressEvent(event)

# GUI 통합 클래스
class Ui_main(object):
    def __init__(self):
        self.signals = Signals()

    def setupUi(self, main_ui):
        self.signals.update_status.connect(self.update_status_text)  # 시그널-슬롯 연결
        self.signals.update_image.connect(self.update_image_label)   # 이미지 업데이트 시그널 연결

        self.set_monokai_theme(main_ui)

        main_ui.setObjectName("main_ui")
        main_ui.setWindowModality(QtCore.Qt.NonModal)
        main_ui.setEnabled(True)
        main_ui.resize(660, 795)
        
        self.media_label = ClickableLabel(main_ui)
        self.media_label.setGeometry(QtCore.QRect(10, 50, 640, 480))
        self.media_label.setStyleSheet("color: green; background-color: black;")  # 스타일 설정
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.media_label.setFont(font)
        self.media_label.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.media_label.setAlignment(QtCore.Qt.AlignCenter)
        self.media_label.setObjectName("media_label")

        self.conveyor_status_button = QtWidgets.QCheckBox(main_ui)
        self.conveyor_status_button.setEnabled(False)
        self.conveyor_status_button.setGeometry(QtCore.QRect(10, 540, 271, 23))
        self.conveyor_status_button.setObjectName("conveyor_status_button")
        
        self.conveyor_button = QtWidgets.QPushButton(main_ui)
        self.conveyor_button.setEnabled(False)
        self.conveyor_button.setGeometry(QtCore.QRect(10, 570, 271, 61))
        self.conveyor_button.setObjectName("conveyor_button")
        
        self.collect_data_button = QtWidgets.QPushButton(main_ui)
        self.collect_data_button.setEnabled(False)
        self.collect_data_button.setGeometry(QtCore.QRect(10, 640, 271, 51))
        self.collect_data_button.setObjectName("collect_data_button")
        
        self.Emergency_button = QtWidgets.QPushButton(main_ui)
        self.Emergency_button.setGeometry(QtCore.QRect(10, 700, 641, 81))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.Emergency_button.setFont(font)
        self.Emergency_button.setObjectName("Emergency_button")
        
        self.pause_button = QtWidgets.QPushButton(main_ui)
        self.pause_button.setEnabled(False)
        self.pause_button.setGeometry(QtCore.QRect(300, 610, 111, 41))
        self.pause_button.setObjectName("pause_button")
        
        self.stop_button = QtWidgets.QPushButton(main_ui)
        self.stop_button.setEnabled(False)
        self.stop_button.setGeometry(QtCore.QRect(540, 610, 111, 41))
        self.stop_button.setObjectName("stop_button")
        
        self.resume_button = QtWidgets.QPushButton(main_ui)
        self.resume_button.setEnabled(False)
        self.resume_button.setGeometry(QtCore.QRect(420, 610, 111, 41))
        self.resume_button.setObjectName("resume_button")
        
        self.start_button = QtWidgets.QPushButton(main_ui)
        self.start_button.setEnabled(False)
        self.start_button.setGeometry(QtCore.QRect(540, 570, 111, 31))
        self.start_button.setObjectName("start_button")
        
        self.reset_button = QtWidgets.QPushButton(main_ui)
        self.reset_button.setEnabled(False)
        self.reset_button.setGeometry(QtCore.QRect(300, 660, 351, 31))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.reset_button.setFont(font)
        self.reset_button.setObjectName("reset_button")
        
        self.processing_timer = QtWidgets.QLabel(main_ui)
        self.processing_timer.setGeometry(QtCore.QRect(310, 540, 341, 21))
        self.processing_timer.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.processing_timer.setObjectName("processing_timer")
        
        self.status_text = QtWidgets.QPlainTextEdit(main_ui)
        self.status_text.setGeometry(QtCore.QRect(10, 10, 641, 31))
        self.status_text.setReadOnly(True)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.status_text.setFont(font)
        self.status_text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.status_text.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.status_text.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.status_text.setObjectName("status_text")
        
        self.comboBox = QtWidgets.QComboBox(main_ui)
        self.comboBox.setGeometry(QtCore.QRect(300, 574, 231, 31))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        
        self.retranslateUi(main_ui)
        QtCore.QMetaObject.connectSlotsByName(main_ui)


    def set_monokai_theme(self, main_ui):
    # 전체 배경과 각 요소에 스타일 적용
        main_ui.setStyleSheet("""
            QWidget {
                background-color: #272822;
                color: #f8f8f2;
            }
            QLabel {
                color: #f8f8f2;
            }
            QPlainTextEdit {
                background-color: #272822;
                color: #f8f8f2;
                border: 1px solid #444444;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #444444;
                color: #f8f8f2;
                border: 1px solid #555555;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QPushButton:pressed {
                background-color: #66d9ef;
            }
            QPushButton:disabled {
                background-color: #444444;
                color: #888888;
                border: 1px solid #666666;
            }
            QLineEdit {
                background-color: #272822;
                color: #f8f8f2;
                border: 1px solid #444444;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #66d9ef;
            }
            QCheckBox {
                color: #F5F5F5;
                font-size: 16px;
                padding: 5px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 3px;
                border: 2px solid #F5F5F5;
                background-color: #2E2E2E;
            }
            QCheckBox::indicator:checked {
                background-color: #66D9EF;
                border: 2px solid #66D9EF;
            }
            QCheckBox::indicator:disabled {
                border: 2px solid #666666;
                background-color: #444444;
            }
            QCheckBox::indicator:disabled:checked {
                background-color: #666666;
                border: 2px solid #666666;
            }
        """)

    
    def retranslateUi(self, main_ui):
        _translate = QtCore.QCoreApplication.translate
        main_ui.setWindowTitle(_translate("main_ui", "team 5 week5"))
        self.media_label.setText(_translate("main_ui", "카메라 연결 중..."))
        self.conveyor_button.setText(_translate("main_ui", "컨베이어 작동"))
        self.collect_data_button.setText(_translate("main_ui", "학습 데이터 수집"))
        self.Emergency_button.setText(_translate("main_ui", "비상 정지"))
        self.pause_button.setText(_translate("main_ui", "일시정지"))
        self.stop_button.setText(_translate("main_ui", "정지"))
        self.resume_button.setText(_translate("main_ui", "작업 재게"))
        self.start_button.setText(_translate("main_ui", "시작"))
        self.reset_button.setText(_translate("main_ui", "초기화"))
        self.processing_timer.setText(_translate("main_ui", "작업 소요 시간 - "))
        self.status_text.setPlainText(_translate("main_ui", "연결을 기다리는 중..."))
        self.conveyor_status_button.setText(_translate("main_ui", "컨베이어 수동 조작"))
        self.comboBox.setItemText(0, _translate("main_ui", "JOB1"))
        self.comboBox.setItemText(1, _translate("main_ui", "JOB2"))
        self.comboBox.setItemText(2, _translate("main_ui", "JOB3"))

        # media_label 클릭 시 save_current_frame 함수 호출
        self.media_label.clicked.connect(self.save_current_frame)

        # 체크박스 상태 변경 시 호출할 함수 연결
        self.conveyor_status_button.stateChanged.connect(self.handle_conveyor_status_change)

        # 버튼 이벤트 연결
        self.start_button.clicked.connect(self.handle_start_button)
        self.stop_button.clicked.connect(lambda: self.handle_job_button("STOP"))
        self.pause_button.clicked.connect(lambda: self.handle_job_button("PAUSE"))
        self.resume_button.clicked.connect(lambda: self.handle_job_button("RESUME"))
        self.reset_button.clicked.connect(lambda: self.handle_job_button("RESET"))

        # 학습 데이터 수집 연결
        self.collect_data_button.clicked.connect(self.handle_collect_data_button)


        # 비상 정지 버튼 클릭 이벤트 연결
        self.Emergency_button.clicked.connect(self.handle_emergency_button)

        # 컨베이어 버튼 이벤트 연결
        self.conveyor_button.pressed.connect(self.handle_conveyor_move_pressed)
        self.conveyor_button.released.connect(self.handle_conveyor_move_released)

    def save_current_frame(self):
        # 현재 media_label에 표시된 pixmap 가져오기
        print("save_current_frame called")  # 디버그
        pixmap = self.media_label.pixmap()
        if pixmap:
            # 원하는 경로에 저장 (여기서는 예시로 현재 경로에 frame.png로 저장)
            # 폴더가 없다면 미리 만들어두거나 경로를 변경하세요.
            save_path = "./frame.png"  
            success = pixmap.save(save_path, "PNG")
            if success:
                print(f"이미지가 {save_path} 에 저장되었습니다.")
            else:
                print("이미지 저장에 실패했습니다.")



    def set_monokai_theme(self, main_ui):
    # 전체 배경과 각 요소에 스타일 적용
        main_ui.setStyleSheet("""
            QWidget {
                background-color: #272822;
                color: #f8f8f2;
            }
            QLabel {
                color: #f8f8f2;
            }
            QPlainTextEdit {
                background-color: #272822;
                color: #f8f8f2;
                border: 1px solid #444444;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #444444;
                color: #f8f8f2;
                border: 1px solid #555555;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QPushButton:pressed {
                background-color: #66d9ef;
            }
            QPushButton:disabled {
                background-color: #444444;
                color: #888888;
                border: 1px solid #666666;
            }
            QLineEdit {
                background-color: #272822;
                color: #f8f8f2;
                border: 1px solid #444444;
                border-radius: 5px;
            }
            QLineEdit:focus {
                border: 1px solid #66d9ef;
            }
            QCheckBox {
                color: #F5F5F5;
                font-size: 16px;
                padding: 5px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 3px;
                border: 2px solid #F5F5F5;
                background-color: #2E2E2E;
            }
            QCheckBox::indicator:checked {
                background-color: #66D9EF;
                border: 2px solid #66D9EF;
            }
            QCheckBox::indicator:disabled {
                border: 2px solid #666666;
                background-color: #444444;
            }
            QCheckBox::indicator:disabled:checked {
                background-color: #666666;
                border: 2px solid #666666;
            }
        """)

    
    def retranslateUi(self, main_ui):
        _translate = QtCore.QCoreApplication.translate
        main_ui.setWindowTitle(_translate("main_ui", "team 5 week5"))
        self.media_label.setText(_translate("main_ui", "카메라 연결 중..."))
        self.conveyor_button.setText(_translate("main_ui", "컨베이어 작동"))
        self.collect_data_button.setText(_translate("main_ui", "학습 데이터 수집"))
        self.Emergency_button.setText(_translate("main_ui", "비상 정지"))
        self.pause_button.setText(_translate("main_ui", "일시정지"))
        self.stop_button.setText(_translate("main_ui", "정지"))
        self.resume_button.setText(_translate("main_ui", "작업 재게"))
        self.start_button.setText(_translate("main_ui", "시작"))
        self.reset_button.setText(_translate("main_ui", "초기화"))
        self.processing_timer.setText(_translate("main_ui", "작업 소요 시간 - "))
        self.status_text.setPlainText(_translate("main_ui", "연결을 기다리는 중..."))
        self.conveyor_status_button.setText(_translate("main_ui", "컨베이어 수동 조작"))
        self.comboBox.setItemText(0, _translate("main_ui", "JOB1"))
        self.comboBox.setItemText(1, _translate("main_ui", "JOB2"))
        self.comboBox.setItemText(2, _translate("main_ui", "JOB3"))

        # media_label 클릭 시 save_current_frame 함수 호출
        self.media_label.clicked.connect(self.save_current_frame)

        # 체크박스 상태 변경 시 호출할 함수 연결
        self.conveyor_status_button.stateChanged.connect(self.handle_conveyor_status_change)

        # 버튼 이벤트 연결
        self.start_button.clicked.connect(self.handle_start_button)
        self.stop_button.clicked.connect(lambda: self.handle_job_button("STOP"))
        self.pause_button.clicked.connect(lambda: self.handle_job_button("PAUSE"))
        self.resume_button.clicked.connect(lambda: self.handle_job_button("RESUME"))
        self.reset_button.clicked.connect(lambda: self.handle_job_button("RESET"))

        # 학습 데이터 수집 연결
        self.collect_data_button.clicked.connect(self.handle_collect_data_button)


        # 비상 정지 버튼 클릭 이벤트 연결
        self.Emergency_button.clicked.connect(self.handle_emergency_button)

        # 컨베이어 버튼 이벤트 연결
        self.conveyor_button.pressed.connect(self.handle_conveyor_move_pressed)
        self.conveyor_button.released.connect(self.handle_conveyor_move_released)

    def save_current_frame(self):
        # 현재 media_label에 표시된 pixmap 가져오기
        pixmap = self.media_label.pixmap()
        if pixmap:
            # 이미지 저장 폴더 생성
            save_dir = os.path.abspath("./images")
            os.makedirs(save_dir, exist_ok=True)

            # 현재 시간 기반 파일 이름 생성
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(save_dir, f"frame_{timestamp}.png")

            # 이미지 저장
            success = pixmap.save(save_path, "PNG")
            if success:
                print(f"이미지가 {save_path} 에 저장되었습니다.")
            else:
                print("이미지 저장에 실패했습니다.")
        else:
            print("현재 표시 중인 이미지가 없습니다. 저장 불가.")


    def handle_start_button(self):
        """STATE 버튼 클릭 시 호출."""
        if hasattr(self, 'ui_node') and self.ui_node:
            selected_job = self.comboBox.currentText()  # 콤보 박스에서 선택된 JOB 이름 가져오기
            msg = String()
            msg.data = f"[JOB]{selected_job}"
            self.ui_node.ui_commend_publisher.publish(msg)
            self.ui_node.get_logger().info(f"[JOB] 메시지 발행: {msg.data}")
        else:
            print("UI Node가 초기화되지 않았습니다.")

    def handle_job_button(self, command):
        """JOB 관련 버튼 클릭 시 호출."""
        if hasattr(self, 'ui_node') and self.ui_node:
            selected_job = self.comboBox.currentText()  # 콤보 박스에서 선택된 JOB 이름 가져오기
            msg = String()
            msg.data = f"[JOB]{command}"
            self.ui_node.ui_commend_publisher.publish(msg)
            self.ui_node.get_logger().info(f"[JOB]{command} 메시지 발행: {msg.data}")
        else:
            print("UI Node가 초기화되지 않았습니다.")

    def handle_conveyor_move_pressed(self):
        """컨베이어 버튼이 눌렸을 때 호출"""
        if hasattr(self, 'ui_node') and self.ui_node:
            msg = String()
            msg.data = "[CONVEYOR]MOVE"
            self.ui_node.ui_commend_publisher.publish(msg)
            self.ui_node.get_logger().info(f"[CONVEYOR]MOVE 메시지가 발행되었습니다.")
        else:
            print("UI Node가 초기화되지 않았습니다.")

    def handle_conveyor_move_released(self):
        """컨베이어 버튼에서 손을 뗐을 때 호출"""
        if hasattr(self, 'ui_node') and self.ui_node:
            msg = String()
            msg.data = "[CONVEYOR]STOP"
            self.ui_node.ui_commend_publisher.publish(msg)
            self.ui_node.get_logger().info(f"[CONVEYOR]STOP 메시지가 발행되었습니다.")
        else:
            print("UI Node가 초기화되지 않았습니다.")

    def handle_emergency_button(self):
        """비상 정지 버튼 클릭 시 호출."""
        if not hasattr(self, 'ui_node') or not self.ui_node:
            print("UI Node가 초기화되지 않았습니다.")
            return

        msg = String()
        if self.Emergency_button.text() == "비상 정지":
            msg.data = "[ESTOP]STOP"
        elif self.Emergency_button.text() == "정지 해제":
            msg.data = "[ESTOP]NONE"

        # 메시지 발행
        self.ui_node.ui_commend_publisher.publish(msg)
        self.ui_node.get_logger().info(f"[ESTOP] 메시지 발행: {msg.data}")

    def handle_conveyor_status_change(self, state):
        """
        컨베이어 수동 조작 체크박스 상태 변경 시 호출되는 슬롯.
        :param state: int - 체크박스 상태 (0: OFF, 2: ON)
        """
        if hasattr(self, 'ui_node') and self.ui_node:
            msg = String()
            if state == QtCore.Qt.Checked:
                msg.data = "[CONVEYOR]manual"
                self.conveyor_button.setEnabled(True)  # 컨베이어 버튼 활성화
            else:
                msg.data = "[CONVEYOR]auto"
                self.conveyor_button.setEnabled(False)  # 컨베이어 버튼 비활성화

            self.ui_node.ui_commend_publisher.publish(msg)
            self.ui_node.get_logger().info(f"컨베이어 상태 메시지 발행: {msg.data}")
        else:
            print("ui_node가 UI와 연결되지 않았습니다.")

    def update_status_text(self, message):
        """status_text 업데이트 함수"""
        self.status_text.setPlainText(message)  # 상태 메시지 업데이트

    def update_image_label(self, pixmap):
        """media_label에 이미지를 업데이트하는 슬롯"""
        self.media_label.setPixmap(pixmap.scaled(
            self.media_label.width(),
            self.media_label.height(),
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation
        ))

    def handle_collect_data_button(self):
        """학습 데이터 수집 버튼 클릭 시 호출."""
        if hasattr(self, 'ui_node') and self.ui_node:
            msg = String()
            # 버튼의 텍스트를 확인하여 적절한 메시지를 발행
            if self.collect_data_button.text() == "학습 데이터 수집":
                msg.data = "[학습데이터수집]START"
                self.ui_node.ui_commend_publisher.publish(msg)
                self.ui_node.get_logger().info(f"[학습데이터수집]START 메시지 발행: {msg.data}")
                # self.collect_data_button.setText("학습 데이터 수집 중단")  # 버튼 텍스트 변경
            elif self.collect_data_button.text() == "학습 데이터 수집 중단":
                msg.data = "[학습데이터수집]STOP"
                self.ui_node.ui_commend_publisher.publish(msg)
                self.ui_node.get_logger().info(f"[학습데이터수집]STOP 메시지 발행: {msg.data}")
                # self.collect_data_button.setText("학습 데이터 수집")  # 버튼 텍스트 원래대로 되돌리기
        else:
            print("UI Node가 초기화되지 않았습니다.")


# 로그인 창 추가 (이전과 동일한 로그인 기능)
class Login(QWidget):
    def __init__(self, gui_node):
        super().__init__()
        self.gui_node = gui_node
        self.email = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('시스템 로그인')
        self.resize(450, 350)
        self.setMinimumSize(300, 250)
        # self.setStyleSheet("background-color: #F5F6F7;")

        # 다크 테마 스타일 적용
        self.setStyleSheet("""
            QWidget {
                background-color: #2E2E2E;
                color: #F5F5F5;
            }
            QLabel {
                color: #F5F5F5;
            }
            QLineEdit {
                border: 1px solid #444444;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
                background-color: #3E3D32;
                color: #F5F5F5;
            }
            QLineEdit:focus {
                border: 1px solid #66D9EF;
            }
            QPushButton {
                background-color: #1E90FF;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 15px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5ACCFF;
            }
            QPushButton:pressed {
                background-color: #4498cc;
            }
        """)

        # 화면 중앙 배치
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        layout.addStretch(1)

        # 로그인 제목
        title_label = QLabel('로그인')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Arial', 24, QFont.Bold))
        layout.addWidget(title_label)

        layout.addStretch(1)

        # 이메일 입력
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("이메일")
        # self.email_input.setStyleSheet("""
        #     QLineEdit {
        #         border: 1px solid #DADADA;
        #         border-radius: 5px;
        #         padding: 10px;
        #         font-size: 16px;
        #         background-color: white;
        #     }
        # """)
        layout.addWidget(self.email_input)

        # 비밀번호 입력
        self.pw_input = QLineEdit()
        self.pw_input.setPlaceholderText("비밀번호")
        self.pw_input.setEchoMode(QLineEdit.Password)
        # self.pw_input.setStyleSheet("""
        #     QLineEdit {
        #         border: 1px solid #DADADA;
        #         border-radius: 5px;
        #         padding: 10px;
        #         font-size: 16px;
        #         background-color: white;
        #     }
        # """)
        layout.addWidget(self.pw_input)

        layout.addStretch(1)

        # 로그인 버튼
        login_button = QPushButton("로그인")
        # login_button.setStyleSheet("""
        #     QPushButton {
        #         background-color: #1E90FF;
        #         color: white;
        #         border: none;
        #         border-radius: 5px;
        #         padding: 15px;
        #         font-size: 18px;
        #         font-weight: bold;
        #     }
        #     QPushButton:hover {
        #         background-color: #5ACCFF;
        #     }
        # """)
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        layout.addStretch(1)

        self.setLayout(layout)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.login()

    def login(self):
        if self.pw_input.text() == "rokey":
            self.email = self.email_input.text()
            if not self.email:
                QMessageBox.warning(self, "로그인 실패", "이메일을 입력하세요.")
                return
            self.gui_node.email = self.email
            self.gui_node.get_logger().info(f"로그인된 이메일: {self.email}")
            QMessageBox.information(self, "로그인 성공", f"{self.email}님 환영합니다.")
            self.open_main_window()
        else:
            QMessageBox.warning(self, "로그인 실패", "비밀번호가 올바르지 않습니다.")

    def open_main_window(self):
        # 로그인 성공 시 메인 UI를 표시
        self.main_ui_widget = QtWidgets.QWidget()
        self.ui_main = Ui_main()
        self.ui_main.setupUi(self.main_ui_widget)

        # ROS 노드와 UI 연결
        self.gui_node.ui = self.ui_main
        self.ui_main.ui_node = self.gui_node
        self.gui_node.signals = self.ui_main.signals

        self.main_ui_widget.show()
        self.close()


# ROS 통합 클래스
class UINode(Node):
    def __init__(self):
        super().__init__('ui_node')
        self.get_logger().info("UI Node started")

        # UI 객체 연결
        self.ui = None  # UI 객체는 런타임에 설정

        # 플래그
        self.setup_completed = False    # 초기화 플래그

        # 퍼블리셔와 서브스크라이버 설정
        self.ui_commend_publisher = None
        self.setup_publisher_and_subscriber()

        # 타이머 데이터를 저장할 변수
        self.current_job_time = "00:00:00"

        # Signals와 UI 연결 (추후 연결)
        if self.ui:
            self.signals.update_status.connect(self.ui.status_text.setPlainText)
            self.signals.update_image.connect(self.ui.update_image_label)




    #--------------------시작---------------------------------
        # 첫 SETUP 메시지 발송 (초기화 이후로 이동)
        self.create_timer(0.5, self.send_setup_message)


    #------------------------------퍼블리셔 서브스크라이브
    def setup_publisher_and_subscriber(self):
        """퍼블리셔와 서브스크라이버 설정"""
        self.ui_commend_publisher = self.create_publisher(String, 'ui_commend', 10)
        self.main_commend_subscriber = self.create_subscription(String, 'main_commend', self.main_commend_callback, 10)
        self.image_subscriber = self.create_subscription(CompressedImage,'world_cam_node/image_raw/compressed',self.image_callback,10)
    #------------------------------퍼블리셔 서브스크라이브

    #-------------------------------main_commend 메세지 처리 시작
    def main_commend_callback(self, msg):
        """main_commend 메시지를 처리하는 콜백."""
        self.get_logger().info(f"ui_commend에서 수신됨: {msg.data}")

        if "[STATUS]" in msg.data:
            self.get_logger().info(f"[STATUS] 메시지 수신: {msg.data}")
            full_message = msg.data[len("[STATUS]"):].strip()  # [STATUS] 뒤의 내용만 추출

            if "[EMAIL][WARN]" in full_message and "카메라 연결이 끊어졌습니다." in full_message:
                if self.ui:
                    # media_label 초기화 및 기본 라벨 화면으로 되돌리기
                    self.ui.media_label.clear()
                    self.ui.media_label.setText("카메라 연결 기다리는 중...")  # 기본 텍스트로 복원
                    self.ui.media_label.setAlignment(QtCore.Qt.AlignCenter)  # 텍스트 중앙 정렬
                    self.ui.media_label.setStyleSheet("color: green; background-color: black;")  # 스타일 설정

                self.get_logger().info("[WARN] 카메라 연결이 끊어졌습니다. 기본 라벨로 복원")

            elif "[EMAIL]" in full_message:
                email_message = full_message.split("[EMAIL]", 1)[1].strip()
                display_message = full_message.replace("[EMAIL]", "").strip()

                if self.ui:
                    self.ui.signals.update_status.emit(display_message)

                # 이메일 전송: 별도 스레드에서 실행
                email_thread = threading.Thread(target=self.send_email, args=(email_message,), daemon=True)
                email_thread.start()
            else:
                if self.ui:
                    self.ui.signals.update_status.emit(full_message)

        elif "[JOB]time=" in msg.data:
            self.get_logger().info(f"작업 시간 메시지 수신: {msg.data}")
            self.update_job_time(msg.data)

        elif msg.data == "[ESTOP]STOP":
            self.get_logger().info("[ESTOP]STOP 메시지 수신.")
            if self.ui:
                self.ui.Emergency_button.setText("정지 해제")

            # 모든 버튼 비활성화
            buttons = [
                self.ui.conveyor_button, self.ui.collect_data_button, self.ui.pause_button,
                self.ui.stop_button, self.ui.resume_button, self.ui.start_button, self.ui.reset_button
            ]
            for button in buttons:
                button.setEnabled(False)

            # 컨베이어 수동 조작 체크박스 비활성화
            self.ui.conveyor_status_button.setEnabled(False)

        elif msg.data == "[ESTOP]NONE":
            self.get_logger().info("[ESTOP]NONE 메시지 수신.")
            if self.ui:
                self.ui.Emergency_button.setText("비상 정지")
                self.ui.collect_data_button.setText("학습 데이터 수집")

        # 학습 데이터 수집 START 메시지 처리
        elif msg.data == "[학습데이터수집]START":
            self.get_logger().info("[학습데이터수집]START 메시지 수신.")
            if self.ui:
                self.ui.collect_data_button.setText("학습 데이터 수집 중단")
                # 학습 데이터 수집 버튼을 중단 버튼으로 변경
                self.ui.collect_data_button.setEnabled(True)  # 버튼 활성화

        elif msg.data == "[학습데이터수집]STOP":
            self.get_logger().info("[학습데이터수집]STOP 메시지 수신.")
            if self.ui:
                self.ui.collect_data_button.setText("학습 데이터 수집")
                # 중단 버튼을 "학습 데이터 수집"으로 되돌림
                self.ui.collect_data_button.setEnabled(True)

        elif "[UI_STATUS]" in msg.data:
            self.get_logger().info(f"ui_status 메시지 수신: {msg.data}")
            # 메시지 파싱 및 UI 업데이트
            parsed_status = self.parse_ui_status(msg.data)
            self.update_ui_buttons(parsed_status)
            self.setup_completed = True
        else:
            self.get_logger().warning(f"알 수 없는 메시지 형식: {msg.data}")

    def send_email(self, content):
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "******@*****.***"
        sender_password = "******"
        receiver_email = "******"  # 실제 받는 사람 이메일 주소로 변경
        subject = "STATUS Notification"

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(content, "plain"))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(message)
            print("이메일 전송 성공")
        except Exception as e:
            print(f"이메일 전송 실패: {e}")


    def enable_emergency_button(self):
        """비상 정지 버튼을 활성화."""
        if self.ui:
            self.ui.Emergency_button.setEnabled(True)
    #-------------------------------main_commend 메세지 처리 끝

    def update_job_time(self, data):
        """[JOB]time 메시지를 처리하여 UI에 작업 시간을 업데이트."""
        try:
            if "[JOB]time=" not in data:
                raise ValueError("메시지 형식이 올바르지 않습니다.")

            # 시간 정보 추출
            time_value = data.split("time=")[-1]
            self.current_job_time = time_value
            self.get_logger().info(f"작업 시간 업데이트: {time_value}")

            # UI 업데이트
            if self.ui:
                self.ui.processing_timer.setText(f"작업 소요 시간 - {time_value}")
        except Exception as e:
            self.get_logger().error(f"작업 시간 업데이트 중 오류 발생: {e}")

    #--------------------------------[SETUP] 시작
    def send_setup_message(self):
        """[SETUP]ui_node 메시지를 ui_commend 토픽으로 발행."""
        if self.ui_commend_publisher is not None:
            if not self.setup_completed:  # 플래그 확인
                self.get_logger().info("[SETUP]ui_node 메시지를 보내는 중...")
                msg = String()
                msg.data = "[SETUP]ui_node"
                self.ui_commend_publisher.publish(msg)
    #--------------------------------[SETUP] 끝

    #------------------------------ui_status 메시지 처리
    def parse_ui_status(self, data):
        try:
            if not data.startswith("[UI_STATUS]"):
                raise ValueError("메시지 형식이 올바르지 않습니다.")
            
            # [UI_STATUS] 제거 및 본문 추출
            content = data[len("[UI_STATUS] "):].strip()
            tuples = [item.strip() for item in content.split('), ') if item.strip()]

            ui_status = []
            for item in tuples:
                if item.endswith(')'):
                    item = item[:-1]  # 마지막 괄호 제거
                if '(' in item and ', ' in item:  # 유효성 검사
                    key, value, checked = item.strip('()').split(', ')
                    ui_status.append((key, value, checked))
            return ui_status

        except Exception as e:
            print(f"역직렬화 오류: {e}")
            return []
    
    def update_ui_buttons(self, button_status):
        """
        UI 버튼 상태를 업데이트.
        :param button_status: dict - 버튼 상태 정보
        """
        if not self.ui:
            self.get_logger().warning("UI 객체가 연결되지 않았습니다.")
            return

        for button_name, state, checked in button_status:
            if button_name == "conveyor_status":
                checkbox = getattr(self.ui, f"{button_name}_button", None)
                if checkbox:
                    checkbox.setEnabled(state == "활성화")
                    checkbox.setChecked(checked == "체크됨")
                    self.get_logger().info(f"{button_name} 체크박스 {'활성화' if state == '활성화' else '비활성화'}, {'체크됨' if checked == '체크됨' else '미체크'}")
            else:
                button = getattr(self.ui, f"{button_name}_button", None)
                if button:
                    button.setEnabled(state == "활성화")
                    self.get_logger().info(f"{button_name} 버튼 {'활성화' if state == '활성화' else '비활성화'}")
    #------------------------------ui_status 메시지 처리 끝

    def image_callback(self, msg):
        """CompressedImage 메시지를 처리하는 콜백."""
        try:
            # 압축된 이미지 데이터를 디코드
            np_arr = np.frombuffer(msg.data, np.uint8)
            image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            if image is not None:
                # OpenCV 이미지를 RGB로 변환
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                height, width, channel = image.shape
                bytes_per_line = 3 * width
                qt_image = QtGui.QImage(image.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap.fromImage(qt_image)
                # 시그널을 통해 GUI 업데이트
                if self.ui:
                    self.ui.signals.update_image.emit(pixmap)
            else:
                self.get_logger().warning("디코드된 이미지가 None입니다.")
        except Exception as e:
            self.get_logger().error(f"이미지 처리 중 오류 발생: {e}")



def run_ros_node(node):
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("ROS2 Node shutting down.")
    finally:
        rclpy.shutdown()

def run_ui():
    app = QtWidgets.QApplication(sys.argv)

    # ROS 초기화
    rclpy.init()

    # UINode 생성
    ui_node = UINode()

    # ROS 노드 별도 스레드에서 실행
    ros_thread = Thread(target=run_ros_node, args=(ui_node,), daemon=True)
    ros_thread.start()

    # 로그인 창 표시
    login_window = Login(ui_node)
    login_window.show()

    sys.exit(app.exec_())

def main(args=None):
    # PyQt UI는 메인 스레드에서 실행
    run_ui()

if __name__ == "__main__":
    main()
