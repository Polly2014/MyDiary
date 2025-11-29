"""
MyDiary 最终完整版
整合了所有功能的完整日记应用

功能清单：
✅ 第一节课功能
  - 基本窗口和布局
  - 日记增删改查
  - 数据库操作
  - 搜索功能
  - 字数统计

✅ 第二节课功能
  - 富文本编辑器
  - 心情标记
  - 数据统计（折线图、饼图）
  - PDF导出
  - 完整的用户体验

运行方式：
python main.py

作者：王宝莉
邮箱：baoli.wang@microsoft.com
"""

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QListWidget, QComboBox,
    QMessageBox, QFileDialog, QToolBar, QFontComboBox, QColorDialog,
    QStatusBar, QTabWidget, QCheckBox, QMenuBar, QMenu
)
from PyQt6.QtGui import QTextCharFormat, QColor, QFont, QAction, QKeySequence
from PyQt6.QtCore import Qt
import sys
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

# Matplotlib for statistics
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # Mac
# matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # Windows
matplotlib.rcParams['axes.unicode_minus'] = False

# ReportLab for PDF export
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import re


# ========== 数据库管理模块 ==========
class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_path: str = "mydiary_final.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS diaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                mood TEXT DEFAULT 'neutral',
                is_important INTEGER DEFAULT 0,
                created_date DATE NOT NULL,
                modified_date DATETIME,
                word_count INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_diary(self, title: str, content: str, mood: str = 'neutral', is_important: bool = False) -> int:
        """添加日记"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now()
        # 计算纯文本字数
        plain_text = re.sub('<[^>]+>', '', content)
        word_count = len(plain_text.replace(' ', '').replace('\n', ''))
        
        cursor.execute('''
            INSERT INTO diaries (title, content, mood, is_important, created_date, modified_date, word_count)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (title, content, mood, int(is_important), now.date(), now, word_count))
        
        conn.commit()
        diary_id = cursor.lastrowid
        conn.close()
        return diary_id
    
    def get_all_diaries(self) -> List[Dict]:
        """获取所有日记列表"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, created_date, mood, is_important
            FROM diaries
            ORDER BY is_important DESC, created_date DESC, id DESC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def get_diary(self, diary_id: int) -> Optional[Dict]:
        """获取单条日记"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, content, mood, is_important, created_date, modified_date, word_count
            FROM diaries
            WHERE id = ?
        ''', (diary_id,))
        
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def update_diary(self, diary_id: int, title: str, content: str, mood: str = 'neutral', is_important: bool = False) -> bool:
        """更新日记"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now()
        plain_text = re.sub('<[^>]+>', '', content)
        word_count = len(plain_text.replace(' ', '').replace('\n', ''))
        
        cursor.execute('''
            UPDATE diaries
            SET title = ?, content = ?, mood = ?, is_important = ?, modified_date = ?, word_count = ?
            WHERE id = ?
        ''', (title, content, mood, int(is_important), now, word_count, diary_id))
        
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        return affected > 0
    
    def delete_diary(self, diary_id: int) -> bool:
        """删除日记"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM diaries WHERE id = ?', (diary_id,))
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        return affected > 0
    
    def search_diaries(self, keyword: str) -> List[Dict]:
        """搜索日记"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        search_term = f"%{keyword}%"
        cursor.execute('''
            SELECT id, title, created_date, mood, is_important
            FROM diaries
            WHERE title LIKE ? OR content LIKE ?
            ORDER BY is_important DESC, created_date DESC
        ''', (search_term, search_term))
        
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM diaries')
        total_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT SUM(word_count) FROM diaries')
        total_words = cursor.fetchone()[0] or 0
        
        avg_words = total_words // total_count if total_count > 0 else 0
        
        conn.close()
        return {
            'total_count': total_count,
            'total_words': total_words,
            'avg_words': avg_words
        }


# ========== 统计图表组件 ==========
class StatisticsDialog(QWidget):
    """统计对话框"""
    
    MOOD_LABELS = {
        'happy': '😄 开心',
        'sad': '😢 难过',
        'neutral': '😐 平静',
        'angry': '😡 愤怒',
        'anxious': '😰 焦虑',
        'tired': '😴 疲惫',
        'confused': '🤔 困惑',
        'satisfied': '😌 满足'
    }
    
    def __init__(self, db: DatabaseManager):
        super().__init__()
        self.db = db
        self.setWindowTitle("数据统计")
        self.setGeometry(150, 150, 900, 700)
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout()
        
        # 标签页
        self.tabs = QTabWidget()
        
        # 基础统计页
        self.basic_widget = self.create_basic_stats()
        self.tabs.addTab(self.basic_widget, "📊 基础统计")
        
        # 字数趋势页
        self.trend_widget = QWidget()
        self.trend_layout = QVBoxLayout()
        self.trend_figure = Figure(figsize=(8, 6))
        self.trend_canvas = FigureCanvasQTAgg(self.trend_figure)
        self.trend_layout.addWidget(self.trend_canvas)
        self.trend_widget.setLayout(self.trend_layout)
        self.tabs.addTab(self.trend_widget, "📈 字数趋势")
        
        # 心情分布页
        self.mood_widget = QWidget()
        self.mood_layout = QVBoxLayout()
        self.mood_figure = Figure(figsize=(8, 6))
        self.mood_canvas = FigureCanvasQTAgg(self.mood_figure)
        self.mood_layout.addWidget(self.mood_canvas)
        self.mood_widget.setLayout(self.mood_layout)
        self.tabs.addTab(self.mood_widget, "😊 心情分布")
        
        layout.addWidget(self.tabs)
        
        # 刷新按钮
        refresh_btn = QPushButton("🔄 刷新数据")
        refresh_btn.clicked.connect(self.refresh_all)
        layout.addWidget(refresh_btn)
        
        self.setLayout(layout)
        self.refresh_all()
    
    def create_basic_stats(self):
        """创建基础统计页"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.total_label = QLabel()
        self.total_words_label = QLabel()
        self.avg_words_label = QLabel()
        
        for label in [self.total_label, self.total_words_label, self.avg_words_label]:
            label.setStyleSheet("font-size: 20px; padding: 15px;")
            layout.addWidget(label)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def refresh_all(self):
        """刷新所有统计"""
        self.refresh_basic_stats()
        self.refresh_trend_chart()
        self.refresh_mood_chart()
    
    def refresh_basic_stats(self):
        """刷新基础统计"""
        stats = self.db.get_statistics()
        self.total_label.setText(f"📚 总日记数: {stats['total_count']} 篇")
        self.total_words_label.setText(f"✍️ 总字数: {stats['total_words']:,} 字")
        self.avg_words_label.setText(f"📝 平均字数: {stats['avg_words']} 字/篇")
    
    def refresh_trend_chart(self):
        """刷新字数趋势图"""
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT created_date, SUM(word_count) as total_words
            FROM diaries
            WHERE created_date >= date('now', '-30 days')
            GROUP BY created_date
            ORDER BY created_date
        ''')
        
        data = cursor.fetchall()
        conn.close()
        
        if not data:
            return
        
        dates = [row[0] for row in data]
        words = [row[1] for row in data]
        
        self.trend_figure.clear()
        ax = self.trend_figure.add_subplot(111)
        ax.plot(dates, words, marker='o', linewidth=2, color='#3498db', markersize=8)
        ax.set_xlabel('日期', fontsize=12)
        ax.set_ylabel('字数', fontsize=12)
        ax.set_title('近30天字数趋势', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        for label in ax.get_xticklabels():
            label.set_rotation(45)
            label.set_ha('right')
        
        self.trend_figure.tight_layout()
        self.trend_canvas.draw()
    
    def refresh_mood_chart(self):
        """刷新心情分布图"""
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT mood, COUNT(*) as count
            FROM diaries
            WHERE mood IS NOT NULL
            GROUP BY mood
            ORDER BY count DESC
        ''')
        
        data = cursor.fetchall()
        conn.close()
        
        if not data:
            return
        
        moods = [self.MOOD_LABELS.get(row[0], row[0]) for row in data]
        counts = [row[1] for row in data]
        
        self.mood_figure.clear()
        ax = self.mood_figure.add_subplot(111)
        
        colors = ['#3498db', '#e74c3c', '#95a5a6', '#e67e22', '#9b59b6', '#1abc9c', '#f39c12', '#2ecc71']
        ax.pie(counts, labels=moods, autopct='%1.1f%%', colors=colors[:len(moods)], startangle=90)
        ax.set_title('心情分布', fontsize=14, fontweight='bold')
        
        self.mood_figure.tight_layout()
        self.mood_canvas.draw()


# ========== 主应用 ==========
class MyDiaryApp(QMainWindow):
    """MyDiary 主应用"""
    
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
    
    MOOD_EMOJI = {v: k for k, v in MOODS}
    
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.current_diary_id = None
        self.stats_dialog = None
        self.init_ui()
        self.load_diary_list()
        self.update_statistics()
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("MyDiary - 私密日记本 (完整版)")
        self.setGeometry(100, 100, 1200, 750)
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建工具栏
        self.create_toolbar()
        
        # 创建中心widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QHBoxLayout()
        
        # === 左侧：日记列表区 ===
        left_layout = QVBoxLayout()
        
        # 搜索框
        search_layout = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("🔍 搜索日记...")
        self.search_edit.textChanged.connect(self.search_diaries)
        clear_search_btn = QPushButton("❌")
        clear_search_btn.setMaximumWidth(40)
        clear_search_btn.clicked.connect(self.clear_search)
        search_layout.addWidget(self.search_edit)
        search_layout.addWidget(clear_search_btn)
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
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("padding: 5px; color: #7f8c8d; font-size: 11px;")
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
        
        # 心情和重要性
        mood_layout = QHBoxLayout()
        mood_label = QLabel("心情:")
        mood_label.setMinimumWidth(60)
        self.mood_combo = QComboBox()
        for text, value in self.MOODS:
            self.mood_combo.addItem(text, value)
        index = self.mood_combo.findData("neutral")
        self.mood_combo.setCurrentIndex(index)
        
        self.important_checkbox = QCheckBox("⭐ 标为重要")
        
        mood_layout.addWidget(mood_label)
        mood_layout.addWidget(self.mood_combo)
        mood_layout.addWidget(self.important_checkbox)
        mood_layout.addStretch()
        right_layout.addLayout(mood_layout)
        
        # 内容区域
        content_label = QLabel("内容:")
        right_layout.addWidget(content_label)
        
        self.content_edit = QTextEdit()
        self.content_edit.setPlaceholderText("记录今天的故事...")
        self.content_edit.textChanged.connect(self.on_content_changed)
        self.content_edit.cursorPositionChanged.connect(self.update_format_buttons)
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
        
        # 状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")
        
        # 设置样式
        self.apply_styles()
        
        # 设置快捷键
        self.setup_shortcuts()
    
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("文件")
        
        new_action = QAction("新建日记", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self.new_diary)
        file_menu.addAction(new_action)
        
        save_action = QAction("保存", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_diary)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        export_action = QAction("导出PDF", self)
        export_action.triggered.connect(self.export_to_pdf)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("退出", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 查看菜单
        view_menu = menubar.addMenu("查看")
        
        stats_action = QAction("数据统计", self)
        stats_action.triggered.connect(self.show_statistics)
        view_menu.addAction(stats_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu("帮助")
        
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        """创建格式化工具栏"""
        toolbar = QToolBar("格式工具栏")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # 字体
        font_label = QLabel(" 字体: ")
        toolbar.addWidget(font_label)
        
        self.font_box = QFontComboBox()
        self.font_box.setMaximumWidth(200)
        self.font_box.currentFontChanged.connect(self.change_font)
        toolbar.addWidget(self.font_box)
        
        toolbar.addSeparator()
        
        # 字号
        size_label = QLabel(" 字号: ")
        toolbar.addWidget(size_label)
        
        self.size_box = QComboBox()
        self.size_box.addItems(['10', '12', '14', '16', '18', '20', '24', '28'])
        self.size_box.setCurrentText('14')
        self.size_box.setMaximumWidth(80)
        self.size_box.currentTextChanged.connect(self.change_size)
        toolbar.addWidget(self.size_box)
        
        toolbar.addSeparator()
        
        # 格式按钮
        self.bold_btn = QPushButton("B")
        self.bold_btn.setCheckable(True)
        self.bold_btn.setStyleSheet("font-weight: bold;")
        self.bold_btn.clicked.connect(self.toggle_bold)
        toolbar.addWidget(self.bold_btn)
        
        self.italic_btn = QPushButton("I")
        self.italic_btn.setCheckable(True)
        self.italic_btn.setStyleSheet("font-style: italic;")
        self.italic_btn.clicked.connect(self.toggle_italic)
        toolbar.addWidget(self.italic_btn)
        
        self.underline_btn = QPushButton("U")
        self.underline_btn.setCheckable(True)
        self.underline_btn.setStyleSheet("text-decoration: underline;")
        self.underline_btn.clicked.connect(self.toggle_underline)
        toolbar.addWidget(self.underline_btn)
        
        toolbar.addSeparator()
        
        # 颜色
        color_btn = QPushButton("🎨")
        color_btn.setToolTip("文字颜色")
        color_btn.clicked.connect(self.change_text_color)
        toolbar.addWidget(color_btn)
        
        bg_color_btn = QPushButton("🖍️")
        bg_color_btn.setToolTip("背景颜色")
        bg_color_btn.clicked.connect(self.change_bg_color)
        toolbar.addWidget(bg_color_btn)
        
        toolbar.addSeparator()
        
        # 对齐
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
    
    def apply_styles(self):
        """应用样式"""
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
            QComboBox {
                padding: 5px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 13px;
                background-color: white;
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
            QToolBar {
                background-color: #ecf0f1;
                border: 1px solid #bdc3c7;
                spacing: 5px;
                padding: 5px;
            }
            QToolBar QPushButton {
                min-width: 35px;
                min-height: 30px;
                font-size: 14px;
            }
        """)
    
    def setup_shortcuts(self):
        """设置快捷键"""
        # Ctrl+S: 保存
        save_shortcut = QAction(self)
        save_shortcut.setShortcut(QKeySequence.StandardKey.Save)
        save_shortcut.triggered.connect(self.save_diary)
        self.addAction(save_shortcut)
        
        # Ctrl+N: 新建
        new_shortcut = QAction(self)
        new_shortcut.setShortcut(QKeySequence.StandardKey.New)
        new_shortcut.triggered.connect(self.new_diary)
        self.addAction(new_shortcut)
    
    # === 格式化方法 ===
    def change_font(self, font):
        """改变字体"""
        fmt = QTextCharFormat()
        fmt.setFontFamily(font.family())
        self.content_edit.mergeCurrentCharFormat(fmt)
    
    def change_size(self, size):
        """改变字号"""
        fmt = QTextCharFormat()
        fmt.setFontPointSize(int(size))
        self.content_edit.mergeCurrentCharFormat(fmt)
    
    def toggle_bold(self, checked):
        """切换加粗"""
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Weight.Bold if checked else QFont.Weight.Normal)
        self.content_edit.mergeCurrentCharFormat(fmt)
    
    def toggle_italic(self, checked):
        """切换斜体"""
        fmt = QTextCharFormat()
        fmt.setFontItalic(checked)
        self.content_edit.mergeCurrentCharFormat(fmt)
    
    def toggle_underline(self, checked):
        """切换下划线"""
        fmt = QTextCharFormat()
        fmt.setFontUnderline(checked)
        self.content_edit.mergeCurrentCharFormat(fmt)
    
    def change_text_color(self):
        """改变文字颜色"""
        color = QColorDialog.getColor()
        if color.isValid():
            fmt = QTextCharFormat()
            fmt.setForeground(color)
            self.content_edit.mergeCurrentCharFormat(fmt)
    
    def change_bg_color(self):
        """改变背景颜色"""
        color = QColorDialog.getColor()
        if color.isValid():
            fmt = QTextCharFormat()
            fmt.setBackground(color)
            self.content_edit.mergeCurrentCharFormat(fmt)
    
    def update_format_buttons(self):
        """更新格式按钮状态"""
        fmt = self.content_edit.currentCharFormat()
        self.bold_btn.setChecked(fmt.fontWeight() == QFont.Weight.Bold)
        self.italic_btn.setChecked(fmt.fontItalic())
        self.underline_btn.setChecked(fmt.fontUnderline())
        
        font = fmt.font()
        self.font_box.setCurrentFont(font)
        if fmt.fontPointSize() > 0:
            self.size_box.setCurrentText(str(int(fmt.fontPointSize())))
    
    # === 日记操作方法 ===
    def load_diary_list(self):
        """加载日记列表"""
        self.diary_list.clear()
        diaries = self.db.get_all_diaries()
        
        for diary in diaries:
            star = "⭐ " if diary.get('is_important') else ""
            mood = diary.get('mood', 'neutral')
            emoji = self.MOOD_EMOJI.get(mood, self.MOODS[2][0])
            
            item_text = f"{star}{emoji} [{diary['created_date']}] {diary['title']}"
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
            star = "⭐ " if diary.get('is_important') else ""
            mood = diary.get('mood', 'neutral')
            emoji = self.MOOD_EMOJI.get(mood, self.MOODS[2][0])
            
            item_text = f"{star}{emoji} [{diary['created_date']}] {diary['title']}"
            self.diary_list.addItem(item_text)
            item = self.diary_list.item(self.diary_list.count() - 1)
            item.setData(Qt.ItemDataRole.UserRole, diary['id'])
        
        self.status_bar.showMessage(f"找到 {len(diaries)} 篇匹配的日记")
    
    def clear_search(self):
        """清空搜索"""
        self.search_edit.clear()
        self.load_diary_list()
    
    def on_diary_clicked(self, item):
        """点击日记"""
        diary_id = item.data(Qt.ItemDataRole.UserRole)
        diary = self.db.get_diary(diary_id)
        
        if diary:
            self.current_diary_id = diary_id
            self.title_edit.setText(diary['title'])
            self.content_edit.setHtml(diary['content'])
            
            mood = diary.get('mood', 'neutral')
            index = self.mood_combo.findData(mood)
            if index >= 0:
                self.mood_combo.setCurrentIndex(index)
            
            self.important_checkbox.setChecked(bool(diary.get('is_important')))
            self.status_bar.showMessage(f"正在编辑: {diary['title']}")
    
    def new_diary(self):
        """新建日记"""
        self.current_diary_id = None
        self.clear_content()
        index = self.mood_combo.findData("neutral")
        self.mood_combo.setCurrentIndex(index)
        self.important_checkbox.setChecked(False)
        self.status_bar.showMessage("新建日记")
    
    def save_diary(self):
        """保存日记"""
        title = self.title_edit.text().strip()
        content = self.content_edit.toHtml()
        mood = self.mood_combo.currentData()
        is_important = self.important_checkbox.isChecked()
        
        if not title:
            QMessageBox.warning(self, "警告", "请输入日记标题！")
            self.title_edit.setFocus()
            return
        
        if not self.content_edit.toPlainText().strip():
            QMessageBox.warning(self, "警告", "请输入日记内容！")
            self.content_edit.setFocus()
            return
        
        try:
            if self.current_diary_id:
                self.db.update_diary(self.current_diary_id, title, content, mood, is_important)
                QMessageBox.information(self, "成功", "日记已更新！")
                self.status_bar.showMessage("日记已更新")
            else:
                diary_id = self.db.add_diary(title, content, mood, is_important)
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
    
    def clear_content(self):
        """清空编辑区"""
        self.title_edit.clear()
        self.content_edit.clear()
        self.title_edit.setFocus()
    
    def on_content_changed(self):
        """内容改变"""
        content = self.content_edit.toPlainText()
        word_count = len(content.replace(' ', '').replace('\n', ''))
        self.word_count_label.setText(f"字数: {word_count}")
    
    def update_statistics(self):
        """更新统计"""
        stats = self.db.get_statistics()
        self.stats_label.setText(
            f"📊 {stats['total_count']} 篇 | "
            f"✍️ {stats['total_words']} 字 | "
            f"📝 平均 {stats['avg_words']} 字/篇"
        )
    
    # === 其他功能 ===
    def show_statistics(self):
        """显示统计窗口"""
        if self.stats_dialog is None:
            self.stats_dialog = StatisticsDialog(self.db)
        self.stats_dialog.show()
        self.stats_dialog.raise_()
        self.stats_dialog.activateWindow()
    
    def export_to_pdf(self):
        """导出为PDF"""
        diaries = self.db.get_all_diaries()
        
        if not diaries:
            QMessageBox.information(self, "提示", "没有日记可以导出！")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "保存PDF文件",
            f"我的日记_{len(diaries)}篇.pdf",
            "PDF文件 (*.pdf)"
        )
        
        if not filename:
            return
        
        try:
            self.create_pdf(filename, diaries)
            QMessageBox.information(self, "成功", f"已导出 {len(diaries)} 篇日记！\n{filename}")
            self.status_bar.showMessage(f"已导出PDF: {filename}")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导出失败: {str(e)}")
    
    def create_pdf(self, filename, diary_list):
        """创建PDF"""
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4
        
        # 尝试注册中文字体
        try:
            pdfmetrics.registerFont(TTFont('SimSun', '/System/Library/Fonts/STHeiti Medium.ttc'))
        except:
            try:
                pdfmetrics.registerFont(TTFont('SimSun', 'C:/Windows/Fonts/simhei.ttf'))
            except:
                pass
        
        y = height - 50
        
        # 标题
        c.setFont('SimSun', 20)
        c.drawCentredString(width / 2, y, "我的日记集")
        y -= 40
        
        for i, diary_info in enumerate(diary_list, 1):
            diary = self.db.get_diary(diary_info['id'])
            if not diary:
                continue
            
            if y < 100:
                c.showPage()
                y = height - 50
            
            # 日记标题
            c.setFont('SimSun', 16)
            c.drawString(50, y, f"{i}. {diary['title']}")
            y -= 25
            
            # 日期和心情
            c.setFont('SimSun', 10)
            mood_dict = {v: k for k, v in self.MOODS}
            mood_text = mood_dict.get(diary.get('mood', 'neutral'), '平静')
            c.drawString(50, y, f"日期: {diary['created_date']}  |  心情: {mood_text}")
            y -= 20
            
            # 分隔线
            c.line(50, y, width - 50, y)
            y -= 20
            
            # 内容
            content = re.sub('<[^>]+>', '', diary['content'])
            c.setFont('SimSun', 12)
            
            for paragraph in content.split('\n')[:10]:
                if not paragraph.strip():
                    continue
                if y < 50:
                    c.showPage()
                    y = height - 50
                # 简单换行
                if len(paragraph) > 50:
                    paragraph = paragraph[:50] + "..."
                c.drawString(50, y, paragraph)
                y -= 18
            
            y -= 30
        
        c.save()
    
    def show_about(self):
        """关于对话框"""
        QMessageBox.about(
            self,
            "关于 MyDiary",
            "MyDiary - 私密日记本 (完整版)\n\n"
            "版本: 1.0\n"
            "作者: 王宝莉\n"
            "邮箱: baoli.wang@microsoft.com\n\n"
            "功能特性:\n"
            "✅ 富文本编辑\n"
            "✅ 心情标记\n"
            "✅ 数据统计\n"
            "✅ PDF导出\n"
            "✅ 搜索功能\n\n"
            "© 2024 对外经贸大学"
        )


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用信息
    app.setApplicationName("MyDiary")
    app.setOrganizationName("UIBE")
    app.setOrganizationDomain("uibe.edu.cn")
    
    # 创建并显示主窗口
    window = MyDiaryApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
