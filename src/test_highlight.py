import mdtex2html
import markdown
from markupsafe import Markup,escape
content = """
i'm :
```python
import 123


1



2
print(123)
print(456)\nprint(789)
```
"""
content = Markup(content)
# content = escape(content)
# content = markdown.markdown(content)

print(content)

