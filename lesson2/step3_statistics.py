"""
第三步：数据统计与可视化
目标：使用Matplotlib展示日记统计数据
"""

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTabWidget
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from lesson1.database import DatabaseManager

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # Mac
# matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # Windows
matplotlib.rcParams['axes.unicode_minus'] = False


class StatisticsWidget(QWidget):
    """统计图表组件"""
    
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout()
        
        # 创建标签页
        self.tabs = QTabWidget()
        
        # 基础统计页
        self.basic_tab = QWidget()
        self.init_basic_tab()
        self.tabs.addTab(self.basic_tab, "📊 基础统计")
        
        # 字数趋势页
        self.trend_tab = QWidget()
        self.init_trend_tab()
        self.tabs.addTab(self.trend_tab, "📈 字数趋势")
        
        # 心情分布页
        self.mood_tab = QWidget()
        self.init_mood_tab()
        self.tabs.addTab(self.mood_tab, "😊 心情分布")
        
        layout.addWidget(self.tabs)
        
        # 刷新按钮
        refresh_btn = QPushButton("🔄 刷新数据")
        refresh_btn.setMinimumHeight(40)
        refresh_btn.clicked.connect(self.refresh_all)
        layout.addWidget(refresh_btn)
        
        self.setLayout(layout)
        
        # 加载数据
        self.refresh_all()
    
    def init_basic_tab(self):
        """初始化基础统计页"""
        layout = QVBoxLayout()
        
        self.total_label = QLabel("总日记数: 0")
        self.total_label.setStyleSheet("font-size: 18px; padding: 10px;")
        
        self.total_words_label = QLabel("总字数: 0")
        self.total_words_label.setStyleSheet("font-size: 18px; padding: 10px;")
        
        self.avg_words_label = QLabel("平均字数: 0")
        self.avg_words_label.setStyleSheet("font-size: 18px; padding: 10px;")
        
        layout.addWidget(self.total_label)
        layout.addWidget(self.total_words_label)
        layout.addWidget(self.avg_words_label)
        layout.addStretch()
        
        self.basic_tab.setLayout(layout)
    
    def init_trend_tab(self):
        """初始化趋势图页"""
        layout = QVBoxLayout()
        
        self.trend_figure = Figure(figsize=(8, 6))
        self.trend_canvas = FigureCanvasQTAgg(self.trend_figure)
        layout.addWidget(self.trend_canvas)
        
        self.trend_tab.setLayout(layout)
    
    def init_mood_tab(self):
        """初始化心情分布页"""
        layout = QVBoxLayout()
        
        self.mood_figure = Figure(figsize=(8, 6))
        self.mood_canvas = FigureCanvasQTAgg(self.mood_figure)
        layout.addWidget(self.mood_canvas)
        
        self.mood_tab.setLayout(layout)
    
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
        # 获取最近30天的数据
        conn = self.db.db.connect(self.db.db_path)
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
        
        ax.plot(dates, words, marker='o', linewidth=2, color='#3498db')
        ax.set_xlabel('日期', fontsize=12)
        ax.set_ylabel('字数', fontsize=12)
        ax.set_title('近30天字数趋势', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # 旋转日期标签
        for label in ax.get_xticklabels():
            label.set_rotation(45)
            label.set_ha('right')
        
        self.trend_figure.tight_layout()
        self.trend_canvas.draw()
    
    def refresh_mood_chart(self):
        """刷新心情分布图"""
        import sqlite3
        
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
        
        # 心情映射
        mood_labels = {
            'happy': '😄 开心',
            'sad': '😢 难过',
            'neutral': '😐 平静',
            'angry': '😡 愤怒',
            'anxious': '😰 焦虑',
            'tired': '😴 疲惫',
            'confused': '🤔 困惑',
            'satisfied': '😌 满足'
        }
        
        moods = [mood_labels.get(row[0], row[0]) for row in data]
        counts = [row[1] for row in data]
        
        self.mood_figure.clear()
        ax = self.mood_figure.add_subplot(111)
        
        colors = ['#3498db', '#e74c3c', '#95a5a6', '#e67e22', '#9b59b6', '#1abc9c', '#f39c12', '#2ecc71']
        ax.pie(counts, labels=moods, autopct='%1.1f%%', colors=colors[:len(moods)])
        ax.set_title('心情分布', fontsize=14, fontweight='bold')
        
        self.mood_figure.tight_layout()
        self.mood_canvas.draw()


class StatisticsApp(QMainWindow):
    """统计应用"""
    
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager("mydiary_v2.db")
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("MyDiary - 数据统计")
        self.setGeometry(100, 100, 900, 700)
        
        # 创建统计组件
        stats_widget = StatisticsWidget(self.db)
        self.setCentralWidget(stats_widget)
        
        # 设置样式
        self.setStyleSheet("""
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


def main():
    """主函数"""
    app = QApplication(sys.argv)
    window = StatisticsApp()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()


"""
知识点总结：
1. Matplotlib集成:
   - FigureCanvasQTAgg: Qt画布
   - Figure: 图形对象
   - add_subplot(): 添加子图
   - plot(): 折线图
   - pie(): 饼图

2. 数据查询:
   - GROUP BY: 分组统计
   - SUM(): 求和
   - COUNT(): 计数
   - date(): SQLite日期函数

3. QTabWidget标签页:
   - addTab(): 添加标签页
   - 组织多个视图

4. 图表美化:
   - 颜色设置
   - 网格线
   - 标签旋转
   - tight_layout(): 自动调整布局

运行方式：
python lesson2/step3_statistics.py

练习题：
1. 添加柱状图显示每月日记数
2. 统计最常用的词汇
3. 显示写作活跃时段
4. 导出统计报告
"""
