#!/usr/bin/env python3
"""
PyQt5测试脚本
"""

import sys

try:
    from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QFont
    
    print("✓ PyQt5导入成功")
    
    class TestWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("PyQt5测试")
            self.setGeometry(100, 100, 400, 200)
            
            # 设置黑色文字
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #f8f9fa;
                }
                QLabel {
                    color: #000000;
                    font-size: 16px;
                    font-weight: bold;
                }
            """)
            
            label = QLabel("PyQt5测试成功！\n文字应该是黑色的")
            label.setAlignment(Qt.AlignCenter)
            label.setFont(QFont("Arial", 16, QFont.Bold))
            self.setCentralWidget(label)
    
    def main():
        app = QApplication(sys.argv)
        window = TestWindow()
        window.show()
        sys.exit(app.exec_())
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"✗ PyQt5导入失败: {e}")
    print("请运行: pip3 install PyQt5")
except Exception as e:
    print(f"✗ 其他错误: {e}") 