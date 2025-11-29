"""
第四步：PDF导出功能
目标：将日记导出为PDF文件
"""

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QListWidget, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from lesson1.database import DatabaseManager


class ExportApp(QMainWindow):
    """导出功能应用"""
    
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager("mydiary_v2.db")
        self.init_ui()
        self.load_diary_list()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("MyDiary - 导出PDF")
        self.setGeometry(100, 100, 700, 500)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # 说明
        info_label = QLabel("📤 选择要导出的日记，点击导出按钮生成PDF文件")
        info_label.setStyleSheet("font-size: 14px; padding: 10px; background-color: #ecf0f1; border-radius: 5px;")
        layout.addWidget(info_label)
        
        # 日记列表
        list_label = QLabel("📚 日记列表:")
        list_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(list_label)
        
        self.diary_list = QListWidget()
        self.diary_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        layout.addWidget(self.diary_list)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        select_all_btn = QPushButton("✅ 全选")
        select_all_btn.clicked.connect(self.select_all)
        
        clear_btn = QPushButton("❌ 取消全选")
        clear_btn.clicked.connect(self.clear_selection)
        
        export_btn = QPushButton("📄 导出为PDF")
        export_btn.clicked.connect(self.export_to_pdf)
        
        button_layout.addWidget(select_all_btn)
        button_layout.addWidget(clear_btn)
        button_layout.addWidget(export_btn)
        
        layout.addLayout(button_layout)
        
        central_widget.setLayout(layout)
        
        # 设置样式
        self.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                min-height: 35px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QListWidget {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #ecf0f1;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
    
    def load_diary_list(self):
        """加载日记列表"""
        self.diary_list.clear()
        diaries = self.db.get_all_diaries()
        
        for diary in diaries:
            item_text = f"[{diary['created_date']}] {diary['title']}"
            self.diary_list.addItem(item_text)
            item = self.diary_list.item(self.diary_list.count() - 1)
            item.setData(Qt.ItemDataRole.UserRole, diary['id'])
    
    def select_all(self):
        """全选"""
        for i in range(self.diary_list.count()):
            self.diary_list.item(i).setSelected(True)
    
    def clear_selection(self):
        """取消全选"""
        self.diary_list.clearSelection()
    
    def export_to_pdf(self):
        """导出为PDF"""
        selected_items = self.diary_list.selectedItems()
        
        if not selected_items:
            QMessageBox.warning(self, "警告", "请至少选择一篇日记！")
            return
        
        # 选择保存路径
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "保存PDF文件",
            f"我的日记_{len(selected_items)}篇.pdf",
            "PDF文件 (*.pdf)"
        )
        
        if not filename:
            return
        
        try:
            # 获取选中的日记
            diary_ids = [item.data(Qt.ItemDataRole.UserRole) for item in selected_items]
            diaries = [self.db.get_diary(diary_id) for diary_id in diary_ids]
            
            # 生成PDF
            self.create_pdf(filename, diaries)
            
            QMessageBox.information(
                self,
                "成功",
                f"已成功导出 {len(diaries)} 篇日记到:\n{filename}"
            )
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导出失败: {str(e)}")
    
    def create_pdf(self, filename, diaries):
        """创建PDF文件"""
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4
        
        # 注册中文字体（如果系统有）
        try:
            # Mac
            pdfmetrics.registerFont(TTFont('SimSun', '/System/Library/Fonts/STHeiti Medium.ttc'))
        except:
            try:
                # Windows
                pdfmetrics.registerFont(TTFont('SimSun', 'C:/Windows/Fonts/simhei.ttf'))
            except:
                # 使用默认字体
                print("未找到中文字体，使用默认字体")
        
        y = height - 50
        
        # 标题
        c.setFont('SimSun', 20)
        c.drawCentredString(width / 2, y, "我的日记集")
        y -= 40
        
        # 遍历日记
        for i, diary in enumerate(diaries, 1):
            # 检查是否需要新页
            if y < 100:
                c.showPage()
                y = height - 50
            
            # 日记标题
            c.setFont('SimSun', 16)
            c.drawString(50, y, f"{i}. {diary['title']}")
            y -= 25
            
            # 日期和心情
            c.setFont('SimSun', 10)
            date_text = f"日期: {diary['created_date']}"
            mood_dict = {'happy': '开心', 'sad': '难过', 'neutral': '平静', 
                         'angry': '愤怒', 'anxious': '焦虑', 'tired': '疲惫'}
            mood_text = f"心情: {mood_dict.get(diary.get('mood', 'neutral'), '平静')}"
            c.drawString(50, y, f"{date_text}  |  {mood_text}")
            y -= 20
            
            # 分隔线
            c.line(50, y, width - 50, y)
            y -= 20
            
            # 内容（去除HTML标签）
            content = diary['content']
            # 简单的HTML标签去除
            import re
            content = re.sub('<[^>]+>', '', content)
            
            # 分段处理
            c.setFont('SimSun', 12)
            max_width = width - 100
            lines = []
            
            for paragraph in content.split('\n'):
                if not paragraph.strip():
                    continue
                
                # 简单的文字换行
                words = paragraph
                current_line = ""
                for char in words:
                    if c.stringWidth(current_line + char, 'SimSun', 12) < max_width:
                        current_line += char
                    else:
                        lines.append(current_line)
                        current_line = char
                if current_line:
                    lines.append(current_line)
            
            # 绘制文本
            for line in lines[:20]:  # 限制每篇日记的行数
                if y < 50:
                    c.showPage()
                    y = height - 50
                c.drawString(50, y, line)
                y -= 18
            
            y -= 30  # 日记之间的间距
        
        c.save()


def main():
    """主函数"""
    app = QApplication(sys.argv)
    window = ExportApp()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()


"""
知识点总结：
1. QFileDialog文件对话框:
   - getSaveFileName(): 保存文件对话框
   - 返回文件路径和过滤器

2. QListWidget多选:
   - setSelectionMode(): 设置选择模式
   - MultiSelection: 多选模式
   - selectedItems(): 获取选中项

3. ReportLab PDF生成:
   - Canvas: PDF画布
   - setFont(): 设置字体
   - drawString(): 绘制文本
   - showPage(): 新建页面

4. 中文字体处理:
   - registerFont(): 注册字体
   - TTFont: TrueType字体
   - 处理不同操作系统的字体路径

5. 文本处理:
   - 去除HTML标签
   - 文本换行
   - 页面分页

运行方式：
python lesson2/step4_export.py

练习题：
1. 添加PDF水印
2. 支持导出为Word文档
3. 添加更多PDF格式选项
4. 支持图片导出
"""
