# Qt Designer 完整工作流程

## 一、Qt Designer 设计界面

### 1. 启动 Qt Designer
```bash
designer
```

### 2. 创建新窗体
- File → New → Dialog / Main Window / Widget
- 选择合适的模板

### 3. 设计界面
- 从左侧控件库拖拽控件到设计区
- 设置控件属性(右侧属性编辑器)
- **重要**: 给控件起有意义的 objectName (如 `btn_save`, `txt_name`)

### 4. 设置布局
- 选中控件 → 右键 → Layout
- 或使用工具栏布局按钮
- 推荐: QVBoxLayout, QHBoxLayout, QGridLayout

### 5. 保存文件
- File → Save As → `xxx.ui`
- .ui 文件是 XML 格式,记录界面结构

---

## 二、转换为 Python 代码

### 使用 pyuic6 转换
```bash
pyuic6 -o simple_dialog.py simple_dialog.ui
```

**参数说明:**
- `-o`: 输出文件名
- 最后是输入的 .ui 文件

**生成的代码特点:**
- 自动生成 `Ui_XXX` 类
- 包含 `setupUi()` 方法
- 包含 `retranslateUi()` 方法(国际化)
- ⚠️ **不要手动修改此文件!**

---

## 三、启动 Qt Designer

### 方式 1:命令行启动(推荐)

```bash
# macOS (Homebrew 安装)
open /opt/homebrew/bin/designer

# 或直接打开文件
/opt/homebrew/bin/designer simple_dialog.ui &

# 创建别名(可选)
echo 'alias designer="/opt/homebrew/bin/designer"' >> ~/.zshrc
source ~/.zshrc
designer simple_dialog.ui &
```

### 方式 2:从应用程序启动

- 应用程序 → designer.app
- 或双击 `.ui` 文件(需要设置默认打开方式)

---

## 四、创建业务逻辑文件

### 方法 1: 组合方式(推荐)
```python
from PyQt6.QtWidgets import QDialog
from simple_dialog import Ui_Dialog

class MyDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        # 连接信号
        self.ui.btn_ok.clicked.connect(self.on_ok_clicked)
    
    def on_ok_clicked(self):
        print("OK 被点击")
```

### 方法2: 多重继承
```python
from PyQt6.QtWidgets import QDialog
from simple_dialog import Ui_Dialog

class MyDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # 连接信号
        self.btn_ok.clicked.connect(self.on_ok_clicked)
    
    def on_ok_clicked(self):
        print("OK 被点击")
```

---

## 四、运行程序

```python
if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = MyDialog()
    dialog.show()
    sys.exit(app.exec())
```

---

## 五、修改界面后的流程

1. **修改 .ui 文件**: 在 Designer 中修改
2. **重新转换**: `pyuic6 -o simple_dialog.py simple_dialog.ui`
3. **业务逻辑文件不变**: 只要控件名不变,代码无需修改
4. **运行测试**: 查看新界面效果

---

## 六、常见问题

### Q1: 为什么不直接修改 .py 文件?
**A:** 每次重新转换 .ui 都会覆盖 .py 文件,手动修改会丢失。

### Q2: 如何给控件添加事件?
**A:** 在业务逻辑文件中使用 `connect()` 连接信号和槽。

### Q3: Designer 和纯代码哪个好?
**A:** 
- **Designer**: 直观、快速、适合复杂界面
- **纯代码**: 灵活、版本控制友好、适合简单界面

### Q4: 控件命名规范?
**A:** 
- 按钮: `btn_xxx` (如 btn_save, btn_cancel)
- 文本框: `txt_xxx` 或 `edit_xxx`
- 标签: `lbl_xxx`
- 列表: `list_xxx`
- 下拉框: `combo_xxx`

---

## 七、最佳实践

1. ✅ 使用有意义的控件名称
2. ✅ 合理使用布局管理器
3. ✅ 业务逻辑与 UI 分离
4. ✅ .ui 文件纳入版本控制
5. ✅ .py 转换文件可以不纳入版本控制(或添加到 .gitignore)
6. ❌ 不要手动修改 pyuic6 生成的文件
7. ❌ 不要在 Designer 中写代码逻辑

---

## 八、Eric IDE 集成

在 Eric7 中:
1. 双击 .ui 文件自动打开 Designer
2. 右键 .ui → Compile Form 可直接转换
3. 可以在项目中管理 .ui 和 .py 文件的关系
