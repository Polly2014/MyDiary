# lessonEx - 补充教学示例

本文件夹包含额外的教学演示代码和示例,用于课堂讲解。

## 目录结构

### 1. Qt Designer 工作流程示例
- `designer_workflow.md` - Qt Designer 完整工作流程说明
- `simple_dialog.ui` - 简单对话框 UI 文件
- `simple_dialog.py` - pyuic6 转换后的代码(自动生成)
- `simple_dialog_main.py` - 实际使用示例(添加事件处理)

### 2. 事件处理示例
- `event_handling_demo.py` - 各种控件事件处理演示
- `signal_slot_demo.py` - 信号与槽机制详解

### 3. Designer vs 代码对比
- `code_based_ui.py` - 纯代码创建界面
- `designer_based_ui.py` - Designer 设计界面
- `comparison.md` - 两种方法对比说明

## 使用说明

1. **Qt Designer 文件(.ui)**: 在 Designer 中打开编辑
2. **转换命令**: `pyuic6 -o output.py input.ui`
3. **运行示例**: `python xxx_main.py`

## 教学建议

- 先演示 Designer 基本操作
- 展示 .ui 转 .py 的过程
- 重点讲解事件连接方式
- 对比两种开发方式的优缺点
