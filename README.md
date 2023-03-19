[TOC]
# DeskChat
## TODO
- [x] 核心功能

- [x] 流式传输

- [x] 代码块渲染

- [x] 异常捕获

- [ ] status_bar

- [ ] 快捷键绑定
  - [ ] 按钮快捷键

  - [ ] 导航栏快捷键

- [x] 按钮功能完善
  - [x] 发送:不能发送空字符串
  - [ ] 停止:强制停止生成回答
  - [x] 重新生成上条对话
  - [x] 删除上条对话
  - [x] 对summary进程优化
  - [x] 总结对话
  - [x] 总结对话标题并保存
  - [x] 新的对话
  - [x] 加载对话

- [x] 按钮样式（图标）

- [x] 显示tokens

- [x] 计算速度

- [ ] 收集prompt模版

- [ ] 自动减少tokens

- [ ] State Tool Tip

- [ ] 导航栏
  - [ ] 聊天界面
  - [ ] 历史记录管理界面
  - [ ] Prompt界面
  - [ ] Account界面
  


## 重构

### UI美化

使用组件库

+ combo_box:
+ dialog
+ state_tool_tip

### 逻辑优化

- [ ] Chat对话抽象类代替bot和botFrame（对话管理器）

## 打包

### 1 zipimporter has no attribute exec_module 写在main.py最前面

```python
from zipimport import zipimporter
def create_module(self, spec):
    return None

def exec_module(self, module):
    exec(self.get_code(module.__name__), module.__dict__)
zipimporter.create_module = create_module
zipimporter.exec_module = exec_module
```

### 2 main.py 写main函数

## 开发日志

#### 3.18

+ 历史记录管理界面显示方案
  + comboBox
+ 逻辑模块与新UI模块合并
+ 测试
+ 导航栏设置页面设计
+ 菜单图标换成白色
