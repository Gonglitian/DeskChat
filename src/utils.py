def zipimporter_fix():
    from zipimport import zipimporter

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        exec(self.get_code(module.__name__), module.__dict__)

    zipimporter.create_module = create_module
    zipimporter.exec_module = exec_module


zipimporter_fix()

import tiktoken
import mdtex2html
from markdown import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import re
import inspect

LOGFLAG = True


def log(msg: str):
    if LOGFLAG:
        frame = inspect.stack()[1]
        print(f"[log]{msg}  at: File {inspect.getfile(frame[0])}, line {frame[2]}")


def count_token(Sentence):
    encoding = tiktoken.get_encoding("cl100k_base")
    input_str = f"role: {Sentence.role}, content: {Sentence.content}"
    length = len(encoding.encode(input_str))
    return length


def parse_text(text):
    in_code_block = False
    new_lines = []
    for line in text.split("\n"):
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
        if in_code_block:
            if line.strip() != "":
                new_lines.append(line)
        else:
            new_lines.append(line)
    if in_code_block:
        new_lines.append("```")
    text = "\n".join(new_lines)
    return text


def markdown_to_html_with_syntax_highlight(md_str):
    def replacer(match):
        lang = match.group(1) or "text"
        code = match.group(2)
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except ValueError:
            lexer = get_lexer_by_name("text", stripall=True)

        formatter = HtmlFormatter()
        highlighted_code = highlight(code, lexer, formatter)

        return f'<pre><code class="{lang}">{highlighted_code}</code></pre>'

    code_block_pattern = r"```(\w+)?\n([\s\S]+?)\n```"
    md_str = re.sub(code_block_pattern, replacer, md_str, flags=re.MULTILINE)

    html_str = markdown(md_str)
    return html_str


def normalize_markdown(md_text: str) -> str:
    lines = md_text.split("\n")
    normalized_lines = []
    inside_list = False

    for i, line in enumerate(lines):
        if re.match(r"^(\d+\.|-|\*|\+)\s", line.strip()):
            if not inside_list and i > 0 and lines[i - 1].strip() != "":
                normalized_lines.append("")
            inside_list = True
            normalized_lines.append(line)
        elif inside_list and line.strip() == "":
            if i < len(lines) - 1 and not re.match(
                    r"^(\d+\.|-|\*|\+)\s", lines[i + 1].strip()
            ):
                normalized_lines.append(line)
            continue
        else:
            inside_list = False
            normalized_lines.append(line)

    return "\n".join(normalized_lines)


def convert_mdtext(md_text):
    code_block_pattern = re.compile(r"```(.*?)(?:```|$)", re.DOTALL)
    inline_code_pattern = re.compile(r"`(.*?)`", re.DOTALL)
    code_blocks = code_block_pattern.findall(md_text)
    non_code_parts = code_block_pattern.split(md_text)[::2]

    result = []
    for non_code, code in zip(non_code_parts, code_blocks + [""]):
        if non_code.strip():
            non_code = normalize_markdown(non_code)
            if inline_code_pattern.search(non_code):
                result.append(markdown(non_code, extensions=["tables"]))
            else:
                result.append(mdtex2html.convert(non_code, extensions=["tables"]))
        if code.strip():
            # _, code = detect_language(code)  # 暂时去除代码高亮功能，因为在大段代码的情况下会出现问题
            # code = code.replace("\n\n", "\n") # 暂时去除代码中的空行，因为在大段代码的情况下会出现问题
            code = f"\n```{code}\n\n```"
            code = markdown_to_html_with_syntax_highlight(code)
            result.append(code)
    result = "".join(result)
    return result


def detect_language(code):
    if code.startswith("\n"):
        first_line = ""
    else:
        first_line = code.strip().split("\n", 1)[0]
    language = first_line.lower() if first_line else ""
    code_without_language = code[len(first_line):].lstrip() if first_line else code
    return language, code_without_language


def processTime(current_time):
    # print(str(current_time))
    current_time = str(current_time)[6:19].replace(":", "_").replace("-", "_").replace(" ", "_")
    return current_time
