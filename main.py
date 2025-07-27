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
            QPushButton#budgetBtn {
                background-color: #9b59b6;
            }
            QPushButton#budgetBtn:hover {
                background-color: #8e44ad;
            }
            QProgressBar {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 3px;
            }
            QProgressBar#budgetProgress::chunk {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #27ae60, stop: 0.5 #f39c12, stop: 1 #e74c3c);
            }
            QPushButton#exportBtn {
                background-color: #1abc9c;
            }
            QPushButton#exportBtn:hover {
                background-color: #16a085;
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
        
        # 优先级
        add_layout.addWidget(QLabel("优先级:"), 3, 0)
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["低", "中", "高", "必需"])
        add_layout.addWidget(self.priority_combo, 3, 1)
        
        # 类别
        add_layout.addWidget(QLabel("类别:"), 4, 0)
        self.category_combo = QComboBox()
        self.category_combo.addItems([
            "住房", "交通", "餐饮", "娱乐", "购物", "健康", 
            "教育", "投资", "其他"
        ])
        add_layout.addWidget(self.category_combo, 4, 1)
        
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
        
        # 预算进度
        self.budget_label = QLabel("预算目标: ¥0.00")
        self.budget_label.setFont(QFont("Arial", 10))
        stats_layout.addWidget(self.budget_label)
        
        self.budget_progress = QProgressBar()
        self.budget_progress.setObjectName("budgetProgress")
        self.budget_progress.setVisible(False)
        stats_layout.addWidget(self.budget_progress)
        
        layout.addWidget(stats_group)
        
        # 筛选和排序
        filter_group = QGroupBox("筛选和排序")
        filter_layout = QGridLayout(filter_group)
        
        filter_layout.addWidget(QLabel("类别:"), 0, 0)
        self.category_filter = QComboBox()
        self.category_filter.addItem("全部")
        self.category_filter.addItems([
            "住房", "交通", "餐饮", "娱乐", "购物", "健康", 
            "教育", "投资", "其他"
        ])
        self.category_filter.currentTextChanged.connect(self.filter_desires)
        filter_layout.addWidget(self.category_filter, 0, 1)
        
        filter_layout.addWidget(QLabel("优先级:"), 0, 2)
        self.priority_filter = QComboBox()
        self.priority_filter.addItem("全部")
        self.priority_filter.addItems(["低", "中", "高", "必需"])
        self.priority_filter.currentTextChanged.connect(self.filter_desires)
        filter_layout.addWidget(self.priority_filter, 0, 3)
        
        layout.addWidget(filter_group)
        
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
        
        budget_btn = QPushButton("设置预算")
        budget_btn.setObjectName("budgetBtn")
        budget_btn.clicked.connect(self.set_budget_goal)
        button_layout.addWidget(budget_btn)
        
        export_btn = QPushButton("导出报告")
        export_btn.setObjectName("exportBtn")
        export_btn.clicked.connect(self.export_report)
        button_layout.addWidget(export_btn)
        
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
        """设置预算目标"""
        try:
            budget_str, ok = QInputDialog.getText(self, "设置预算目标", 
                                                "请输入月度预算目标金额(元):")
            if ok and budget_str.strip():
                budget = float(budget_str.strip())
                if budget > 0:
                    self.budget_goal = budget
                    self.budget_label.setText(f"预算目标: ¥{budget:.2f}")
                    self.budget_progress.setVisible(True)
                    self.update_statistics()
                    QMessageBox.information(self, "成功", f"预算目标已设置为 ¥{budget:.2f}")
                else:
                    QMessageBox.warning(self, "错误", "预算必须大于0")
        except ValueError:
            QMessageBox.warning(self, "错误", "请输入有效的数字")
        
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
        
        # 名称和优先级
        name_layout = QHBoxLayout()
        name_label = QLabel(desire['name'])
        name_label.setFont(QFont("Arial", 10, QFont.Bold))
        
        priority = desire.get('priority', '中')  # 默认优先级为中
        priority_label = QLabel(f"[{priority}]")
        priority_label.setFont(QFont("Arial", 9))
        priority_colors = {
            "低": "#27ae60",
            "中": "#f39c12", 
            "高": "#e74c3c",
            "必需": "#8e44ad"
        }
        priority_label.setStyleSheet(f"color: {priority_colors.get(priority, '#2c3e50')}")
        
        name_layout.addWidget(name_label)
        name_layout.addWidget(priority_label)
        name_layout.addStretch()
        
        info_layout.addLayout(name_layout)
        
        # 详细信息
        details_label = QLabel(
            f"{desire['frequency']} ¥{desire['cost']:.2f} | {desire['category']}"
        )
        details_label.setFont(QFont("Arial", 9))
        
        if not desire['enabled']:
            name_label.setStyleSheet("color: #95a5a6;")
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