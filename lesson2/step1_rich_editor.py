"""
第一步：富文本编辑器
目标：实现富文本编辑功能（字体、颜色、格式）
"""

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QToolBar, QLabel, QLineEdit, QTextEdit, QPushButton,
    QFontComboBox, QComboBox, QColorDialog, QMessageBox
)
from PyQt6.QtGui import QTextCharFormat, QColor, QFont, QAction
from PyQt6.QtCore import Qt
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from lesson1.database import DatabaseManager


class RichTextEditor(QMainWindow):
    """富文本编辑器"""
    
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager("mydiary_v2.db")
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("MyDiary - 富文本编辑器")
        self.setGeometry(100, 100, 900, 700)
        
        # 创建中心widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout()
        
        # 创建格式工具栏
        self.create_format_toolbar()
        
        # === 标题区域 ===
        title_layout = QHBoxLayout()
        title_label = QLabel("标题:")
        title_label.setMinimumWidth(60)
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("请输入日记标题...")
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.title_edit)
        main_layout.addLayout(title_layout)
        
        # === 内容区域（富文本编辑器）===
        content_label = QLabel("内容:")
        main_layout.addWidget(content_label)
        
        self.content_edit = QTextEdit()
        self.content_edit.setPlaceholderText("尝试使用上面的工具栏来格式化文字...")
        main_layout.addWidget(self.content_edit)
        
        # === 按钮区域 ===
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 保存为HTML")
        save_btn.setMinimumHeight(40)
        save_btn.clicked.connect(self.save_diary)
        
        load_btn = QPushButton("📖 测试加载")
        load_btn.setMinimumHeight(40)
        load_btn.clicked.connect(self.test_load)
        
        clear_btn = QPushButton("🆕 清空")
        clear_btn.setMinimumHeight(40)
        clear_btn.clicked.connect(self.clear_content)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(load_btn)
        button_layout.addWidget(clear_btn)
        
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
            QToolBar {
                background-color: #ecf0f1;
                border: 1px solid #bdc3c7;
                spacing: 5px;
                padding: 5px;
            }
            QToolBar QPushButton {
                min-width: 40px;
                min-height: 30px;
                font-size: 16px;
            }
        """)
    
    def create_format_toolbar(self):
        """创建格式化工具栏"""
        toolbar = QToolBar("格式工具栏")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # === 字体选择 ===
        font_label = QLabel(" 字体: ")
        toolbar.addWidget(font_label)
        
        self.font_box = QFontComboBox()
        self.font_box.setMaximumWidth(200)
        self.font_box.currentFontChanged.connect(self.change_font)
        toolbar.addWidget(self.font_box)
        
        toolbar.addSeparator()
        
        # === 字号选择 ===
        size_label = QLabel(" 字号: ")
        toolbar.addWidget(size_label)
        
        self.size_box = QComboBox()
        self.size_box.addItems(['10', '12', '14', '16', '18', '20', '24', '28', '32'])
        self.size_box.setCurrentText('14')
        self.size_box.setMaximumWidth(80)
        self.size_box.currentTextChanged.connect(self.change_size)
        toolbar.addWidget(self.size_box)
        
        toolbar.addSeparator()
        
        # === 加粗按钮 ===
        bold_btn = QPushButton("B")
        bold_btn.setCheckable(True)
        bold_btn.setStyleSheet("font-weight: bold;")
        bold_btn.clicked.connect(self.toggle_bold)
        toolbar.addWidget(bold_btn)
        self.bold_btn = bold_btn
        
        # === 斜体按钮 ===
        italic_btn = QPushButton("I")
        italic_btn.setCheckable(True)
        italic_btn.setStyleSheet("font-style: italic;")
        italic_btn.clicked.connect(self.toggle_italic)
        toolbar.addWidget(italic_btn)
        self.italic_btn = italic_btn
        
        # === 下划线按钮 ===
        underline_btn = QPushButton("U")
        underline_btn.setCheckable(True)
        underline_btn.setStyleSheet("text-decoration: underline;")
        underline_btn.clicked.connect(self.toggle_underline)
        toolbar.addWidget(underline_btn)
        self.underline_btn = underline_btn
        
        toolbar.addSeparator()
        
        # === 文字颜色 ===
        color_btn = QPushButton("🎨")
        color_btn.setToolTip("文字颜色")
        color_btn.clicked.connect(self.change_text_color)
        toolbar.addWidget(color_btn)
        
        # === 背景颜色 ===
        bg_color_btn = QPushButton("🖍️")
        bg_color_btn.setToolTip("背景颜色")
        bg_color_btn.clicked.connect(self.change_bg_color)
        toolbar.addWidget(bg_color_btn)
        
        toolbar.addSeparator()
        
        # === 对齐方式 ===
        align_left_btn = QPushButton("⬅️")
        align_left_btn.setToolTip("左对齐")
        align_left_btn.clicked.connect(lambda: self.content_edit.setAlignment(Qt.AlignmentFlag.AlignLeft))
        toolbar.addWidget(align_left_btn)
        
        align_center_btn = QPushButton("↔️")
        align_center_btn.setToolTip("居中")
        align_center_btn.clicked.connect(lambda: self.content_edit.setAlignment(Qt.AlignmentFlag.AlignCenter))
        toolbar.addWidget(align_center_btn)
        
        align_right_btn = QPushButton("➡️")
        align_right_btn.setToolTip("右对齐")
        align_right_btn.clicked.connect(lambda: self.content_edit.setAlignment(Qt.AlignmentFlag.AlignRight))
        toolbar.addWidget(align_right_btn)
        
        # 连接编辑器信号，更新工具栏状态
        self.content_edit.cursorPositionChanged.connect(self.update_format_buttons)
    
    def change_font(self, font):
        """改变字体"""
        fmt = QTextCharFormat()
        fmt.setFontFamily(font.family())
        self.content_edit.mergeCurrentCharFormat(fmt)
        self.content_edit.setFocus()
    
    def change_size(self, size):
        """改变字号"""
        fmt = QTextCharFormat()
        fmt.setFontPointSize(int(size))
        self.content_edit.mergeCurrentCharFormat(fmt)
        self.content_edit.setFocus()
    
    def toggle_bold(self, checked):
        """切换加粗"""
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Weight.Bold if checked else QFont.Weight.Normal)
        self.content_edit.mergeCurrentCharFormat(fmt)
        self.content_edit.setFocus()
    
    def toggle_italic(self, checked):
        """切换斜体"""
        fmt = QTextCharFormat()
        fmt.setFontItalic(checked)
        self.content_edit.mergeCurrentCharFormat(fmt)
        self.content_edit.setFocus()
    
    def toggle_underline(self, checked):
        """切换下划线"""
        fmt = QTextCharFormat()
        fmt.setFontUnderline(checked)
        self.content_edit.mergeCurrentCharFormat(fmt)
        self.content_edit.setFocus()
    
    def change_text_color(self):
        """改变文字颜色"""
        color = QColorDialog.getColor()
        if color.isValid():
            fmt = QTextCharFormat()
            fmt.setForeground(color)
            self.content_edit.mergeCurrentCharFormat(fmt)
            self.content_edit.setFocus()
    
    def change_bg_color(self):
        """改变背景颜色"""
        color = QColorDialog.getColor()
        if color.isValid():
            fmt = QTextCharFormat()
            fmt.setBackground(color)
            self.content_edit.mergeCurrentCharFormat(fmt)
            self.content_edit.setFocus()
    
    def update_format_buttons(self):
        """更新格式按钮状态"""
        # 获取当前光标处的格式
        fmt = self.content_edit.currentCharFormat()
        
        # 更新加粗按钮
        self.bold_btn.setChecked(fmt.fontWeight() == QFont.Weight.Bold)
        
        # 更新斜体按钮
        self.italic_btn.setChecked(fmt.fontItalic())
        
        # 更新下划线按钮
        self.underline_btn.setChecked(fmt.fontUnderline())
        
        # 更新字体和字号
        font = fmt.font()
        self.font_box.setCurrentFont(font)
        if fmt.fontPointSize() > 0:
            self.size_box.setCurrentText(str(int(fmt.fontPointSize())))
    
    def save_diary(self):
        """保存日记（HTML格式）"""
        title = self.title_edit.text().strip()
        html_content = self.content_edit.toHtml()
        
        if not title:
            QMessageBox.warning(self, "警告", "请输入标题！")
            return
        
        if not self.content_edit.toPlainText().strip():
            QMessageBox.warning(self, "警告", "请输入内容！")
            return
        
        try:
            # 保存为HTML
            diary_id = self.db.add_diary(title, html_content)
            QMessageBox.information(
                self, 
                "成功", 
                f"日记已保存！\nID: {diary_id}\n\n格式已保存为HTML"
            )
            self.last_saved_id = diary_id
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存失败: {str(e)}")
    
    def test_load(self):
        """测试加载最后保存的日记"""
        if not hasattr(self, 'last_saved_id'):
            QMessageBox.information(self, "提示", "请先保存一篇日记")
            return
        
        try:
            diary = self.db.get_diary(self.last_saved_id)
            if diary:
                self.title_edit.setText(diary['title'])
                self.content_edit.setHtml(diary['content'])  # 使用setHtml加载
                QMessageBox.information(self, "成功", "日记已加载，格式已恢复！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载失败: {str(e)}")
    
    def clear_content(self):
        """清空内容"""
        self.title_edit.clear()
        self.content_edit.clear()
        self.title_edit.setFocus()


def main():
    """主函数"""
    app = QApplication(sys.argv)
    window = RichTextEditor()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()


"""
知识点总结：
1. QTextEdit富文本编辑:
   - toHtml(): 获取HTML格式的内容
   - setHtml(): 设置HTML内容
   - toPlainText(): 获取纯文本
   - mergeCurrentCharFormat(): 合并字符格式

2. QTextCharFormat格式设置:
   - setFontFamily(): 设置字体
   - setFontPointSize(): 设置字号
   - setFontWeight(): 设置粗细
   - setFontItalic(): 设置斜体
   - setFontUnderline(): 设置下划线
   - setForeground(): 设置文字颜色
   - setBackground(): 设置背景颜色

3. QToolBar工具栏:
   - addWidget(): 添加组件
   - addSeparator(): 添加分隔线
   - setMovable(): 设置是否可移动

4. 信号连接:
   - cursorPositionChanged: 光标位置改变
   - currentFontChanged: 字体改变
   - currentTextChanged: 文本改变

5. HTML存储:
   - 使用HTML保存格式
   - 数据库中存储HTML字符串
   - 加载时使用setHtml恢复格式

运行方式：
python lesson2/step1_rich_editor.py

练习题：
1. 添加撤销/重做功能（content_edit.undo/redo）
2. 添加项目符号和编号列表
3. 实现查找和替换功能
"""
