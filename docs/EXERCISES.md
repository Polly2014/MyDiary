# MyDiary 课程练习题与答案

## 📝 第一节课练习

### 练习1：窗口定制（简单）

**题目：**
修改 `lesson1/step1_first_window.py`，实现以下功能：
1. 窗口标题改为"我的日记 - [你的名字]"
2. 窗口大小改为 900x700
3. 欢迎文字改为"欢迎 [你的名字] 使用日记本！"
4. 文字颜色改为蓝色（#3498db）

**答案：**
```python
class MyDiaryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("我的日记 - 张三")  # 改1
        self.setGeometry(100, 100, 900, 700)    # 改2
        
        label = QLabel("欢迎 张三 使用日记本！", self)  # 改3
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #3498db;  /* 改4 */
            }
        """)
        
        self.setCentralWidget(label)
```

---

### 练习2：字数统计（中等）

**题目：**
在 `lesson1/step2_layout_design.py` 中添加实时字数统计功能：
1. 在内容编辑区下方添加一个标签显示字数
2. 每当内容改变时，自动更新字数
3. 格式：`字数: 123 | 字符: 123`

**答案：**
```python
class MyDiaryApp(QMainWindow):
    def init_ui(self):
        # ... 原有代码 ...
        
        # 添加字数统计标签
        self.word_count_label = QLabel("字数: 0 | 字符: 0")
        self.word_count_label.setStyleSheet("""
            QLabel {
                padding: 5px;
                color: #7f8c8d;
                font-weight: normal;
            }
        """)
        main_layout.addWidget(self.word_count_label)
        
        # 连接信号
        self.content_edit.textChanged.connect(self.update_word_count)
    
    def update_word_count(self):
        """更新字数统计"""
        content = self.content_edit.toPlainText()
        
        # 计算字数（去除空格）
        words = len(content.replace(' ', '').replace('\n', ''))
        
        # 计算字符数（包含空格和换行）
        chars = len(content)
        
        self.word_count_label.setText(f"字数: {words} | 字符: {chars}")
```

---

### 练习3：快捷键（中等）

**题目：**
在 `lesson1/step2_layout_design.py` 中添加快捷键支持：
1. Ctrl+S 或 Cmd+S 保存
2. Ctrl+N 或 Cmd+N 清空
3. Ctrl+Q 或 Cmd+Q 退出

**答案：**
```python
from PyQt6.QtGui import QKeySequence, QShortcut

class MyDiaryApp(QMainWindow):
    def init_ui(self):
        # ... 原有代码 ...
        
        # 添加快捷键
        self.setup_shortcuts()
    
    def setup_shortcuts(self):
        """设置快捷键"""
        # Ctrl/Cmd + S: 保存
        save_shortcut = QShortcut(QKeySequence.StandardKey.Save, self)
        save_shortcut.activated.connect(self.save_diary)
        
        # Ctrl/Cmd + N: 新建/清空
        new_shortcut = QShortcut(QKeySequence.StandardKey.New, self)
        new_shortcut.activated.connect(self.clear_content)
        
        # Ctrl/Cmd + Q: 退出
        quit_shortcut = QShortcut(QKeySequence.StandardKey.Quit, self)
        quit_shortcut.activated.connect(self.close)
```

---

### 练习4：搜索功能（中等）

**题目：**
在 `lesson1/step3_database.py` 中实现搜索功能：
1. 添加搜索输入框
2. 输入关键词后实时搜索
3. 搜索范围：标题和内容
4. 显示搜索结果数量

**答案：**
```python
class MyDiaryApp(QMainWindow):
    def init_ui(self):
        # 在左侧布局顶部添加搜索框
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
        
        # ... 其余代码 ...
    
    def search_diaries(self):
        """搜索日记"""
        keyword = self.search_edit.text().strip()
        
        if not keyword:
            # 如果搜索框为空，显示所有日记
            self.load_diary_list()
            return
        
        # 使用数据库的搜索方法
        self.diary_list.clear()
        diaries = self.db.search_diaries(keyword)
        
        for diary in diaries:
            item_text = f"[{diary['created_date']}] {diary['title']}"
            self.diary_list.addItem(item_text)
            item = self.diary_list.item(self.diary_list.count() - 1)
            item.setData(Qt.ItemDataRole.UserRole, diary['id'])
        
        # 更新状态栏
        self.statusBar().showMessage(f"找到 {len(diaries)} 篇匹配的日记")
    
    def clear_search(self):
        """清空搜索"""
        self.search_edit.clear()
        self.load_diary_list()
```

---

### 练习5：标为重要（困难）

**题目：**
添加"标为重要"功能：
1. 修改数据库，添加 `is_important` 字段
2. 在界面添加"标为重要"复选框
3. 列表中重要日记显示⭐图标
4. 支持按重要性排序

**答案：**

**1. 修改 `database.py`：**
```python
class DatabaseManager:
    def init_database(self):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS diaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                mood TEXT DEFAULT 'neutral',
                created_date DATE NOT NULL,
                modified_date DATETIME,
                word_count INTEGER DEFAULT 0,
                is_important INTEGER DEFAULT 0  -- 新增字段
            )
        ''')
    
    def add_diary(self, title, content, mood='neutral', is_important=False):
        cursor.execute('''
            INSERT INTO diaries 
            (title, content, mood, created_date, modified_date, word_count, is_important)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (title, content, mood, now.date(), now, word_count, int(is_important)))
    
    def update_diary(self, diary_id, title, content, mood='neutral', is_important=False):
        cursor.execute('''
            UPDATE diaries
            SET title = ?, content = ?, mood = ?, modified_date = ?, 
                word_count = ?, is_important = ?
            WHERE id = ?
        ''', (title, content, mood, now, word_count, int(is_important), diary_id))
```

**2. 修改界面代码：**
```python
from PyQt6.QtWidgets import QCheckBox

class MyDiaryApp(QMainWindow):
    def init_ui(self):
        # 在心情选择后添加重要性复选框
        self.important_checkbox = QCheckBox("⭐ 标为重要")
        right_layout.addWidget(self.important_checkbox)
    
    def load_diary_list(self):
        """加载日记列表（显示重要标记）"""
        self.diary_list.clear()
        diaries = self.db.get_all_diaries()
        
        for diary in diaries:
            # 添加重要标记
            star = "⭐ " if diary.get('is_important') else ""
            item_text = f"{star}[{diary['created_date']}] {diary['title']}"
            self.diary_list.addItem(item_text)
            item = self.diary_list.item(self.diary_list.count() - 1)
            item.setData(Qt.ItemDataRole.UserRole, diary['id'])
    
    def on_diary_clicked(self, item):
        """点击日记时，同步重要性状态"""
        diary_id = item.data(Qt.ItemDataRole.UserRole)
        diary = self.db.get_diary(diary_id)
        
        if diary:
            # ... 原有代码 ...
            self.important_checkbox.setChecked(bool(diary.get('is_important')))
    
    def save_diary(self):
        """保存时包含重要性"""
        is_important = self.important_checkbox.isChecked()
        
        if self.current_diary_id:
            self.db.update_diary(
                self.current_diary_id, title, content, mood, is_important
            )
        else:
            diary_id = self.db.add_diary(title, content, mood, is_important)
```

---

## 📝 第二节课练习

### 练习6：撤销重做（简单）

**题目：**
在 `lesson2/step1_rich_editor.py` 中添加撤销和重做按钮。

**答案：**
```python
class RichTextEditor(QMainWindow):
    def create_format_toolbar(self):
        # 在工具栏开始处添加
        undo_btn = QPushButton("↶")
        undo_btn.setToolTip("撤销 (Ctrl+Z)")
        undo_btn.clicked.connect(self.content_edit.undo)
        toolbar.addWidget(undo_btn)
        
        redo_btn = QPushButton("↷")
        redo_btn.setToolTip("重做 (Ctrl+Y)")
        redo_btn.clicked.connect(self.content_edit.redo)
        toolbar.addWidget(redo_btn)
        
        toolbar.addSeparator()
```

---

### 练习7：心情统计（中等）

**题目：**
在 `lesson2/step2_mood_tracker.py` 中添加心情统计功能：
1. 在界面底部显示各种心情的数量
2. 添加"按心情筛选"功能

**答案：**
```python
class MoodDiaryApp(QMainWindow):
    def init_ui(self):
        # 在左侧布局底部添加统计标签
        self.mood_stats_label = QLabel()
        self.mood_stats_label.setStyleSheet("padding: 10px; background-color: #ecf0f1;")
        left_layout.addWidget(self.mood_stats_label)
        
        # 添加筛选下拉框
        filter_layout = QHBoxLayout()
        filter_label = QLabel("筛选:")
        self.filter_combo = QComboBox()
        self.filter_combo.addItem("全部", None)
        for text, value in self.MOODS:
            self.filter_combo.addItem(text, value)
        self.filter_combo.currentIndexChanged.connect(self.filter_by_mood)
        
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_combo)
        left_layout.addLayout(filter_layout)
        
        # 更新统计
        self.update_mood_stats()
    
    def update_mood_stats(self):
        """更新心情统计"""
        import sqlite3
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT mood, COUNT(*) as count
            FROM diaries
            GROUP BY mood
        ''')
        
        stats = cursor.fetchall()
        conn.close()
        
        # 格式化显示
        stats_text = "心情统计:\n"
        for mood, count in stats:
            emoji = self.MOOD_EMOJI.get(mood, '😐')
            stats_text += f"{emoji} {count}篇  "
        
        self.mood_stats_label.setText(stats_text)
    
    def filter_by_mood(self):
        """按心情筛选"""
        mood = self.filter_combo.currentData()
        
        if mood is None:
            self.load_diary_list()
            return
        
        # 查询特定心情的日记
        import sqlite3
        conn = sqlite3.connect(self.db.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, created_date, mood
            FROM diaries
            WHERE mood = ?
            ORDER BY created_date DESC
        ''', (mood,))
        
        diaries = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        # 更新列表
        self.diary_list.clear()
        for diary in diaries:
            emoji = self.MOOD_EMOJI.get(diary['mood'], '😐')
            item_text = f"{emoji} [{diary['created_date']}] {diary['title']}"
            self.diary_list.addItem(item_text)
            item = self.diary_list.item(self.diary_list.count() - 1)
            item.setData(Qt.ItemDataRole.UserRole, diary['id'])
    
    def save_diary(self):
        # 保存后更新统计
        # ... 原有保存代码 ...
        self.update_mood_stats()
```

---

### 练习8：词频统计（困难）

**题目：**
添加词频统计功能，显示最常用的10个词汇（需要安装jieba）。

**答案：**
```python
# 首先安装 jieba
# pip install jieba

import jieba
from collections import Counter

class StatisticsWidget(QWidget):
    def init_ui(self):
        # 添加词云标签页
        self.word_tab = QWidget()
        self.init_word_tab()
        self.tabs.addTab(self.word_tab, "🔤 词频统计")
    
    def init_word_tab(self):
        """初始化词频统计页"""
        layout = QVBoxLayout()
        
        self.word_list = QListWidget()
        layout.addWidget(self.word_list)
        
        self.word_tab.setLayout(layout)
    
    def refresh_word_stats(self):
        """刷新词频统计"""
        # 获取所有日记内容
        diaries = self.db.get_all_diaries()
        
        # 合并所有内容
        all_content = ""
        for diary in diaries:
            diary_detail = self.db.get_diary(diary['id'])
            # 去除HTML标签
            import re
            content = re.sub('<[^>]+>', '', diary_detail['content'])
            all_content += content + " "
        
        # 分词
        words = jieba.cut(all_content)
        
        # 过滤停用词和单字
        stop_words = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'}
        filtered_words = [w for w in words if len(w) > 1 and w not in stop_words]
        
        # 统计词频
        word_counts = Counter(filtered_words)
        top_words = word_counts.most_common(10)
        
        # 显示
        self.word_list.clear()
        for i, (word, count) in enumerate(top_words, 1):
            self.word_list.addItem(f"{i}. {word} ({count}次)")
    
    def refresh_all(self):
        # 在原有的刷新方法中添加
        self.refresh_word_stats()
```

---

### 练习9：PDF水印（中等）

**题目：**
在导出的PDF中添加水印"私密文档"。

**答案：**
```python
class ExportApp(QMainWindow):
    def create_pdf(self, filename, diaries):
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4
        
        # ... 原有代码 ...
        
        # 在每一页添加水印
        def add_watermark():
            c.saveState()
            c.setFont('SimSun', 40)
            c.setFillColorRGB(0.9, 0.9, 0.9, alpha=0.3)  # 浅灰色，半透明
            c.translate(width / 2, height / 2)
            c.rotate(45)
            c.drawCentredString(0, 0, "私密文档")
            c.restoreState()
        
        # 在绘制内容后添加水印
        add_watermark()
        
        # 遍历日记
        for i, diary in enumerate(diaries, 1):
            if y < 100:
                add_watermark()  # 新页也添加水印
                c.showPage()
                y = height - 50
            
            # ... 原有绘制代码 ...
        
        add_watermark()  # 最后一页
        c.save()
```

---

### 练习10：连续写作天数（困难）

**题目：**
计算并显示连续写作天数，激励用户坚持写日记。

**答案：**
```python
class DatabaseManager:
    def get_consecutive_days(self):
        """获取连续写作天数"""
        from datetime import datetime, timedelta
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 获取所有日记日期（去重）
        cursor.execute('''
            SELECT DISTINCT created_date
            FROM diaries
            ORDER BY created_date DESC
        ''')
        
        dates = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        if not dates:
            return 0
        
        # 计算连续天数
        consecutive = 1
        today = datetime.now().date()
        
        # 转换字符串为日期
        date_objects = [datetime.strptime(d, '%Y-%m-%d').date() for d in dates]
        
        # 检查今天是否写了
        if date_objects[0] != today:
            # 检查昨天
            yesterday = today - timedelta(days=1)
            if date_objects[0] != yesterday:
                return 0
        
        # 计算连续天数
        for i in range(len(date_objects) - 1):
            diff = (date_objects[i] - date_objects[i + 1]).days
            if diff == 1:
                consecutive += 1
            else:
                break
        
        return consecutive

# 在主应用中显示
class MyDiaryApp(QMainWindow):
    def update_statistics(self):
        stats = self.db.get_statistics()
        consecutive = self.db.get_consecutive_days()
        
        self.stats_label.setText(
            f"统计: {stats['total_count']} 篇日记, "
            f"{stats['total_words']} 字 | "
            f"🔥 连续写作 {consecutive} 天"
        )
```

---

## 🎓 综合项目练习

### 项目1：密码保护（困难）

**要求：**
1. 应用启动时要求输入密码
2. 使用cryptography库加密数据库
3. 三次密码错误后锁定5分钟
4. 提供修改密码功能

**提示：**
```python
from cryptography.fernet import Fernet
import hashlib

# 生成密钥
key = Fernet.generate_key()
cipher = Fernet(key)

# 加密
encrypted = cipher.encrypt(data.encode())

# 解密
decrypted = cipher.decrypt(encrypted).decode()

# 密码哈希
password_hash = hashlib.sha256(password.encode()).hexdigest()
```

---

### 项目2：云同步（困难）

**要求：**
1. 支持导出数据为JSON
2. 上传到云存储（如阿里云OSS）
3. 从云端恢复数据
4. 处理冲突

---

### 项目3：主题切换（中等）

**要求：**
1. 实现浅色和深色主题
2. 添加主题选择器
3. 保存用户偏好
4. 平滑过渡动画

**提示：**
```python
# 深色主题样式
DARK_THEME = """
    QMainWindow {
        background-color: #2c3e50;
    }
    QLabel {
        color: #ecf0f1;
    }
    /* ... 更多样式 ... */
"""

# 切换主题
def change_theme(self, theme_name):
    if theme_name == "dark":
        self.setStyleSheet(DARK_THEME)
    else:
        self.setStyleSheet(LIGHT_THEME)
```

---

## 📚 提交作业

完成练习后，请：

1. **创建GitHub仓库**
2. **提交代码**
3. **写好README**
4. **发送链接给老师**

**评分标准：**
- 功能完整性：60%
- 代码质量：20%
- 创新性：20%

---

**加油！期待你的优秀作品！** 🎉
