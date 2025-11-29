"""
简单对话框主程序 - 演示如何使用 Designer 设计的界面

工作流程:
1. simple_dialog.ui - 在 Designer 中设计
2. simple_dialog.py - 使用 pyuic6 转换生成(不要手动修改!)
3. simple_dialog_main.py - 本文件,添加业务逻辑和事件处理
"""
from PyQt6.QtWidgets import QApplication, QDialog
import sys

# 导入 pyuic6 转换生成的 UI 类
from simple_dialog import Ui_Dialog


class SimpleDialog(QDialog):
    """简单对话框 - 演示信息输入和显示"""
    
    def __init__(self):
        super().__init__()
        
        # 创建 UI 对象并设置到当前窗口
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        # 连接信号和槽
        self.connect_signals()
    
    def connect_signals(self):
        """连接控件的信号到处理函数"""
        # 显示信息按钮
        self.ui.btn_show.clicked.connect(self.show_info)
        
        # 清空按钮
        self.ui.btn_clear.clicked.connect(self.clear_info)
        
        # 关闭按钮
        self.ui.btn_close.clicked.connect(self.close)
        
        # 姓名输入框回车键
        self.ui.txt_name.returnPressed.connect(self.show_info)
    
    def show_info(self):
        """显示用户输入的信息"""
        # 获取输入的值
        name = self.ui.txt_name.text()
        age = self.ui.spin_age.value()
        gender = self.ui.combo_gender.currentText()
        
        # 验证输入
        if not name.strip():
            self.ui.txt_info.setPlainText("⚠️ 请输入姓名!")
            return
        
        # 格式化显示
        info = f"""
📋 用户信息
{'='*30}
姓名: {name}
年龄: {age} 岁
性别: {gender}
{'='*30}
        """
        
        self.ui.txt_info.setPlainText(info.strip())
    
    def clear_info(self):
        """清空所有输入"""
        self.ui.txt_name.clear()
        self.ui.spin_age.setValue(20)
        self.ui.combo_gender.setCurrentIndex(0)
        self.ui.txt_info.clear()
        
        # 焦点回到姓名输入框
        self.ui.txt_name.setFocus()


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 创建并显示对话框
    dialog = SimpleDialog()
    dialog.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
