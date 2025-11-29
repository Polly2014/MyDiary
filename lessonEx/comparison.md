# Designer vs 纯代码 对比

## 一、同一个界面的两种实现方式

### 方式1: Qt Designer (可视化设计)
**流程:**
1. 在 Designer 中拖拽设计 → `layout_example.ui`
2. 转换: `pyuic6 -o layout_example.py layout_example.ui`
3. 创建业务逻辑: `layout_example_main.py`

**优点:**
- ✅ 可视化,直观
- ✅ 快速设计复杂界面
- ✅ 易于调整布局和样式
- ✅ 非程序员也能设计界面
- ✅ 界面预览所见即所得

**缺点:**
- ❌ 需要额外的 .ui 文件
- ❌ 转换步骤(需要 pyuic6)
- ❌ 动态界面不灵活
- ❌ 版本控制时 XML 难读
- ❌ 依赖 Designer 工具

---

### 方式2: 纯代码 (直接编写)
**流程:**
1. 直接编写 Python 代码创建界面
2. 运行即可

**优点:**
- ✅ 完全控制,灵活性强
- ✅ 易于动态创建界面
- ✅ 代码即文档
- ✅ 版本控制友好
- ✅ 不依赖额外工具

**缺点:**
- ❌ 代码量大
- ❌ 复杂界面难以维护
- ❌ 调整样式需要重新运行
- ❌ 不直观,需要经验
- ❌ 学习曲线陡峭

---

## 二、代码对比示例

### Designer 方式

**1. layout_example.ui (在 Designer 中设计)**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <widget class="QDialog">
  <layout class="QVBoxLayout">
   <item>
    <widget class="QLabel" name="label">
     <property name="text">
      <string>用户名:</string>
     </property>
    </widget>
   </item>
   <item>
    <widget class="QLineEdit" name="txt_username"/>
   </item>
  </layout>
 </widget>
</ui>
```

**2. layout_example.py (pyuic6 自动生成)**
```python
from PyQt6 import QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.label = QtWidgets.QLabel(Dialog)
        self.verticalLayout.addWidget(self.label)
        self.txt_username = QtWidgets.QLineEdit(Dialog)
        self.verticalLayout.addWidget(self.txt_username)
        self.retranslateUi(Dialog)
    
    def retranslateUi(self, Dialog):
        self.label.setText("用户名:")
```

**3. layout_example_main.py (业务逻辑)**
```python
from PyQt6.QtWidgets import QDialog, QApplication
from layout_example import Ui_Dialog

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        # 只需要写业务逻辑
        self.ui.txt_username.textChanged.connect(self.on_text_changed)
    
    def on_text_changed(self, text):
        print(f"输入: {text}")
```

**代码量统计:**
- UI 设计: 0 行(在 Designer 中)
- 业务逻辑: ~10 行
- **总计需要手写: ~10 行**

---

### 纯代码方式

**code_based_ui.py (全部手写)**
```python
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, 
                            QLineEdit, QApplication)

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        # 创建布局
        layout = QVBoxLayout(self)
        
        # 创建标签
        label = QLabel("用户名:")
        layout.addWidget(label)
        
        # 创建文本框
        self.txt_username = QLineEdit()
        layout.addWidget(self.txt_username)
        
        # 连接信号
        self.txt_username.textChanged.connect(self.on_text_changed)
    
    def on_text_changed(self, text):
        print(f"输入: {text}")
```

**代码量统计:**
- 界面 + 业务逻辑: ~20 行
- **总计需要手写: ~20 行**

---

## 三、使用场景建议

### 推荐使用 Designer 的情况:
1. 🎨 **复杂界面**: 多个布局嵌套,控件众多
2. 👥 **团队协作**: UI 设计师和程序员分工
3. 🔄 **频繁调整**: 界面需要经常修改样式
4. 📚 **教学演示**: 让学生快速看到效果
5. 🚀 **快速原型**: 需要快速验证想法

**例如:** 主窗口、设置对话框、数据录入表单

---

### 推荐使用纯代码的情况:
1. 🔀 **动态界面**: 根据数据动态生成控件
2. 🎯 **简单窗口**: 几个控件,布局简单
3. 📦 **可复用组件**: 需要参数化的控件
4. 🐛 **精确控制**: 需要完全控制创建过程
5. 📝 **代码优先**: 团队更习惯纯代码开发

**例如:** 消息框、简单输入框、动态列表

---

## 四、混合使用策略(最佳实践)

### 推荐方案:
```
主界面 → Designer 设计
  ├─ 工具栏 → 代码创建
  ├─ 菜单栏 → 代码创建
  ├─ 主内容区 → Designer 设计
  └─ 动态部分 → 代码创建
```

### 示例:
```python
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 使用 Designer 设计的主界面
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # 用代码创建动态工具栏
        self.create_toolbar()
        
        # 用代码创建菜单
        self.create_menus()
    
    def create_toolbar(self):
        """代码创建工具栏(灵活)"""
        toolbar = self.addToolBar("工具")
        # 动态添加工具按钮...
    
    def create_menus(self):
        """代码创建菜单(灵活)"""
        menu = self.menuBar().addMenu("文件")
        # 动态添加菜单项...
```

---

## 五、对比总结表

| 对比项 | Designer | 纯代码 |
|--------|----------|--------|
| **学习曲线** | 低,拖拽即可 | 中等,需要 API 知识 |
| **开发速度** | 快(复杂界面) | 慢(复杂界面) |
| **代码可读性** | 差(XML) | 好(Python) |
| **灵活性** | 中等 | 高 |
| **维护性** | 中等 | 高 |
| **版本控制** | 差(XML) | 好 |
| **动态创建** | 困难 | 容易 |
| **调试便利性** | 中等 | 好 |
| **团队协作** | 好(分工明确) | 中等 |
| **依赖工具** | 需要 Designer | 只需要编辑器 |

---

## 六、教学建议

### Lesson 1: Designer 基础
- 介绍 Designer 界面
- 演示基本控件使用
- 讲解 .ui → .py 转换
- 强调不要修改生成的 .py

### Lesson 2: 纯代码实现
- 讲解布局管理器
- 演示同样界面的代码实现
- 对比两种方式

### Lesson 3: 混合使用
- 演示实际项目中的最佳实践
- 讲解何时用哪种方式
- 动态界面示例

---

## 七、常见问题

### Q: 初学者应该用哪种方式?
**A:** 建议先学 Designer,快速建立信心,再学代码方式理解原理。

### Q: 专业开发用哪种?
**A:** 混合使用 - 主界面用 Designer,动态部分用代码。

### Q: Designer 的局限性?
**A:** 
1. 无法实现复杂逻辑
2. 动态界面支持差
3. 自定义控件需要代码

### Q: 如何从 Designer 过渡到纯代码?
**A:** 
1. 查看 pyuic6 生成的代码
2. 理解布局管理器工作原理
3. 尝试手写简单界面
4. 逐步增加复杂度
