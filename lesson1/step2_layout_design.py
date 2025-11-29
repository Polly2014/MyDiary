"""
第二步：界面布局设计
目标：学习PyQt6的布局管理和常用组件
"""

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
import sys


class MyDiaryApp(QMainWindow):
    """我的日记应用 - 布局设计"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("MyDiary - 布局设计")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中心widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局（垂直布局）
        main_layout = QVBoxLayout()
        
        # === 标题区域 ===
        title_layout = QHBoxLayout()
        title_label = QLabel("标题:")
        title_label.setMinimumWidth(60)
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("请输入日记标题...")
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.title_edit)
        main_layout.addLayout(title_layout)
        
        # === 内容区域 ===
        content_label = QLabel("内容:")
        main_layout.addWidget(content_label)
        
        self.content_edit = QTextEdit()
        self.content_edit.setPlaceholderText("今天发生了什么有趣的事情？写下来吧...")
        main_layout.addWidget(self.content_edit)
        
        # === 按钮区域 ===
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 保存")
        save_btn.setMinimumHeight(40)
        save_btn.clicked.connect(self.save_diary)
        
        clear_btn = QPushButton("🗑️ 清空")
        clear_btn.setMinimumHeight(40)
        clear_btn.clicked.connect(self.clear_content)
        
        exit_btn = QPushButton("❌ 退出")
        exit_btn.setMinimumHeight(40)
        exit_btn.clicked.connect(self.close)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(clear_btn)
        button_layout.addWidget(exit_btn)
        
        main_layout.addLayout(button_layout)
        
        # 设置布局
        central_widget.setLayout(main_layout)
        
        # 设置样式
        self.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #34495e;
            }
            QLineEdit, QTextEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 13px;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #3498db;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
    
    def save_diary(self):
        """保存日记（暂时只是显示消息）"""
        title = self.title_edit.text()
        content = self.content_edit.toPlainText()
        
        # 验证输入
        if not title.strip():
            QMessageBox.warning(self, "警告", "请输入日记标题！")
            self.title_edit.setFocus()
            return
        
        if not content.strip():
            QMessageBox.warning(self, "警告", "请输入日记内容！")
            self.content_edit.setFocus()
            return
        
        # 显示成功消息
        word_count = len(content)
        QMessageBox.information(
            self, 
            "保存成功", 
            f"日记已保存！\n\n标题: {title}\n字数: {word_count}"
        )
        
        # 清空输入框
        self.clear_content()
    
    def clear_content(self):
        """清空内容"""
        reply = QMessageBox.question(
            self,
            "确认清空",
            "确定要清空所有内容吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.title_edit.clear()
            self.content_edit.clear()
            self.title_edit.setFocus()


def main():
    """主函数"""
    app = QApplication(sys.argv)
    window = MyDiaryApp()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()


"""
知识点总结：
1. 布局管理器:
   - QVBoxLayout: 垂直布局，组件从上到下排列
   - QHBoxLayout: 水平布局，组件从左到右排列
   - addWidget(): 添加组件到布局
   - addLayout(): 添加子布局到父布局

2. 常用组件:
   - QLabel: 文本标签
   - QLineEdit: 单行文本输入框
   - QTextEdit: 多行文本编辑器
   - QPushButton: 按钮

3. 信号与槽:
   - clicked.connect(): 连接按钮点击信号到槽函数
   - 槽函数：响应信号的普通Python方法

4. 消息框:
   - QMessageBox.warning(): 警告消息
   - QMessageBox.information(): 信息消息
   - QMessageBox.question(): 询问消息

5. 样式表:
   - setStyleSheet(): 使用CSS样式美化界面
   - 支持伪类选择器如 :hover, :pressed, :focus

运行方式：
python lesson1/step2_layout_design.py

练习题：
1. 添加一个"字数统计"标签，实时显示内容字数
2. 修改按钮样式为不同的颜色
3. 在保存前添加日期显示
"""
