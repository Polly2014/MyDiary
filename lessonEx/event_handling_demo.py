"""
事件处理演示 - 展示 PyQt6 中常用的事件处理方式
"""
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QPushButton, QLineEdit, QTextEdit, QListWidget,
                            QLabel, QComboBox)
from PyQt6.QtCore import Qt
import sys


class EventHandlingDemo(QMainWindow):
    """事件处理演示窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 事件处理演示")
        self.setGeometry(100, 100, 600, 500)
        
        # 创建界面
        self.init_ui()
        
        # 连接信号
        self.connect_signals()
    
    def init_ui(self):
        """初始化界面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 1. 按钮事件
        layout.addWidget(QLabel("1️⃣ 按钮事件:"))
        self.btn_single = QPushButton("单击我")
        layout.addWidget(self.btn_single)
        
        # 2. 文本输入事件
        layout.addWidget(QLabel("\n2️⃣ 文本输入事件:"))
        self.txt_input = QLineEdit()
        self.txt_input.setPlaceholderText("输入文本观察实时变化...")
        layout.addWidget(self.txt_input)
        
        # 3. 下拉框事件
        layout.addWidget(QLabel("\n3️⃣ 下拉框选择事件:"))
        self.combo = QComboBox()
        self.combo.addItems(["选项1", "选项2", "选项3"])
        layout.addWidget(self.combo)
        
        # 4. 列表双击事件
        layout.addWidget(QLabel("\n4️⃣ 列表双击事件:"))
        self.list_widget = QListWidget()
        self.list_widget.addItems([f"列表项 {i+1}" for i in range(5)])
        layout.addWidget(self.list_widget)
        
        # 5. 事件日志
        layout.addWidget(QLabel("\n📝 事件日志:"))
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMaximumHeight(150)
        layout.addWidget(self.log)
    
    def connect_signals(self):
        """连接所有信号"""
        # 按钮单击
        self.btn_single.clicked.connect(self.on_button_clicked)
        
        # 文本改变(实时)
        self.txt_input.textChanged.connect(self.on_text_changed)
        
        # 回车键
        self.txt_input.returnPressed.connect(self.on_return_pressed)
        
        # 下拉框选择改变
        self.combo.currentIndexChanged.connect(self.on_combo_changed)
        self.combo.currentTextChanged.connect(self.on_combo_text_changed)
        
        # 列表项单击
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        
        # 列表项双击
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
    
    # ============= 事件处理函数 =============
    
    def log_event(self, message):
        """记录事件到日志"""
        self.log.append(f"🔔 {message}")
    
    def on_button_clicked(self):
        """按钮单击事件"""
        self.log_event("按钮被单击!")
    
    def on_text_changed(self, text):
        """文本改变事件(实时触发)"""
        self.log_event(f"文本改变: '{text}'")
    
    def on_return_pressed(self):
        """回车键事件"""
        text = self.txt_input.text()
        self.log_event(f"按下回车键,当前文本: '{text}'")
    
    def on_combo_changed(self, index):
        """下拉框索引改变"""
        self.log_event(f"下拉框索引改变: {index}")
    
    def on_combo_text_changed(self, text):
        """下拉框文本改变"""
        self.log_event(f"选择了: '{text}'")
    
    def on_item_clicked(self, item):
        """列表项单击"""
        self.log_event(f"单击列表项: '{item.text()}'")
    
    def on_item_double_clicked(self, item):
        """列表项双击"""
        self.log_event(f"✨ 双击列表项: '{item.text()}'")
    
    # ============= 鼠标和键盘事件(重写方法) =============
    
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.log_event(f"鼠标左键按下位置: ({event.pos().x()}, {event.pos().y()})")
        elif event.button() == Qt.MouseButton.RightButton:
            self.log_event(f"鼠标右键按下位置: ({event.pos().x()}, {event.pos().y()})")
    
    def keyPressEvent(self, event):
        """键盘按下事件"""
        key = event.key()
        if key == Qt.Key.Key_Escape:
            self.log_event("按下 ESC 键")
        elif key == Qt.Key.Key_F1:
            self.log_event("按下 F1 键")
        else:
            self.log_event(f"按下按键: {event.text()}")


# ============= 常用信号汇总 =============
"""
📌 按钮 (QPushButton):
- clicked()                  # 单击
- pressed()                  # 按下
- released()                 # 释放

📌 文本框 (QLineEdit):
- textChanged(str)           # 文本改变
- textEdited(str)            # 用户编辑(不包括程序设置)
- returnPressed()            # 回车键
- editingFinished()          # 编辑完成(失去焦点或回车)

📌 文本编辑器 (QTextEdit):
- textChanged()              # 文本改变
- selectionChanged()         # 选择改变

📌 下拉框 (QComboBox):
- currentIndexChanged(int)   # 索引改变
- currentTextChanged(str)    # 文本改变
- activated(int)             # 用户激活(不包括程序设置)

📌 列表 (QListWidget):
- itemClicked(item)          # 单击项
- itemDoubleClicked(item)    # 双击项
- itemSelectionChanged()     # 选择改变
- currentItemChanged(cur, prev) # 当前项改变

📌 复选框 (QCheckBox):
- stateChanged(int)          # 状态改变
- toggled(bool)              # 切换

📌 单选按钮 (QRadioButton):
- toggled(bool)              # 切换

📌 滑块 (QSlider):
- valueChanged(int)          # 值改变
- sliderPressed()            # 按下
- sliderReleased()           # 释放
- sliderMoved(int)           # 移动

📌 旋转框 (QSpinBox):
- valueChanged(int)          # 值改变
- textChanged(str)           # 文本改变
"""


def main():
    """主函数"""
    app = QApplication(sys.argv)
    window = EventHandlingDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
