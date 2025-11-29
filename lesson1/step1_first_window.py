"""
第一步：创建第一个PyQt6窗口
目标：理解PyQt6的基本结构和窗口创建
"""

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import Qt
import sys


class MyDiaryApp(QMainWindow):
    """我的日记应用 - 第一个窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        # 设置窗口标题
        self.setWindowTitle("MyDiary - 私密日记本")
        
        # 设置窗口位置和大小 (x, y, width, height)
        self.setGeometry(100, 100, 800, 600)
        
        # 添加一个欢迎标签
        label = QLabel("欢迎使用 MyDiary！", self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 设置标签样式
        label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
            }
        """)
        
        # 将标签设置为中心部件
        self.setCentralWidget(label)


def main():
    """主函数"""
    # 创建应用程序对象
    # 每个PyQt应用都需要一个QApplication对象
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = MyDiaryApp()
    
    # 显示窗口
    window.show()
    
    # 进入应用程序的主循环
    # 直到窗口关闭才会退出
    sys.exit(app.exec())


if __name__ == '__main__':
    main()


"""
知识点总结：
1. QApplication: 管理整个应用程序的对象，必须先创建
2. QMainWindow: 主窗口类，提供菜单栏、工具栏、状态栏等功能
3. setWindowTitle(): 设置窗口标题
4. setGeometry(): 设置窗口位置和大小
5. setCentralWidget(): 设置中心部件
6. sys.exit(app.exec()): 启动事件循环，直到窗口关闭

运行方式：
python lesson1/step1_first_window.py

练习题：
1. 修改窗口标题为你自己的名字
2. 调整窗口大小为 900x700
3. 改变欢迎文字的颜色和大小
"""
