"""
第一节课完整版
包含所有基本功能的日记应用
"""

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox, QListWidget,
    QStatusBar, QInputDialog
)
from PyQt6.QtCore import Qt
import sys
from database import DatabaseManager


class MyDiaryApp(QMainWindow):
    """我的日记应用 - 第一节课完整版"""
    
    def __init__(self):
        super().__init__()
        # 初始化数据库
        self.db = DatabaseManager("mydiary.db")
        self.current_diary_id = None
        self.init_ui()
        self.load_diary_list()
        self.update_statistics()
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("MyDiary - 私密日记本")
        self.setGeometry(100, 100, 1000, 650)
        
        # 创建中心widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout()
        
        # === 左侧：日记列表区 ===
        left_layout = QVBoxLayout()
        
        # 顶部：搜索栏
        search_layout = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("🔍 搜索日记...")
        self.search_edit.textChanged.connect(self.search_diaries)
        search_btn = QPushButton("搜索")
        search_btn.clicked.connect(self.search_diaries)
        search_layout.addWidget(self.search_edit)
        search_layout.addWidget(search_btn)
        left_layout.addLayout(search_layout)
        
        # 列表标题
        list_label = QLabel("📚 日记列表")
        list_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 5px;")
        left_layout.addWidget(list_label)
        
        # 日记列表
        self.diary_list = QListWidget()
        self.diary_list.itemClicked.connect(self.on_diary_clicked)
        left_layout.addWidget(self.diary_list)
        
        # 统计信息
        self.stats_label = QLabel("统计: 0 篇日记, 0 字")
        self.stats_label.setStyleSheet("padding: 5px; color: #7f8c8d;")
        left_layout.addWidget(self.stats_label)
        
        # 新建按钮
        new_btn = QPushButton("➕ 新建日记")
        new_btn.setMinimumHeight(40)
        new_btn.clicked.connect(self.new_diary)
        left_layout.addWidget(new_btn)
        
        main_layout.addLayout(left_layout, 1)
        
        # === 右侧：编辑区 ===
        right_layout = QVBoxLayout()
        
        # 标题区域
        title_layout = QHBoxLayout()
        title_label = QLabel("标题:")
        title_label.setMinimumWidth(60)
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("请输入日记标题...")
        self.title_edit.textChanged.connect(self.on_content_changed)
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.title_edit)
        right_layout.addLayout(title_layout)
        
        # 内容区域
        content_label = QLabel("内容:")
        right_layout.addWidget(content_label)
        
        self.content_edit = QTextEdit()
        self.content_edit.setPlaceholderText("记录今天的故事...")
        self.content_edit.textChanged.connect(self.on_content_changed)
        right_layout.addWidget(self.content_edit)
        
        # 字数统计
        self.word_count_label = QLabel("字数: 0")
        self.word_count_label.setStyleSheet("padding: 5px; color: #7f8c8d;")
        right_layout.addWidget(self.word_count_label)
        
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
        
        main_layout.addLayout(right_layout, 2)
        
        # 设置布局
        central_widget.setLayout(main_layout)
        
        # 创建状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")
        
        # 设置样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ecf0f1;
            }
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
                background-color: white;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #3498db;
            }
            QListWidget {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 13px;
                background-color: white;
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
            item_text = f"[{diary['created_date']}] {diary['title']}"
            self.diary_list.addItem(item_text)
            item = self.diary_list.item(self.diary_list.count() - 1)
            item.setData(Qt.ItemDataRole.UserRole, diary['id'])
        
        self.status_bar.showMessage(f"已加载 {len(diaries)} 篇日记")
    
    def search_diaries(self):
        """搜索日记"""
        keyword = self.search_edit.text().strip()
        
        if not keyword:
            self.load_diary_list()
            return
        
        self.diary_list.clear()
        diaries = self.db.search_diaries(keyword)
        
        for diary in diaries:
            item_text = f"[{diary['created_date']}] {diary['title']}"
            self.diary_list.addItem(item_text)
            item = self.diary_list.item(self.diary_list.count() - 1)
            item.setData(Qt.ItemDataRole.UserRole, diary['id'])
        
        self.status_bar.showMessage(f"找到 {len(diaries)} 篇匹配的日记")
    
    def on_diary_clicked(self, item):
        """点击日记列表项"""
        diary_id = item.data(Qt.ItemDataRole.UserRole)
        diary = self.db.get_diary(diary_id)
        
        if diary:
            self.current_diary_id = diary_id
            self.title_edit.setText(diary['title'])
            self.content_edit.setPlainText(diary['content'])
            self.status_bar.showMessage(f"正在编辑: {diary['title']}")
    
    def new_diary(self):
        """新建日记"""
        self.current_diary_id = None
        self.clear_content()
        self.status_bar.showMessage("新建日记")
    
    def save_diary(self):
        """保存日记"""
        title = self.title_edit.text().strip()
        content = self.content_edit.toPlainText().strip()
        
        if not title:
            QMessageBox.warning(self, "警告", "请输入日记标题！")
            self.title_edit.setFocus()
            return
        
        if not content:
            QMessageBox.warning(self, "警告", "请输入日记内容！")
            self.content_edit.setFocus()
            return
        
        try:
            if self.current_diary_id:
                self.db.update_diary(self.current_diary_id, title, content)
                QMessageBox.information(self, "成功", "日记已更新！")
                self.status_bar.showMessage("日记已更新")
            else:
                diary_id = self.db.add_diary(title, content)
                self.current_diary_id = diary_id
                QMessageBox.information(self, "成功", "日记已保存！")
                self.status_bar.showMessage("日记已保存")
            
            self.load_diary_list()
            self.update_statistics()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存失败: {str(e)}")
            self.status_bar.showMessage("保存失败")
    
    def delete_diary(self):
        """删除日记"""
        if not self.current_diary_id:
            QMessageBox.warning(self, "警告", "请先选择要删除的日记！")
            return
        
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
                self.status_bar.showMessage("日记已删除")
                
                self.load_diary_list()
                self.update_statistics()
                self.clear_content()
                self.current_diary_id = None
                
            except Exception as e:
                QMessageBox.critical(self, "错误", f"删除失败: {str(e)}")
                self.status_bar.showMessage("删除失败")
    
    def clear_content(self):
        """清空编辑区"""
        self.title_edit.clear()
        self.content_edit.clear()
        self.title_edit.setFocus()
    
    def on_content_changed(self):
        """内容改变时更新字数"""
        content = self.content_edit.toPlainText()
        word_count = len(content)
        self.word_count_label.setText(f"字数: {word_count}")
    
    def update_statistics(self):
        """更新统计信息"""
        stats = self.db.get_statistics()
        self.stats_label.setText(
            f"统计: {stats['total_count']} 篇日记, "
            f"{stats['total_words']} 字 "
            f"(平均 {stats['avg_words']} 字/篇)"
        )


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("MyDiary")
    app.setOrganizationName("UIBE")
    app.setOrganizationDomain("uibe.edu.cn")
    
    window = MyDiaryApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()


"""
第一节课功能总结：
✅ 基本功能:
  - 新建日记
  - 保存日记到数据库
  - 查看日记列表
  - 编辑日记
  - 删除日记

✅ 增强功能:
  - 搜索功能
  - 字数实时统计
  - 统计信息显示
  - 状态栏提示
  - 输入验证

✅ 用户体验:
  - 美观的界面样式
  - 确认对话框
  - 成功/失败提示
  - 自动刷新列表

运行方式：
python lesson1/main_v1.py

课后作业：
1. 添加"今天"、"昨天"的日期显示
2. 实现日记导出为txt文件
3. 添加日记标签功能
4. 思考如何实现密码保护
"""
