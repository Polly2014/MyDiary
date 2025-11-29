# 🎨 MyDiary - 私密日记本

## 📚 课程概述

本课程通过构建一个桌面版私密日记应用，学习 Python 桌面应用开发技术。

**课程时长：** 2 节课（每节 90 分钟）  
**技术栈：** PyQt6 + Qt Designer + SQLite + Matplotlib + Python  
**目标学生：** 有 Python 基础，想学习桌面应用开发的学生

---

## 🎯 学习目标

### 第一节课：PyQt6 基础与事件处理
- ✅ 掌握 PyQt6 基础组件（QLabel, QPushButton, QLineEdit 等）
- ✅ 理解布局管理器（QVBoxLayout, QHBoxLayout, QGridLayout）
- ✅ 掌握信号与槽机制
- ✅ 学习事件处理方法
- ✅ 对比 Qt Designer 与纯代码开发

### 第二节课：Qt Designer 与综合应用
- ✅ 学会使用 Qt Designer 可视化设计界面
- ✅ 掌握 .ui 文件转换与使用流程
- ✅ 实现富文本编辑器（QTextEdit）
- ✅ 集成 SQLite 数据库实现 CRUD 操作
- ✅ 使用 Matplotlib 实现数据可视化
- ✅ 完成完整的日记本应用

---

## 📂 项目结构

```
MyDiary/
├── README.md                    # 项目说明
├── requirements.txt             # 依赖包列表
├── main.py                      # 完整版日记本应用
├── .gitignore                  # Git 忽略文件
├── PPT/                        # 教学材料
│   ├── 教学讲义.md               # 教师详细讲义
│   ├── 课程安排.md               # 课程安排和时间规划
│   └── 课堂演示讲义.md            # 学生课堂演示版本
├── lesson1/                    # 第一节课：PyQt6 基础
│   ├── step1_hello_world.py     # 第一个窗口程序
│   ├── step2_basic_widgets.py   # 基础控件使用
│   ├── step3_layout.py          # 布局管理器
│   └── step4_signals_slots.py   # 信号与槽机制
├── lesson2/                    # 第二节课：综合应用
│   ├── step1_rich_editor.py     # 富文本编辑器
│   ├── step2_database.py        # 数据库集成
│   └── step3_statistics.py      # 数据可视化
└── lessonEx/                   # 补充示例和文档
    ├── simple_dialog.ui         # Qt Designer 示例文件
    ├── simple_dialog.py         # pyuic6 生成的 Python 代码
    ├── simple_dialog_main.py    # 业务逻辑实现
    ├── event_handling_demo.py   # 事件处理完整示例
    ├── code_based_ui.py         # 纯代码 UI 对比示例
    ├── designer_workflow.md     # Qt Designer 工作流程详解
    └── comparison.md            # Designer vs 代码开发对比
```

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/Polly2014/MyDiary.git
cd MyDiary
```

### 2. 创建虚拟环境（推荐）

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

**主要依赖包：**
- PyQt6 >= 6.6.0 (GUI 框架)
- matplotlib >= 3.8.0 (数据可视化)
- reportlab >= 4.0.0 (PDF 导出)

### 4. 运行应用

**运行完整版日记本应用：**
```bash
python main.py
```

**分步学习（第一节课）：**
```bash
python lesson1/step1_hello_world.py      # 最简单的窗口
python lesson1/step2_basic_widgets.py    # 基础控件演示
python lesson1/step3_layout.py           # 布局管理器
python lesson1/step4_signals_slots.py    # 信号与槽
```

**分步学习（第二节课）：**
```bash
python lesson2/step1_rich_editor.py      # 富文本编辑器
python lesson2/step2_database.py         # 数据库操作
python lesson2/step3_statistics.py       # 统计图表
```

**补充示例：**
```bash
python lessonEx/simple_dialog_main.py    # Qt Designer 示例
python lessonEx/event_handling_demo.py   # 事件处理演示
python lessonEx/code_based_ui.py         # 纯代码 UI 示例
```

### 5. Qt Designer 使用

**启动 Qt Designer（macOS）：**
```bash
# 直接启动
open /opt/homebrew/bin/designer

# 打开指定 .ui 文件
/opt/homebrew/bin/designer lessonEx/simple_dialog.ui &

# 创建快捷别名
echo 'alias designer="/opt/homebrew/bin/designer"' >> ~/.zshrc
source ~/.zshrc
```

**转换 .ui 文件为 Python 代码：**
```bash
pyuic6 -o output.py input.ui
```

---

## 📖 课程内容

### 第一节课：PyQt6 基础与事件处理（90 分钟）

**时间分配：**
- 15 分钟：Python GUI 框架对比 + PyQt6 优势介绍
- 15 分钟：环境搭建与依赖安装
- 20 分钟：PyQt6 基础（Hello World + 控件 + 布局）
- 25 分钟：信号与槽机制详解
- 10 分钟：事件处理实战
- 5 分钟：Qt Designer vs 纯代码对比

**核心知识点：**
- PyQt6 vs PySide6 vs Tkinter vs wxPython 对比
- PyQt6 基本组件（QMainWindow, QLabel, QPushButton, QLineEdit）
- 布局管理器（QVBoxLayout, QHBoxLayout, QGridLayout）
- 信号与槽机制（clicked, textChanged, returnPressed）
- 事件处理方法（mousePressEvent, keyPressEvent）
- 开发方式选择（Designer vs 代码）

**课后作业：**
- 修改示例代码添加更多控件
- 尝试连接不同信号和槽
- 阅读补充文档

### 第二节课：Qt Designer 与综合应用（90 分钟）

**时间分配：**
- 5 分钟：回顾第一节课
- 25 分钟：Qt Designer 完整工作流程
- 20 分钟：富文本编辑器实现
- 20 分钟：数据库集成（SQLite CRUD）
- 15 分钟：数据可视化（Matplotlib 图表）
- 5 分钟：完整项目展示与总结

**核心知识点：**
- Qt Designer 界面设计流程
- .ui 文件转换（pyuic6）
- UI 类的正确使用方式（组合 vs 多重继承）
- QTextEdit 富文本操作（字体、颜色、格式）
- SQLite 数据库操作（连接、CRUD、事务）
- Matplotlib 与 PyQt6 集成（FigureCanvas）
- 中文显示配置

**课后作业：**
- 用 Designer 设计自己的界面
- 实现数据库增删改查
- 添加统计图表功能
- （挑战）完善 MyDiary 项目

---

## 🌟 项目特色

1. **渐进式教学**：从 Hello World 到完整应用，分 8 个 step 循序渐进
2. **双模式对比**：既讲 Qt Designer 可视化开发，又讲纯代码实现
3. **实用性强**：开发真正能用的日记本应用（富文本、数据库、统计图表）
4. **完整体验**：涵盖 GUI 设计、数据库、可视化、文件操作全流程
5. **丰富文档**：教师讲义 + 学生讲义 + 工作流程文档 + 对比分析文档

---

## 🔗 相关资源

- [PyQt6 官方文档](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [Qt 官方文档](https://doc.qt.io/)
- [Qt Designer 下载](https://www.qt.io/download-qt-installer)
- [SQLite 教程](https://www.sqlite.org/docs.html)
- [Matplotlib 文档](https://matplotlib.org/stable/contents.html)
- [Python 官方文档](https://docs.python.org/zh-cn/3/)

---

## 📝 学习建议与扩展

### 学习路径
1. **第一节课后**：熟练掌握信号与槽，尝试修改示例代码
2. **第二节课后**：独立完成数据库 CRUD，添加自己的图表类型
3. **课程结束后**：完善 MyDiary，添加个性化功能

### 扩展功能建议

**基础扩展：**
- 添加日记删除确认对话框
- 实现日记内容搜索功能
- 添加字数实时统计
- 支持 Markdown 格式

**进阶扩展：**
- 实现密码保护功能
- 添加图片插入与管理
- 实现标签分类系统
- 支持多种导出格式（Word、HTML）
- 添加主题切换（QSS 样式表）
- 实现数据备份与恢复

**高级挑战：**
- 云端同步（使用 API）
- 多用户支持
- 全文加密存储
- 语音输入集成
- 自然语言处理（情感分析）

---

## 👨‍🏫 教师备注

### 课前准备
- ✅ 提前测试所有示例代码（8 个 step + main.py）
- ✅ 确认 Qt Designer 已安装并配置正确
- ✅ 准备好虚拟环境和依赖包安装脚本
- ✅ 熟悉三份教学文档（教学讲义、课程安排、课堂演示讲义）
- ✅ 准备好演示数据（sample diary entries）

### 教学要点
- 💡 第一节课重点：信号与槽机制（最核心概念）
- 💡 第二节课重点：Qt Designer 工作流程（设计→转换→使用）
- 💡 强调：不要手动修改 pyuic6 生成的文件
- 💡 对比：Designer vs 纯代码的适用场景
- 💡 实践：让学生动手修改代码，观察效果

### 常见问题
1. **PyQt6 vs PySide6**：API 99% 相同，许可证不同
2. **中文显示问题**：设置 matplotlib 字体为 Arial Unicode MS
3. **路径问题**：使用绝对路径或相对于脚本的路径
4. **虚拟环境**：强调每个项目独立环境的重要性

---

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

## 📄 许可证

MIT License

---

**祝教学顺利！🎉**
