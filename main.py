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
    QListWidget, QListWidgetItem, QMessageBox, QFileDialog, QInputDialog,
    QFrame, QGroupBox, QGridLayout, QSplitter, QScrollArea,
    QProgressBar, QTabWidget, QTextEdit, QSpinBox, QDoubleSpinBox
)
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor

class DesireCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.desires = {}
        self.budget_goal = 0
        self.init_ui()
        self.load_desires()
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("Desire Calculator")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(900, 650)
        
        # 现代主题
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QWidget {
                font-family: 'SF Pro Display', 'Segoe UI', 'Helvetica Neue', sans-serif;
                font-size: 14px;
                color: #000000;
            }
            QLabel {
                color: #000000;
            }
            QLineEdit {
                color: #000000;
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
                background-color: white;
                color: #000000;
            }
            QComboBox {
                color: #000000;
                background-color: white;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
            }
            QComboBox:focus {
                border: 2px solid #667eea;
                background-color: white;
                color: #000000;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #000000;
                margin-right: 8px;
            }
            QGroupBox {
                font-weight: 600;
                font-size: 16px;
                border: none;
                border-radius: 12px;
                background-color: white;
                padding: 24px;
                margin-top: 8px;
                box-shadow: 0 2px 20px rgba(0, 0, 0, 0.08);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 0 16px 0;
                color: #000000;
            }
            QPushButton {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 14px;
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            }
            QPushButton:hover {
                background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
            }
            QPushButton:pressed {
                background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
                box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
            }
            QPushButton#deleteBtn {
                background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
                box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3);
                min-width: 36px;
                max-width: 36px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton#deleteBtn:hover {
                background: linear-gradient(135deg, #ee5a52 0%, #ff6b6b 100%);
                box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4);
            }
            QPushButton#saveBtn {
                background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
                box-shadow: 0 4px 12px rgba(72, 187, 120, 0.3);
            }
            QPushButton#saveBtn:hover {
                background: linear-gradient(135deg, #38a169 0%, #48bb78 100%);
                box-shadow: 0 6px 20px rgba(72, 187, 120, 0.4);
            }
            QPushButton#loadBtn {
                background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);
                box-shadow: 0 4px 12px rgba(237, 137, 54, 0.3);
            }
            QPushButton#loadBtn:hover {
                background: linear-gradient(135deg, #dd6b20 0%, #ed8936 100%);
                box-shadow: 0 6px 20px rgba(237, 137, 54, 0.4);
            }
            QPushButton#clearBtn {
                background: linear-gradient(135deg, #e53e3e 0%, #c53030 100%);
                box-shadow: 0 4px 12px rgba(229, 62, 62, 0.3);
            }
            QPushButton#clearBtn:hover {
                background: linear-gradient(135deg, #c53030 0%, #e53e3e 100%);
                box-shadow: 0 6px 20px rgba(229, 62, 62, 0.4);
            }
            QPushButton#budgetBtn {
                background: linear-gradient(135deg, #805ad5 0%, #6b46c1 100%);
                box-shadow: 0 4px 12px rgba(128, 90, 213, 0.3);
            }
            QPushButton#budgetBtn:hover {
                background: linear-gradient(135deg, #6b46c1 0%, #805ad5 100%);
                box-shadow: 0 6px 20px rgba(128, 90, 213, 0.4);
            }
            QPushButton#exportBtn {
                background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
                box-shadow: 0 4px 12px rgba(66, 153, 225, 0.3);
            }
            QPushButton#exportBtn:hover {
                background: linear-gradient(135deg, #3182ce 0%, #4299e1 100%);
                box-shadow: 0 6px 20px rgba(66, 153, 225, 0.4);
            }
            QProgressBar {
                border: none;
                border-radius: 8px;
                background-color: #e2e8f0;
                text-align: center;
                height: 12px;
                color: #000000;
            }
            QProgressBar::chunk {
                border-radius: 8px;
                background: linear-gradient(90deg, #48bb78 0%, #38a169 100%);
            }
            QProgressBar#budgetProgress::chunk {
                background: linear-gradient(90deg, #48bb78 0%, #ed8936 50%, #e53e3e 100%);
            }
            QLineEdit, QComboBox {
                padding: 12px 16px;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background-color: #ffffff;
                font-size: 14px;
                color: #000000;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
                outline: none;
                color: #000000;
            }
            QLabel {
                color: #000000;
                font-weight: 500;
            }
            QListWidget {
                border: none;
                border-radius: 12px;
                background-color: white;
                box-shadow: 0 2px 20px rgba(0, 0, 0, 0.08);
                color: #000000;
            }
            QListWidget::item {
                padding: 16px;
                border-bottom: 1px solid #f1f5f9;
                border-radius: 0;
                color: #000000;
            }
            QListWidget::item:selected {
                background-color: #f7fafc;
                color: #000000;
                border-left: 4px solid #667eea;
            }
            QListWidget::item:hover {
                background-color: #f8f9fa;
                color: #000000;
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
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 现代标题
        title = QLabel("Add New Desire")
        title.setFont(QFont("SF Pro Display", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #000000 !important; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # 添加需求组 - 现代卡片设计
        add_group = QGroupBox()
        add_group.setStyleSheet("""
            QGroupBox {
                font-weight: 600;
                font-size: 16px;
                border: none;
                border-radius: 16px;
                background-color: white;
                padding: 32px;
                margin-top: 0px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            }
        """)
        
        add_layout = QVBoxLayout(add_group)
        add_layout.setSpacing(20)
        
        # 需求名称
        name_label = QLabel("Desire Name")
        name_label.setFont(QFont("SF Pro Display", 12, QFont.Medium))
        name_label.setStyleSheet("color: #000000; margin-bottom: 8px;")
        add_layout.addWidget(name_label)
        
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("e.g., Monthly Rent")
        add_layout.addWidget(self.name_edit)
        
        # 频率和花销在同一行
        freq_cost_layout = QHBoxLayout()
        freq_cost_layout.setSpacing(16)
        
        # 频率
        freq_container = QVBoxLayout()
        freq_label = QLabel("Frequency")
        freq_label.setFont(QFont("SF Pro Display", 12, QFont.Medium))
        freq_label.setStyleSheet("color: #000000; margin-bottom: 8px;")
        freq_container.addWidget(freq_label)
        
        self.freq_combo = QComboBox()
        self.freq_combo.addItems(["Daily", "Weekly", "Monthly", "Quarterly", "Yearly"])
        freq_container.addWidget(self.freq_combo)
        freq_cost_layout.addLayout(freq_container)
        
        # 花销
        cost_container = QVBoxLayout()
        cost_label = QLabel("Cost (¥)")
        cost_label.setFont(QFont("SF Pro Display", 12, QFont.Medium))
        cost_label.setStyleSheet("color: #000000; margin-bottom: 8px;")
        cost_container.addWidget(cost_label)
        
        self.cost_edit = QLineEdit()
        self.cost_edit.setPlaceholderText("e.g., 3000")
        cost_container.addWidget(self.cost_edit)
        freq_cost_layout.addLayout(cost_container)
        
        add_layout.addLayout(freq_cost_layout)
        
        # 优先级和类别在同一行
        priority_category_layout = QHBoxLayout()
        priority_category_layout.setSpacing(16)
        
        # 优先级
        priority_container = QVBoxLayout()
        priority_label = QLabel("Priority")
        priority_label.setFont(QFont("SF Pro Display", 12, QFont.Medium))
        priority_label.setStyleSheet("color: #000000; margin-bottom: 8px;")
        priority_container.addWidget(priority_label)
        
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["Low", "Medium", "High", "Essential"])
        priority_container.addWidget(self.priority_combo)
        priority_category_layout.addLayout(priority_container)
        
        # 类别
        category_container = QVBoxLayout()
        category_label = QLabel("Category")
        category_label.setFont(QFont("SF Pro Display", 12, QFont.Medium))
        category_label.setStyleSheet("color: #000000; margin-bottom: 8px;")
        category_container.addWidget(category_label)
        
        self.category_combo = QComboBox()
        self.category_combo.addItems([
            "Housing", "Transport", "Food", "Entertainment", "Shopping", "Health",
            "Education", "Investment", "Other"
        ])
        category_container.addWidget(self.category_combo)
        priority_category_layout.addLayout(category_container)
        
        add_layout.addLayout(priority_category_layout)
        layout.addWidget(add_group)
        
        # 现代添加按钮
        add_btn = QPushButton("✨ Add Desire")
        add_btn.setFont(QFont("SF Pro Display", 14, QFont.Bold))
        add_btn.clicked.connect(self.add_desire)
        layout.addWidget(add_btn)
        
        layout.addStretch()
        return panel
        
    def create_right_panel(self):
        """创建右侧面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 现代标题
        title = QLabel("Your Desires")
        title.setFont(QFont("SF Pro Display", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #000000 !important; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # 筛选组 - 现代化
        filter_group = QGroupBox()
        filter_group.setStyleSheet("""
            QGroupBox {
                font-weight: 600;
                font-size: 16px;
                border: none;
                border-radius: 16px;
                background-color: white;
                padding: 20px;
                margin-top: 0px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            }
        """)
        
        filter_layout = QHBoxLayout(filter_group)
        filter_layout.setSpacing(16)
        
        # 类别筛选
        category_container = QVBoxLayout()
        category_label = QLabel("Category")
        category_label.setFont(QFont("SF Pro Display", 12, QFont.Medium))
        category_label.setStyleSheet("color: #000000; margin-bottom: 8px;")
        category_container.addWidget(category_label)
        
        self.category_filter = QComboBox()
        self.category_filter.addItem("All")
        self.category_filter.addItems([
            "Housing", "Transport", "Food", "Entertainment", "Shopping", "Health",
            "Education", "Investment", "Other"
        ])
        self.category_filter.currentTextChanged.connect(self.filter_desires)
        category_container.addWidget(self.category_filter)
        filter_layout.addLayout(category_container)
        
        # 优先级筛选
        priority_container = QVBoxLayout()
        priority_label = QLabel("Priority")
        priority_label.setFont(QFont("SF Pro Display", 12, QFont.Medium))
        priority_label.setStyleSheet("color: #000000; margin-bottom: 8px;")
        priority_container.addWidget(priority_label)
        
        self.priority_filter = QComboBox()
        self.priority_filter.addItem("All")
        self.priority_filter.addItems(["Low", "Medium", "High", "Essential"])
        self.priority_filter.currentTextChanged.connect(self.filter_desires)
        priority_container.addWidget(self.priority_filter)
        filter_layout.addLayout(priority_container)
        
        layout.addWidget(filter_group)
        
        # 需求列表 - 现代卡片
        self.desire_list = QListWidget()
        self.desire_list.setStyleSheet("""
            QListWidget {
                border: none;
                border-radius: 16px;
                background-color: white;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            }
        """)
        layout.addWidget(self.desire_list)
        
        # 统计信息组 - 现代卡片
        stats_group = QGroupBox()
        stats_group.setStyleSheet("""
            QGroupBox {
                font-weight: 600;
                font-size: 16px;
                border: none;
                border-radius: 16px;
                background-color: white;
                padding: 24px;
                margin-top: 0px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            }
        """)
        
        stats_layout = QVBoxLayout(stats_group)
        stats_layout.setSpacing(16)
        
        # 现代统计标签
        self.monthly_label = QLabel("Monthly Total: ¥0.00")
        self.monthly_label.setFont(QFont("SF Pro Display", 16, QFont.Bold))
        self.monthly_label.setStyleSheet("color: #000000;")
        stats_layout.addWidget(self.monthly_label)
        
        self.yearly_label = QLabel("Yearly Total: ¥0.00")
        self.yearly_label.setFont(QFont("SF Pro Display", 16, QFont.Bold))
        self.yearly_label.setStyleSheet("color: #000000;")
        stats_layout.addWidget(self.yearly_label)
        
        # 预算进度
        self.budget_label = QLabel("Budget: Not Set")
        self.budget_label.setFont(QFont("SF Pro Display", 14))
        self.budget_label.setAlignment(Qt.AlignCenter)
        self.budget_label.setStyleSheet("color: #000000;")
        stats_layout.addWidget(self.budget_label)
        
        self.budget_progress = QProgressBar()
        self.budget_progress.setObjectName("budgetProgress")
        self.budget_progress.setVisible(False)
        self.budget_progress.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 8px;
                background-color: #e2e8f0;
                text-align: center;
                height: 12px;
            }
            QProgressBar::chunk {
                border-radius: 8px;
                background: linear-gradient(90deg, #48bb78 0%, #38a169 100%);
            }
        """)
        stats_layout.addWidget(self.budget_progress)
        
        layout.addWidget(stats_group)
        
        # 现代按钮组
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        save_btn = QPushButton("💾 Save")
        save_btn.setObjectName("saveBtn")
        save_btn.clicked.connect(self.save_desires)
        button_layout.addWidget(save_btn)
        
        # 黑色字
        load_btn = QPushButton("📁 Load")
        load_btn.setObjectName("loadBtn")
        load_btn.clicked.connect(self.load_desires)
        button_layout.addWidget(load_btn)
        
        budget_btn = QPushButton("💰 Budget")
        budget_btn.setObjectName("budgetBtn")
        budget_btn.clicked.connect(self.set_budget_goal)
        button_layout.addWidget(budget_btn)
        
        export_btn = QPushButton("📊 Export")
        export_btn.setObjectName("exportBtn")
        export_btn.clicked.connect(self.export_report)
        button_layout.addWidget(export_btn)
        
        clear_btn = QPushButton("🗑️ Clear All")
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
        priority = self.priority_combo.currentText()
        category = self.category_combo.currentText()
        
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
            'priority': priority,
            'category': category,
            'enabled': True
        }
        
        # 清空输入框
        self.name_edit.clear()
        self.cost_edit.clear()
        
        # 更新显示
        self.update_display()
        
        QMessageBox.information(self, "成功", f"已添加需求: {name}")
        
    def set_budget_goal(self):
        """Set budget goal"""
        try:
            budget_str, ok = QInputDialog.getText(self, "Set Budget Goal", 
                                                "Enter your monthly budget (¥):")
            if ok and budget_str.strip():
                budget = float(budget_str.strip())
                if budget > 0:
                    self.budget_goal = budget
                    self.budget_label.setText(f"Budget: ¥{budget:.2f}")
                    self.budget_progress.setVisible(True)
                    self.update_statistics()
                    QMessageBox.information(self, "Success", f"Budget set to ¥{budget:.2f}")
                else:
                    QMessageBox.warning(self, "Error", "Budget must be greater than 0")
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a valid number")
        
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
        """创建单个需求项（现代化）"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        # 启用复选框
        enabled_cb = QCheckBox()
        enabled_cb.setChecked(desire['enabled'])
        enabled_cb.toggled.connect(lambda checked, did=desire_id: self.toggle_desire(did, checked))
        enabled_cb.setStyleSheet("""
            QCheckBox {
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 2px solid #e2e8f0;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                background-color: #667eea;
                border-color: #667eea;
            }
        """)
        layout.addWidget(enabled_cb)
        
        # 需求信息
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        # 名称和优先级
        name_layout = QHBoxLayout()
        name_layout.setSpacing(8)
        
        name_label = QLabel(desire['name'])
        name_label.setFont(QFont("SF Pro Display", 14, QFont.Bold))
        
        priority = desire.get('priority', 'Medium')
        priority_colors = {
            "Low": "#48bb78",
            "Medium": "#ed8936", 
            "High": "#e53e3e",
            "Essential": "#805ad5"
        }
        priority_label = QLabel(priority)
        priority_label.setFont(QFont("SF Pro Display", 11, QFont.Bold))
        priority_label.setStyleSheet(f"""
            background-color: {priority_colors.get(priority, '#667eea')}; 
            color: white; 
            padding: 4px 12px; 
            border-radius: 12px;
            font-size: 11px;
        """)
        
        name_layout.addWidget(name_label)
        name_layout.addWidget(priority_label)
        name_layout.addStretch()
        
        info_layout.addLayout(name_layout)
        
        # 详细信息
        details_label = QLabel(
            f"{desire['frequency']} • ¥{desire['cost']:.2f} • {desire['category']}"
        )
        details_label.setFont(QFont("SF Pro Display", 12))
        details_label.setStyleSheet("color: #000000;")
        
        if not desire['enabled']:
            name_label.setStyleSheet("color: #666666; text-decoration: line-through;")
            details_label.setStyleSheet("color: #666666; text-decoration: line-through;")
        
        info_layout.addWidget(details_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        # 删除按钮
        delete_btn = QPushButton("✕")
        delete_btn.setObjectName("deleteBtn")
        delete_btn.clicked.connect(lambda: self.delete_desire(desire_id))
        layout.addWidget(delete_btn)
        
        return widget
        
    def toggle_desire(self, desire_id, enabled):
        """切换需求状态"""
        if desire_id in self.desires:
            self.desires[desire_id]['enabled'] = enabled
            self.update_display()
            
    def filter_desires(self):
        """根据筛选条件显示需求"""
        category_filter = self.category_filter.currentText()
        priority_filter = self.priority_filter.currentText()
        
        self.desire_list.clear()
        
        for desire_id, desire in self.desires.items():
            # 应用筛选条件
            if category_filter != "全部" and desire['category'] != category_filter:
                continue
            if priority_filter != "全部" and desire['priority'] != priority_filter:
                continue
                
            item_widget = self.create_desire_item(desire_id, desire)
            list_item = QListWidgetItem()
            list_item.setSizeHint(item_widget.sizeHint())
            self.desire_list.addItem(list_item)
            self.desire_list.setItemWidget(list_item, item_widget)
            
        self.update_statistics()
        
    def export_report(self):
        """导出详细报告"""
        try:
            if not self.desires:
                QMessageBox.warning(self, "警告", "没有可导出的数据")
                return
                
            filename, _ = QFileDialog.getSaveFileName(
                self, "导出报告", f"desire_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", 
                "Text Files (*.txt)"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("需求计算器详细报告\n")
                    f.write("=" * 50 + "\n\n")
                    
                    # 总体统计
                    monthly_total = 0
                    yearly_total = 0
                    category_totals = {}
                    priority_counts = {"低": 0, "中": 0, "高": 0, "必需": 0}
                    
                    # 计算统计
                    for desire in self.desires.values():
                        if not desire['enabled']:
                            continue
                            
                        cost = desire['cost']
                        frequency = desire['frequency']
                        category = desire['category']
                        priority = desire['priority']
                        
                        # 计算月度花销
                        if frequency == "每天":
                            monthly_cost = cost * 30
                        elif frequency == "每周":
                            monthly_cost = cost * 4.33
                        elif frequency == "每月":
                            monthly_cost = cost
                        elif frequency == "每季度":
                            monthly_cost = cost / 3
                        elif frequency == "每年":
                            monthly_cost = cost / 12
                        else:
                            monthly_cost = 0
                            
                        monthly_total += monthly_cost
                        
                        if category not in category_totals:
                            category_totals[category] = 0
                        category_totals[category] += monthly_cost
                        
                        if priority in priority_counts:
                            priority_counts[priority] += 1
                    
                    yearly_total = monthly_total * 12
                    
                    # 写入报告
                    f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    
                    f.write("【总体统计】\n")
                    f.write(f"月度总花销: ¥{monthly_total:.2f}\n")
                    f.write(f"年度总花销: ¥{yearly_total:.2f}\n")
                    if self.budget_goal > 0:
                        f.write(f"预算目标: ¥{self.budget_goal:.2f}\n")
                        f.write(f"预算使用率: {min(100, int((monthly_total / self.budget_goal) * 100))}%\n")
                    f.write("\n")
                    
                    f.write("【按类别统计】\n")
                    for category, total in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
                        f.write(f"{category}: ¥{total:.2f}\n")
                    f.write("\n")
                    
                    f.write("【按优先级统计】\n")
                    for priority, count in priority_counts.items():
                        f.write(f"{priority}优先级: {count}个需求\n")
                    f.write("\n")
                    
                    f.write("【详细需求列表】\n")
                    for desire_id, desire in sorted(self.desires.items(), 
                                                   key=lambda x: x[1]['priority']):
                        status = "启用" if desire['enabled'] else "禁用"
                        frequency = desire['frequency']
                        cost = desire['cost']
                        
                        # 计算月度花销
                        if frequency == "每天":
                            monthly_cost = cost * 30
                        elif frequency == "每周":
                            monthly_cost = cost * 4.33
                        elif frequency == "每月":
                            monthly_cost = cost
                        elif frequency == "每季度":
                            monthly_cost = cost / 3
                        elif frequency == "每年":
                            monthly_cost = cost / 12
                        else:
                            monthly_cost = 0
                            
                        f.write(f"- {desire['name']} ({status})\n")
                        f.write(f"  频率: {frequency}\n")
                        f.write(f"  单次花销: ¥{cost:.2f}\n")
                        f.write(f"  月度花销: ¥{monthly_cost:.2f}\n")
                        f.write(f"  优先级: {desire['priority']}\n")
                        f.write(f"  类别: {desire['category']}\n")
                        f.write("\n")
                
                QMessageBox.information(self, "成功", f"报告已导出到: {filename}")
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导出失败: {str(e)}")
        
    def update_display(self):
        """更新需求列表显示"""
        self.filter_desires()
            
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
        
        # 按类别统计
        category_totals = {}
        priority_counts = {"低": 0, "中": 0, "高": 0, "必需": 0}
        
        for desire in self.desires.values():
            if not desire['enabled']:
                continue
                
            cost = desire['cost']
            frequency = desire['frequency']
            category = desire['category']
            priority = desire['priority']
            
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
            
            # 按类别累计
            if category not in category_totals:
                category_totals[category] = 0
            category_totals[category] += monthly_cost
            
            # 按优先级计数
            if priority in priority_counts:
                priority_counts[priority] += 1
        
        yearly_total = monthly_total * 12
        
        # 更新显示
        self.monthly_label.setText(f"月度总花销: ¥{monthly_total:.2f}")
        self.yearly_label.setText(f"年度总花销: ¥{yearly_total:.2f}")
        
        # 更新预算进度
        if self.budget_goal > 0:
            budget_percentage = min(100, int((monthly_total / self.budget_goal) * 100))
            self.budget_progress.setValue(budget_percentage)
            self.budget_progress.setFormat(f"{budget_percentage}% ({monthly_total:.0f}/¥{self.budget_goal:.0f})")
            
            # 根据进度设置颜色
            if budget_percentage <= 80:
                self.budget_progress.setStyleSheet("QProgressBar::chunk { background-color: #27ae60; }")
            elif budget_percentage <= 100:
                self.budget_progress.setStyleSheet("QProgressBar::chunk { background-color: #f39c12; }")
            else:
                self.budget_progress.setStyleSheet("QProgressBar::chunk { background-color: #e74c3c; }")
        
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
                    loaded_data = json.load(f)
                    
                # 验证并修复数据结构
                for desire_id, desire in loaded_data.items():
                    if isinstance(desire, dict):
                        # 确保所有必需的键都存在
                        if 'priority' not in desire:
                            desire['priority'] = '中'
                        if 'enabled' not in desire:
                            desire['enabled'] = True
                        if 'category' not in desire:
                            desire['category'] = '其他'
                
                self.desires = loaded_data
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