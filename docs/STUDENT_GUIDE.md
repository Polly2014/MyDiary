# MyDiary 学生学习指南

欢迎学习 Python 桌面应用开发！本指南将帮助你顺利完成课程。

---

## 📚 课前准备

### 1. 环境要求

- **操作系统：** Windows 10+, macOS 10.14+, 或 Linux
- **Python版本：** 3.10 或更高
- **内存：** 至少 4GB RAM
- **磁盘空间：** 至少 1GB 可用空间

### 2. 安装Python

**检查Python版本：**
```bash
python --version
# 应该显示 Python 3.10.x 或更高
```

**如果没有Python或版本太低：**
- Windows: 访问 [python.org](https://www.python.org/downloads/)
- macOS: 使用 Homebrew `brew install python@3.10`
- Linux: `sudo apt-get install python3.10`

### 3. 创建虚拟环境（推荐）

**为什么使用虚拟环境？**
- 隔离项目依赖，避免版本冲突
- 便于管理和迁移项目
- 符合Python开发最佳实践

```bash
# 克隆项目（或下载ZIP）
git clone https://github.com/Polly2014/MyDiary.git
cd MyDiary

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 看到命令行前有 (venv) 标志说明激活成功
```

### 4. 安装依赖

```bash
# 确保虚拟环境已激活
pip install -r requirements.txt
```

**依赖说明：**
- `PyQt6` - GUI框架
- `matplotlib` - 数据可视化
- `reportlab` - PDF生成
- `cryptography` - 加密（可选）

### 5. 测试安装

```bash
# 确保虚拟环境已激活（命令行前有 (venv) 标志）
# 运行第一个示例
python lesson1/step1_first_window.py
```

如果看到一个窗口弹出，说明环境配置成功！ 🎉

---

## 🎓 学习路径

### 第一节课：基础篇

```
Step 1: 第一个窗口
  ↓
Step 2: 界面布局
  ↓
Step 3: 数据库集成
  ↓
完整应用 v1
```

**学习时长：** 约 2-3 小时（包括练习）

### 第二节课：进阶篇

```
Step 1: 富文本编辑器
  ↓
Step 2: 心情标记
  ↓
Step 3: 数据统计
  ↓
Step 4: PDF导出
  ↓
应用打包
```

**学习时长：** 约 2-3 小时（包括练习）

---

## 📖 详细学习步骤

### 第一节课

#### Step 1: 第一个窗口（30分钟）

**目标：** 理解PyQt6的基本结构

**运行代码：**
```bash
python lesson1/step1_first_window.py
```

**你应该看到：**
- 一个800x600的窗口
- 标题是"MyDiary - 私密日记本"
- 中央显示"欢迎使用 MyDiary！"

**代码解读：**
```python
# 1. 导入必要的模块
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel

# 2. 创建应用程序对象（必须）
app = QApplication(sys.argv)

# 3. 创建主窗口
class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("标题")  # 设置标题
        self.setGeometry(x, y, width, height)  # 位置和大小

# 4. 启动事件循环
sys.exit(app.exec())
```

**练习任务：**
1. 修改窗口标题为你的名字
2. 调整窗口大小为 900x700
3. 改变欢迎文字的颜色和大小（提示：使用setStyleSheet）

**参考答案：** 见 `docs/EXERCISES.md`

---

#### Step 2: 界面布局（45分钟）

**目标：** 掌握布局管理和常用组件

**运行代码：**
```bash
python lesson1/step2_layout_design.py
```

**关键概念：**

1. **布局类型：**
   - `QVBoxLayout` - 垂直布局
   - `QHBoxLayout` - 水平布局
   - `QGridLayout` - 网格布局

2. **常用组件：**
   - `QLabel` - 文本标签
   - `QLineEdit` - 单行输入
   - `QTextEdit` - 多行输入
   - `QPushButton` - 按钮

3. **信号与槽：**
   ```python
   button.clicked.connect(self.function_name)
   ```

**练习任务：**
1. 添加一个字数统计标签
2. 修改按钮样式为不同颜色
3. 添加快捷键（Ctrl+S保存）

---

#### Step 3: 数据库集成（60分钟）

**目标：** 实现数据持久化

**运行代码：**
```bash
python lesson1/step3_database.py
```

**数据库基础：**

**表结构：**
```sql
CREATE TABLE diaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    mood TEXT DEFAULT 'neutral',
    created_date DATE NOT NULL,
    word_count INTEGER DEFAULT 0
);
```

**CRUD操作：**
- **C**reate: `db.add_diary(title, content)`
- **R**ead: `db.get_diary(id)`
- **U**pdate: `db.update_diary(id, title, content)`
- **D**elete: `db.delete_diary(id)`

**练习任务：**
1. 实现搜索功能（在数据库模块已有，调用它）
2. 添加"标为重要"功能
3. 统计总日记数和总字数

---

### 第二节课

#### Step 1: 富文本编辑器（40分钟）

**目标：** 实现格式化文本编辑

**运行代码：**
```bash
python lesson2/step1_rich_editor.py
```

**核心知识：**

1. **QTextEdit富文本：**
   ```python
   # 获取HTML
   html = text_edit.toHtml()
   
   # 设置HTML
   text_edit.setHtml(html)
   
   # 格式化
   fmt = QTextCharFormat()
   fmt.setFontWeight(QFont.Weight.Bold)
   text_edit.mergeCurrentCharFormat(fmt)
   ```

2. **工具栏：**
   ```python
   toolbar = QToolBar()
   self.addToolBar(toolbar)
   toolbar.addWidget(widget)
   ```

**练习任务：**
1. 添加撤销/重做按钮
2. 添加列表功能（项目符号）
3. 实现字体大小快捷键（Ctrl++ / Ctrl+-）

---

#### Step 2: 心情标记（30分钟）

**目标：** 添加情绪记录功能

**运行代码：**
```bash
python lesson2/step2_mood_tracker.py
```

**关键组件：QComboBox**
```python
# 添加选项
combo.addItem(display_text, data_value)

# 获取选中的值
value = combo.currentData()

# 查找并设置
index = combo.findData(value)
combo.setCurrentIndex(index)
```

**练习任务：**
1. 添加自定义心情选项
2. 统计每种心情的日记数
3. 按心情筛选日记

---

#### Step 3: 数据统计（45分钟）

**目标：** 数据可视化

**运行代码：**
```bash
python lesson2/step3_statistics.py
```

**Matplotlib基础：**

```python
# 1. 创建画布
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

figure = Figure()
canvas = FigureCanvasQTAgg(figure)

# 2. 绘制图表
ax = figure.add_subplot(111)
ax.plot(x, y)
ax.set_xlabel('X轴')
ax.set_ylabel('Y轴')

# 3. 刷新显示
canvas.draw()
```

**中文字体：**
```python
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # Mac
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # Windows
```

**练习任务：**
1. 添加柱状图显示每月日记数
2. 统计最常用的词汇（提示：使用jieba分词）
3. 显示写作时间分布

---

#### Step 4: PDF导出（30分钟）

**目标：** 将日记导出为PDF

**运行代码：**
```bash
python lesson2/step4_export.py
```

**练习任务：**
1. 添加PDF水印
2. 支持选择字体大小
3. 添加页眉页脚

---

## 🔧 常见问题

### 安装问题

**Q: pip install失败，提示网络错误**

A: 使用国内镜像
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**Q: ImportError: No module named 'PyQt6'**

A: 确保使用正确的Python版本
```bash
python3 -m pip install PyQt6
```

**Q: Mac上matplotlib中文显示方块**

A: 使用系统字体
```python
matplotlib.rcParams['font.sans-serif'] = ['Arial Unicode MS']
```

### 代码问题

**Q: 窗口一闪而过**

A: 确保有事件循环
```python
sys.exit(app.exec())  # 不要忘记这行
```

**Q: 数据库文件在哪里？**

A: 在项目根目录，文件名是 `mydiary.db`
```bash
ls -la *.db
```

**Q: 如何重置数据库？**

A: 删除数据库文件
```bash
rm mydiary.db
rm mydiary_v2.db
```

### 运行问题

**Q: 打包后的exe体积很大**

A: 这是正常的，因为包含了Python解释器和所有依赖

**Q: 如何更改数据库路径？**

A: 修改DatabaseManager的参数
```python
db = DatabaseManager("/path/to/your/diary.db")
```

---

## 📚 推荐学习资源

### 官方文档

- [PyQt6文档](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [Qt6文档](https://doc.qt.io/qt-6/)
- [Python SQLite文档](https://docs.python.org/3/library/sqlite3.html)
- [Matplotlib文档](https://matplotlib.org/stable/contents.html)

### 视频教程

- [PyQt6 Tutorial - YouTube](https://www.youtube.com/results?search_query=pyqt6+tutorial)
- [Python GUI Programming - Coursera](https://www.coursera.org/search?query=python%20gui)

### 书籍推荐

- 《Rapid GUI Programming with Python and Qt》
- 《Python Qt GUI快速编程》
- 《SQLite权威指南》

### 练习项目

完成本项目后，可以尝试：
1. **待办事项管理器**
2. **笔记应用**
3. **个人财务管理**
4. **图片浏览器**

---

## 💪 学习建议

### 学习方法

1. **不要只看不做**
   - 每个示例都要亲手运行
   - 理解每行代码的作用
   - 尝试修改参数观察效果

2. **遇到问题先自己思考**
   - 看错误信息
   - 查文档
   - Google搜索
   - 最后再问老师

3. **做笔记**
   - 记录关键概念
   - 整理常用代码片段
   - 总结遇到的问题

4. **多实践**
   - 完成所有练习题
   - 添加自己的创意功能
   - 分享给朋友使用

### 进度建议

**第1周：**
- 完成第一节课所有内容
- 做完基础练习
- 熟悉PyQt6组件

**第2周：**
- 完成第二节课所有内容
- 做完进阶练习
- 添加自己的功能

**第3周：**
- 完善应用
- 美化界面
- 打包发布

---

## 🎯 学习目标检查清单

### 第一节课

- [ ] 能独立创建PyQt6窗口
- [ ] 理解布局管理器的使用
- [ ] 掌握信号与槽机制
- [ ] 会使用SQLite数据库
- [ ] 能实现基本的CRUD功能
- [ ] 完成第一节课所有练习

### 第二节课

- [ ] 能使用QTextEdit实现富文本编辑
- [ ] 理解QTextCharFormat的使用
- [ ] 会使用QComboBox
- [ ] 能集成Matplotlib绘制图表
- [ ] 了解ReportLab生成PDF
- [ ] 能使用PyInstaller打包应用
- [ ] 完成第二节课所有练习

### 综合能力

- [ ] 能独立设计数据库表结构
- [ ] 能设计友好的用户界面
- [ ] 能处理常见错误和异常
- [ ] 能阅读和理解他人代码
- [ ] 能使用Git管理代码
- [ ] 完成至少一个创新功能

---

## 📞 获取帮助

### 在线资源

- **项目GitHub：** https://github.com/Polly2014/MyDiary
- **Issues反馈：** 在GitHub上提Issue
- **讨论区：** GitHub Discussions

### 联系方式

- **邮箱：** baoli.wang@microsoft.com
- **课程答疑时间：** 每周三下午2-4点（线上）

### 学习社区

- Stack Overflow: 搜索"PyQt6"
- Reddit: r/learnpython, r/PyQt
- 知乎: 搜索"PyQt教程"

---

## 🎓 评分标准

### 作业评分（30分）

- 功能完整性（15分）
- 代码质量（10分）
- 创新性（5分）

### 课堂参与（20分）

- 出勤（5分）
- 提问和讨论（10分）
- 帮助同学（5分）

### 期末项目（50分）

- 功能实现（30分）
  - 所有基础功能
  - 至少2个创新功能
- 代码质量（10分）
  - 结构清晰
  - 有注释
  - 符合PEP8规范
- 文档和展示（10分）
  - README完整
  - 使用说明清楚
  - 项目演示

---

## 🌟 优秀学员作品

完成项目后，欢迎提交到：
https://github.com/Polly2014/MyDiary/discussions

优秀作品将在这里展示！

---

**祝学习愉快！加油！** 💪
