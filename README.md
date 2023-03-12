[TOC]
# DeskChat
## TODO
- [x] 核心功能
- [x] 流式传输
- [x] 代码块渲染
- [x] 异常捕获
- [ ] 快捷键绑定
- [ ] 按钮功能完善
  - [x] 发送:不能发送空字符串
  - [x] 停止:强制停止生成回答
  - [ ] 保存对话
  - [ ] 
  - [ ] 重新生成上条对话
  - [x] 删除上条对话
  - [x] 对summary进程优化
  - [x] 总结对话
  - [ ] 自动总结对话标题并保存
  - [ ] 新的对话
- [ ] 按钮样式（图标）
- [ ] 显示tokens
- [ ] 计算速度
- [ ] 收集模版

## 打包

### 1 zipimporter has no attribute exec_module

```python
from zipimport import zipimporter

def create_module(self, spec):
    return None
zipimporter.create_module = create_module

def exec_module(self, module):
    exec(self.get_code(module.__name__), module.__dict__)
zipimporter.exec_module = exec_module
```

