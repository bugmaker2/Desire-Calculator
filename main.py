#!/usr/bin/env python3
"""
需求计算器 - PyQt5版本
Desire Calculator with PyQt5
"""

import sys
import json
import os
from datetime import datetime
from typing import Dict, Any
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QPushButton, QCheckBox,
    QListWidget, QListWidgetItem, QMessageBox, QFileDialog,
    QFrame, QGroupBox, QGridLayout, QSplitter, QScrollArea
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPalette, QColor

class DesireCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.desires = {}
        self.init_ui()
        self.load_desires()
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("需求计算器 - Desire Calculator")
        self.setGeometry(100, 100, 1000, 700)
        self.setMinimumSize(800, 600)
        
        # 设置样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QPushButton#deleteBtn {
                background-color: #e74c3c;
                min-width: 30px;
                max-width: 30px;
            }
            QPushButton#deleteBtn:hover {
                background-color: #c0392b;
            }
            QPushButton#saveBtn {
                background-color: #27ae60;
            }
            QPushButton#saveBtn:hover {
                background-color: #229954;
            }
            QPushButton#loadBtn {
                background-color: #f39c12;
            }
            QPushButton#loadBtn:hover {
                background-color: #e67e22;
            }
            QPushButton#clearBtn {
                background-color: #e74c3c;
            }
            QPushButton#clearBtn:hover {
                background-color: #c0392b;
            }
            QLineEdit, QComboBox {
                padding: 6px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: white;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #3498db;
            }
            QLabel {
                color: #2c3e50;
            }
            QListWidget {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: white;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #ecf0f1;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout(central_widget)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # 左侧面板 - 添加需求
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # 右侧面板 - 需求列表和统计
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # 设置分割器比例
        splitter.setSizes([300, 700])
        
    def create_left_panel(self):
        """创建左侧面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # 标题
        title = QLabel("添加新需求")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 添加需求组
        add_group = QGroupBox("需求信息")
        add_layout = QGridLayout(add_group)
        
        # 需求名称
        add_layout.addWidget(QLabel("需求名称:"), 0, 0)
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("例如：房屋月租")
        add_layout.addWidget(self.name_edit, 0, 1)
        
        # 频率选择
        add_layout.addWidget(QLabel("频率:"), 1, 0)
        self.freq_combo = QComboBox()
        self.freq_combo.addItems(["每天", "每周", "每月", "每季度", "每年"])
        add_layout.addWidget(self.freq_combo, 1, 1)
        
        # 花销输入
        add_layout.addWidget(QLabel("花销(元):"), 2, 0)
        self.cost_edit = QLineEdit()
        self.cost_edit.setPlaceholderText("例如：3000")
        add_layout.addWidget(self.cost_edit, 2, 1)
        
        layout.addWidget(add_group)
        
        # 添加按钮
        add_btn = QPushButton("添加需求")
        add_btn.clicked.connect(self.add_desire)
        layout.addWidget(add_btn)
        
        layout.addStretch()
        return panel
        
    def create_right_panel(self):
        """创建右侧面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # 标题
        title = QLabel("需求列表")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 需求列表
        self.desire_list = QListWidget()
        layout.addWidget(self.desire_list)
        
        # 统计信息组
        stats_group = QGroupBox("花销统计")
        stats_layout = QVBoxLayout(stats_group)
        
        self.monthly_label = QLabel("月度总花销: ¥0.00")
        self.monthly_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.monthly_label.setStyleSheet("color: #e74c3c;")
        stats_layout.addWidget(self.monthly_label)
        
        self.yearly_label = QLabel("年度总花销: ¥0.00")
        self.yearly_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.yearly_label.setStyleSheet("color: #e74c3c;")
        stats_layout.addWidget(self.yearly_label)
        
        layout.addWidget(stats_group)
        
        # 操作按钮
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("保存数据")
        save_btn.setObjectName("saveBtn")
        save_btn.clicked.connect(self.save_desires)
        button_layout.addWidget(save_btn)
        
        load_btn = QPushButton("加载数据")
        load_btn.setObjectName("loadBtn")
        load_btn.clicked.connect(self.load_desires)
        button_layout.addWidget(load_btn)
        
        clear_btn = QPushButton("清空所有")
        clear_btn.setObjectName("clearBtn")
        clear_btn.clicked.connect(self.clear_all)
        button_layout.addWidget(clear_btn)
        
        layout.addLayout(button_layout)
        return panel
        
    def add_desire(self):
        """添加新需求"""
        name = self.name_edit.text().strip()
        frequency = self.freq_combo.currentText()
        cost_str = self.cost_edit.text().strip()
        
        if not name:
            QMessageBox.warning(self, "错误", "请输入需求名称")
            return
            
        if not cost_str:
            QMessageBox.warning(self, "错误", "请输入花销金额")
            return
            
        try:
            cost = float(cost_str)
            if cost <= 0:
                QMessageBox.warning(self, "错误", "花销必须大于0")
                return
        except ValueError:
            QMessageBox.warning(self, "错误", "请输入有效的数字")
            return
            
        # 生成唯一ID
        desire_id = f"desire_{len(self.desires)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.desires[desire_id] = {
            'name': name,
            'frequency': frequency,
            'cost': cost,
            'enabled': True
        }
        
        # 清空输入框
        self.name_edit.clear()
        self.cost_edit.clear()
        
        # 更新显示
        self.update_display()
        
        QMessageBox.information(self, "成功", f"已添加需求: {name}")
        
    def update_display(self):
        """更新需求列表显示"""
        self.desire_list.clear()
        
        for desire_id, desire in self.desires.items():
            item_widget = self.create_desire_item(desire_id, desire)
            list_item = QListWidgetItem()
            list_item.setSizeHint(item_widget.sizeHint())
            self.desire_list.addItem(list_item)
            self.desire_list.setItemWidget(list_item, item_widget)
            
        self.update_statistics()
        
    def create_desire_item(self, desire_id, desire):
        """创建单个需求项"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # 启用复选框
        enabled_cb = QCheckBox()
        enabled_cb.setChecked(desire['enabled'])
        enabled_cb.toggled.connect(lambda checked, did=desire_id: self.toggle_desire(did, checked))
        layout.addWidget(enabled_cb)
        
        # 需求信息
        info_layout = QVBoxLayout()
        
        name_label = QLabel(desire['name'])
        name_label.setFont(QFont("Arial", 10, QFont.Bold))
        if not desire['enabled']:
            name_label.setStyleSheet("color: #95a5a6;")
        info_layout.addWidget(name_label)
        
        details_label = QLabel(f"{desire['frequency']} ¥{desire['cost']:.2f}")
        if not desire['enabled']:
            details_label.setStyleSheet("color: #bdc3c7;")
        info_layout.addWidget(details_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        # 删除按钮
        delete_btn = QPushButton("×")
        delete_btn.setObjectName("deleteBtn")
        delete_btn.clicked.connect(lambda: self.delete_desire(desire_id))
        layout.addWidget(delete_btn)
        
        return widget
        
    def toggle_desire(self, desire_id, enabled):
        """切换需求状态"""
        if desire_id in self.desires:
            self.desires[desire_id]['enabled'] = enabled
            self.update_display()
            
    def delete_desire(self, desire_id):
        """删除需求"""
        if desire_id in self.desires:
            name = self.desires[desire_id]['name']
            reply = QMessageBox.question(
                self, "确认删除", 
                f"确定要删除需求 '{name}' 吗？",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                del self.desires[desire_id]
                self.update_display()
                
    def update_statistics(self):
        """更新统计信息"""
        monthly_total = 0
        
        for desire in self.desires.values():
            if not desire['enabled']:
                continue
                
            cost = desire['cost']
            frequency = desire['frequency']
            
            # 计算月度花销
            if frequency == "每天":
                monthly_cost = cost * 30
            elif frequency == "每周":
                monthly_cost = cost * 4.33  # 52/12
            elif frequency == "每月":
                monthly_cost = cost
            elif frequency == "每季度":
                monthly_cost = cost / 3
            elif frequency == "每年":
                monthly_cost = cost / 12
            else:
                monthly_cost = 0
                
            monthly_total += monthly_cost
            
        yearly_total = monthly_total * 12
        
        # 更新显示
        self.monthly_label.setText(f"月度总花销: ¥{monthly_total:.2f}")
        self.yearly_label.setText(f"年度总花销: ¥{yearly_total:.2f}")
        
    def save_desires(self):
        """保存需求数据"""
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self, "保存数据", "desires.json", "JSON Files (*.json)"
            )
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.desires, f, ensure_ascii=False, indent=2)
                QMessageBox.information(self, "成功", f"数据已保存到 {filename}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存失败: {str(e)}")
            
    def load_desires(self):
        """加载需求数据"""
        try:
            filename, _ = QFileDialog.getOpenFileName(
                self, "加载数据", "", "JSON Files (*.json)"
            )
            if filename:
                with open(filename, 'r', encoding='utf-8') as f:
                    self.desires = json.load(f)
                self.update_display()
                QMessageBox.information(self, "成功", f"数据已从 {filename} 加载")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载失败: {str(e)}")
            
    def clear_all(self):
        """清空所有需求"""
        reply = QMessageBox.question(
            self, "确认清空", 
            "确定要清空所有需求吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.desires = {}
            self.update_display()

def main():
    app = QApplication(sys.argv)
    
    # 设置应用信息
    app.setApplicationName("需求计算器")
    app.setApplicationVersion("1.0")
    app.setApplicationDisplayName("需求计算器")
    
    # 创建主窗口
    window = DesireCalculator()
    window.show()
    
    # 运行应用
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()