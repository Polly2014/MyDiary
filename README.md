# 🎨 MyDiary - 私密日记本

## 📚 课程概述

本课程通过构建一个桌面版私密日记应用，学习Python桌面应用开发技术。

**课程时长：** 2节课（每节90分钟）  
**技术栈：** PyQt6 + Eric IDE + SQLite + Python  
**目标学生：** 有Python基础，想学习桌面应用开发的学生

---

## 🎯 学习目标

### 第一节课
- ✅ 掌握PyQt6基础组件
- ✅ 学会使用Eric IDE可视化设计界面
- ✅ 理解SQLite数据库操作
- ✅ 实现基本的日记增删改查

### 第二节课
- ✅ 实现富文本编辑器
- ✅ 添加心情标记功能
- ✅ 实现搜索和日历联动
- ✅ 数据统计与可视化
- ✅ 导出功能与项目打包

---

## 📂 项目结构

```
MyDiary/
├── README.md                 # 项目说明
├── requirements.txt          # 依赖包列表
├── .gitignore               # Git忽略文件
├── PPT/                     # 教学PPT
│   ├── Lesson1_PyQt基础与数据库.md
│   └── Lesson2_高级功能与完善.md
├── lesson1/                 # 第一节课代码
│   ├── step1_first_window.py    # 第一个窗口
│   ├── step2_layout_design.py   # 布局设计
│   ├── step3_database.py        # 数据库集成
│   └── main_v1.py              # 第一节课完整版本
├── lesson2/                 # 第二节课代码
│   ├── rich_editor.py          # 富文本编辑器
│   ├── mood_widget.py          # 心情选择器
│   ├── statistics.py           # 统计功能
│   ├── export_utils.py         # 导出工具
│   └── main_v2.py              # 第二节课完整版本
├── database/                # 数据库模块
│   ├── db_manager.py           # 数据库管理器
│   └── init_db.sql            # 数据库初始化脚本
├── ui/                      # Eric生成的UI文件
│   └── (Eric设计器生成的文件)
├── resources/               # 资源文件
│   ├── icons/                  # 图标
│   └── styles/                 # 样式表
├── docs/                    # 文档
│   ├── TEACHING_GUIDE.md       # 教学指南
│   ├── STUDENT_GUIDE.md        # 学生使用指南
│   ├── ERIC_GUIDE.md          # Eric IDE使用指南
│   └── API_REFERENCE.md        # API参考文档
├── exercises/               # 练习题
│   ├── lesson1_exercises.md    # 第一节课练习
│   ├── lesson2_exercises.md    # 第二节课练习
│   └── answers/               # 练习答案
│       ├── lesson1_answers.md
│       └── lesson2_answers.md
└── utils/                   # 工具模块
    ├── crypto.py               # 加密工具
    └── helpers.py              # 辅助函数
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

### 4. 运行应用

**运行完整版应用：**
```bash
python main.py
```

**运行教学版本（分步学习）：**
```bash
# 第一节课
python lesson1/step1_basic_window.py       # 基本窗口
python lesson1/step2_list_widget.py        # 列表组件
python lesson1/step3_database.py           # 数据库集成
python lesson1/main_v1.py                   # 第一节课完整版

# 第二节课
python lesson2/step1_rich_editor.py        # 富文本编辑
python lesson2/step2_mood_tracker.py       # 心情追踪
python lesson2/step3_statistics.py         # 统计功能
python lesson2/step4_export_pdf.py         # PDF导出
python lesson2/main_v2.py                   # 第二节课完整版
```

---

## 📖 课程内容

### 第一节课：PyQt基础与数据库（90分钟）

**时间分配：**
- 10分钟：课程介绍 + 环境准备
- 25分钟：PyQt6基础（step1 + step2）
- 25分钟：数据库集成（step3）
- 20分钟：功能整合与测试
- 10分钟：总结与练习

**核心知识点：**
- PyQt6基本组件（QMainWindow, QTextEdit, QListWidget）
- 布局管理（QVBoxLayout, QHBoxLayout）
- 信号与槽机制
- SQLite数据库操作
- CRUD操作实现

### 第二节课：高级功能与完善（90分钟）

**时间分配：**
- 5分钟：回顾上节课
- 25分钟：富文本编辑器
- 25分钟：高级功能（心情、搜索、日历）
- 20分钟：统计与可视化
- 10分钟：导出与打包
- 5分钟：总结与展望

**核心知识点：**
- QTextEdit富文本操作
- 自定义Widget开发
- 数据库高级查询
- Matplotlib图表集成
- 应用打包（PyInstaller）

---

## 🌟 项目特色

1. **可视化开发**：使用Eric IDE快速设计界面
2. **渐进式教学**：从简单到复杂，层层递进
3. **实用性强**：开发真正能用的日记应用
4. **完整体验**：从编码到打包的完整流程
5. **情感化设计**：学生会真正使用这个应用

---

## 🔗 相关资源

- [PyQt6官方文档](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [Eric IDE官网](https://eric-ide.python-projects.org/)
- [SQLite教程](https://www.sqlite.org/docs.html)
- [Python官方文档](https://docs.python.org/zh-cn/3/)

---

## 📝 作业和扩展

### 基础作业
1. 添加日记标题编辑功能
2. 实现日记删除确认对话框
3. 添加字数实时统计

### 进阶挑战
1. 实现主密码保护功能
2. 添加图片插入功能
3. 实现标签系统
4. 添加云同步功能（可选）
5. 实现主题切换

---

## 👨‍🏫 教师备注

- ✅ 提前测试所有代码
- ✅ 确保Eric IDE正常安装
- ✅ 准备好示例数据库
- ✅ 强调数据安全和隐私保护
- ✅ 鼓励学生个性化定制

---

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

## 📄 许可证

MIT License

---

**祝教学顺利！🎉**
