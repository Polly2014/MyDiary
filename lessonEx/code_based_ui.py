"""
纯代码方式创建界面 - 与 Designer 方式对比

功能: 创建一个简单的登录对话框
特点: 完全使用代码创建,不依赖 .ui 文件
"""
from PyQt6.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout,
                            QLabel, QLineEdit, QPushButton, QMessageBox,
                            QFormLayout, QGroupBox)
from PyQt6.QtCore import Qt
import sys


class CodeBasedLoginDialog(QDialog):
    """纯代码方式创建的登录对话框"""
    
    def __init__(self):
        super().__init__()
        
        # 设置窗口属性
        self.setWindowTitle("登录 - 纯代码方式")
        self.setFixedSize(350, 200)
        
        # 创建界面
        self.init_ui()
        
        # 连接信号
        self.connect_signals()
    
    def init_ui(self):
        """初始化界面"""
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        
        # 标题标签
        title_label = QLabel("用户登录")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(title_label)
        
        # 创建表单组
        form_group = QGroupBox()
        form_layout = QFormLayout()
        
        # 用户名输入
        self.txt_username = QLineEdit()
        self.txt_username.setPlaceholderText("请输入用户名")
        form_layout.addRow("用户名:", self.txt_username)
        
        # 密码输入
        self.txt_password = QLineEdit()
        self.txt_password.setPlaceholderText("请输入密码")
        self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("密码:", self.txt_password)
        
        form_group.setLayout(form_layout)
        main_layout.addWidget(form_group)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # 登录按钮
        self.btn_login = QPushButton("登录")
        self.btn_login.setMinimumWidth(80)
        self.btn_login.setDefault(True)  # 设置为默认按钮(回车触发)
        button_layout.addWidget(self.btn_login)
        
        # 取消按钮
        self.btn_cancel = QPushButton("取消")
        self.btn_cancel.setMinimumWidth(80)
        button_layout.addWidget(self.btn_cancel)
        
        main_layout.addLayout(button_layout)
        
        # 设置焦点到用户名输入框
        self.txt_username.setFocus()
    
    def connect_signals(self):
        """连接信号和槽"""
        self.btn_login.clicked.connect(self.do_login)
        self.btn_cancel.clicked.connect(self.reject)
        
        # 密码框回车触发登录
        self.txt_password.returnPressed.connect(self.do_login)
    
    def do_login(self):
        """执行登录"""
        username = self.txt_username.text().strip()
        password = self.txt_password.text()
        
        # 验证输入
        if not username:
            QMessageBox.warning(self, "警告", "请输入用户名!")
            self.txt_username.setFocus()
            return
        
        if not password:
            QMessageBox.warning(self, "警告", "请输入密码!")
            self.txt_password.setFocus()
            return
        
        # 简单验证(演示用)
        if username == "admin" and password == "123456":
            QMessageBox.information(self, "成功", f"欢迎, {username}!")
            self.accept()
        else:
            QMessageBox.critical(self, "失败", "用户名或密码错误!")
            self.txt_password.clear()
            self.txt_password.setFocus()


# ============= 代码分析 =============
"""
📊 代码统计:
- 总行数: ~100 行
- UI 创建: ~50 行
- 业务逻辑: ~30 行
- 注释: ~20 行

🎯 优点:
1. 完全控制布局和样式
2. 代码即文档,易于理解
3. 便于动态调整
4. 版本控制友好
5. 不依赖额外工具

⚠️ 缺点:
1. 代码量较大
2. 调整样式需要重新运行
3. 不直观,需要想象最终效果
4. 学习曲线较陡

💡 适用场景:
- 简单对话框
- 需要动态创建的界面
- 参数化的可复用组件
- 代码优先的项目
"""


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    dialog = CodeBasedLoginDialog()
    
    # 显示对话框并等待结果
    if dialog.exec() == QDialog.DialogCode.Accepted:
        print("✅ 登录成功")
    else:
        print("❌ 登录取消")


if __name__ == '__main__':
    main()
