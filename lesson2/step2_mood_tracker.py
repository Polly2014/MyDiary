"""
第二步：心情标记
目标：添加心情选择器，记录每天的心情
"""

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QComboBox,
    QListWidget, QMessageBox
)
from PyQt6.QtCore import Qt
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from lesson1.database import DatabaseManager


class MoodDiaryApp(QMainWindow):
    """带心情标记的日记应用"""
    
    # 心情选项
    MOODS = [
        ("😄 开心", "happy"),
        ("😢 难过", "sad"),
        ("😐 平静", "neutral"),
        ("😡 愤怒", "angry"),
        ("😰 焦虑", "anxious"),
        ("😴 疲惫", "tired"),
        ("🤔 困惑", "confused"),
        ("😌 满足", "satisfied")
    ]
    
    # 心情emoji字典
    MOOD_EMOJI = {
        "happy": "😄",
        "sad": "😢",
        "neutral": "😐",
        "angry": "😡",
        "anxious": "😰",
        "tired": "😴",
        "confused": "🤔",
        "satisfied": "😌"
    }
    
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager("mydiary_v2.db")
        self.current_diary_id = None
        self.init_ui()
        self.load_diary_list()
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("MyDiary - 心情日记")
        self.setGeometry(100, 100, 1000, 600)
        
        # 创建中心widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout()
        
        # === 左侧：日记列表 ===
        left_layout = QVBoxLayout()
        
        list_label = QLabel("📚 日记列表")
        list_label.setStyleSheet("font-size: 16px; font-weight: bold; padding: 5px;")
        left_layout.addWidget(list_label)
        
        self.diary_list = QListWidget()
        self.diary_list.itemClicked.connect(self.on_diary_clicked)
        left_layout.addWidget(self.diary_list)
        
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
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.title_edit)
        right_layout.addLayout(title_layout)
        
        # === 心情选择区域 ===
        mood_layout = QHBoxLayout()
        mood_label = QLabel("心情:")
        mood_label.setMinimumWidth(60)
        
        self.mood_combo = QComboBox()
        self.mood_combo.setMinimumHeight(35)
        for text, value in self.MOODS:
            self.mood_combo.addItem(text, value)
        
        # 默认选择"平静"
        index = self.mood_combo.findData("neutral")
        self.mood_combo.setCurrentIndex(index)
        
        mood_layout.addWidget(mood_label)
        mood_layout.addWidget(self.mood_combo)
        right_layout.addLayout(mood_layout)
        
        # 内容区域
        content_label = QLabel("内容:")
        right_layout.addWidget(content_label)
        
        self.content_edit = QTextEdit()
        self.content_edit.setPlaceholderText("今天的心情怎么样？发生了什么事？")
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
        
        main_layout.addLayout(right_layout, 2)
        
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
            QComboBox {
                padding: 5px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
                background-color: white;
            }
            QComboBox:focus {
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
        """)
    
    def load_diary_list(self):
        """加载日记列表（带心情显示）"""
        self.diary_list.clear()
        diaries = self.db.get_all_diaries()
        
        for diary in diaries:
            # 获取心情emoji
            mood = diary.get('mood', 'neutral')
            emoji = self.MOOD_EMOJI.get(mood, '😐')
            
            # 格式：[心情] [日期] 标题
            item_text = f"{emoji} [{diary['created_date']}] {diary['title']}"
            self.diary_list.addItem(item_text)
            
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
            
            # 设置心情
            mood = diary.get('mood', 'neutral')
            index = self.mood_combo.findData(mood)
            if index >= 0:
                self.mood_combo.setCurrentIndex(index)
    
    def new_diary(self):
        """新建日记"""
        self.current_diary_id = None
        self.clear_content()
        # 重置心情为平静
        index = self.mood_combo.findData("neutral")
        self.mood_combo.setCurrentIndex(index)
    
    def save_diary(self):
        """保存日记（包含心情）"""
        title = self.title_edit.text().strip()
        content = self.content_edit.toPlainText().strip()
        mood = self.mood_combo.currentData()
        
        if not title:
            QMessageBox.warning(self, "警告", "请输入日记标题！")
            return
        
        if not content:
            QMessageBox.warning(self, "警告", "请输入日记内容！")
            return
        
        try:
            if self.current_diary_id:
                self.db.update_diary(self.current_diary_id, title, content, mood)
                QMessageBox.information(self, "成功", "日记已更新！")
            else:
                diary_id = self.db.add_diary(title, content, mood)
                self.current_diary_id = diary_id
                mood_text = self.mood_combo.currentText()
                QMessageBox.information(
                    self, 
                    "成功", 
                    f"日记已保存！\n心情: {mood_text}"
                )
            
            self.load_diary_list()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存失败: {str(e)}")
    
    def delete_diary(self):
        """删除日记"""
        if not self.current_diary_id:
            QMessageBox.warning(self, "警告", "请先选择要删除的日记！")
            return
        
        reply = QMessageBox.question(
            self,
            "确认删除",
            "确定要删除这篇日记吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db.delete_diary(self.current_diary_id)
                QMessageBox.information(self, "成功", "日记已删除！")
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
    window = MoodDiaryApp()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()


"""
知识点总结：
1. QComboBox下拉框:
   - addItem(text, data): 添加选项，可附带数据
   - currentData(): 获取当前选项的数据
   - findData(value): 根据数据查找索引
   - setCurrentIndex(): 设置当前选项

2. 数据存储:
   - 使用元组列表存储心情选项
   - 分离显示文本和数据值
   - 使用字典映射心情到emoji

3. 列表显示增强:
   - 在列表项中显示emoji
   - 格式化列表项文本
   - 使用UserRole存储ID

4. 用户体验:
   - 清晰的心情选择
   - 列表中直观显示心情
   - 编辑时自动回显心情

运行方式：
python lesson2/step2_mood_tracker.py

练习题：
1. 添加心情统计（显示各种心情的数量）
2. 实现按心情筛选日记
3. 添加自定义心情选项
4. 统计最近一周的心情趋势
"""
