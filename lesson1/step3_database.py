"""
第三步：数据库集成
目标：将界面与数据库连接，实现日记的保存和读取
"""

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox, QListWidget
)
from PyQt6.QtCore import Qt
import sys
from database import DatabaseManager


class MyDiaryApp(QMainWindow):
    """我的日记应用 - 数据库集成版"""
    
    def __init__(self):
        super().__init__()
        # 初始化数据库
        self.db = DatabaseManager("mydiary.db")
        self.current_diary_id = None  # 当前编辑的日记ID
        self.init_ui()
        self.load_diary_list()
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("MyDiary - 数据库集成")
        self.setGeometry(100, 100, 1000, 600)
        
        # 创建中心widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局（水平布局：左边列表，右边编辑区）
        main_layout = QHBoxLayout()
        
        # === 左侧：日记列表 ===
        left_layout = QVBoxLayout()
        
        # 列表标题
        list_label = QLabel("📚 日记列表")
        list_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 5px;")
        left_layout.addWidget(list_label)
        
        # 日记列表
        self.diary_list = QListWidget()
        self.diary_list.itemClicked.connect(self.on_diary_clicked)
        left_layout.addWidget(self.diary_list)
        
        # 新建按钮
        new_btn = QPushButton("➕ 新建日记")
        new_btn.setMinimumHeight(40)
        new_btn.clicked.connect(self.new_diary)
        left_layout.addWidget(new_btn)
        
        main_layout.addLayout(left_layout, 1)  # 左侧占1份
        
        # === 右侧：编辑区 ===
        right_layout = QVBoxLayout()
        
        # 标题区域
        title_layout = QHBoxLayout()
        title_label = QLabel("标题:")
        title_label.setMinimumWidth(60)
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("请输入日记标题...")
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.title_edit)
        right_layout.addLayout(title_layout)
        
        # 内容区域
        content_label = QLabel("内容:")
        right_layout.addWidget(content_label)
        
        self.content_edit = QTextEdit()
        self.content_edit.setPlaceholderText("记录今天的故事...")
        right_layout.addWidget(self.content_edit)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 保存")
        save_btn.setMinimumHeight(40)
        save_btn.clicked.connect(self.save_diary)
        
        delete_btn = QPushButton("🗑️ 删除")
        delete_btn.setMinimumHeight(40)
        delete_btn.clicked.connect(self.delete_diary)
        
        clear_btn = QPushButton("🆕 清空")
        clear_btn.setMinimumHeight(40)
        clear_btn.clicked.connect(self.clear_content)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addWidget(clear_btn)
        
        right_layout.addLayout(button_layout)
        
        main_layout.addLayout(right_layout, 2)  # 右侧占2份
        
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
            QListWidget {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #ecf0f1;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #ecf0f1;
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
    
    def load_diary_list(self):
        """加载日记列表"""
        self.diary_list.clear()
        diaries = self.db.get_all_diaries()
        
        for diary in diaries:
            # 格式：[日期] 标题
            item_text = f"[{diary['created_date']}] {diary['title']}"
            self.diary_list.addItem(item_text)
            
            # 将日记ID存储在item的data中
            item = self.diary_list.item(self.diary_list.count() - 1)
            item.setData(Qt.ItemDataRole.UserRole, diary['id'])
    
    def on_diary_clicked(self, item):
        """点击日记列表项"""
        diary_id = item.data(Qt.ItemDataRole.UserRole)
        diary = self.db.get_diary(diary_id)
        
        if diary:
            self.current_diary_id = diary_id
            self.title_edit.setText(diary['title'])
            self.content_edit.setPlainText(diary['content'])
    
    def new_diary(self):
        """新建日记"""
        self.current_diary_id = None
        self.clear_content()
    
    def save_diary(self):
        """保存日记"""
        title = self.title_edit.text()
        content = self.content_edit.toPlainText()
        
        # 验证输入
        if not title.strip():
            QMessageBox.warning(self, "警告", "请输入日记标题！")
            return
        
        if not content.strip():
            QMessageBox.warning(self, "警告", "请输入日记内容！")
            return
        
        try:
            if self.current_diary_id:
                # 更新现有日记
                self.db.update_diary(self.current_diary_id, title, content)
                QMessageBox.information(self, "成功", "日记已更新！")
            else:
                # 添加新日记
                diary_id = self.db.add_diary(title, content)
                self.current_diary_id = diary_id
                QMessageBox.information(self, "成功", "日记已保存！")
            
            # 刷新列表
            self.load_diary_list()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存失败: {str(e)}")
    
    def delete_diary(self):
        """删除日记"""
        if not self.current_diary_id:
            QMessageBox.warning(self, "警告", "请先选择要删除的日记！")
            return
        
        # 确认删除
        reply = QMessageBox.question(
            self,
            "确认删除",
            "确定要删除这篇日记吗？\n此操作无法撤销！",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db.delete_diary(self.current_diary_id)
                QMessageBox.information(self, "成功", "日记已删除！")
                
                # 刷新列表和清空编辑区
                self.load_diary_list()
                self.clear_content()
                self.current_diary_id = None
                
            except Exception as e:
                QMessageBox.critical(self, "错误", f"删除失败: {str(e)}")
    
    def clear_content(self):
        """清空编辑区"""
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
1. 数据库集成:
   - 使用DatabaseManager管理数据
   - 添加、查询、更新、删除日记

2. 列表组件:
   - QListWidget: 显示日记列表
   - itemClicked信号: 处理点击事件
   - setData/data: 在列表项中存储自定义数据

3. 状态管理:
   - current_diary_id: 跟踪当前编辑的日记
   - 区分新建和更新操作

4. 用户体验:
   - 确认对话框（删除前确认）
   - 成功/失败提示
   - 自动刷新列表

运行方式：
python lesson1/step3_database.py

练习题：
1. 添加字数统计显示
2. 实现搜索功能
3. 添加排序选项（按日期/标题）
4. 显示统计信息（总日记数、总字数等）
"""
