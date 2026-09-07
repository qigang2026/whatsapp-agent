#!/usr/bin/env python3
"""修复 script-item 的 onclick 转义错误
文件第 1939 行：使用反斜杠转义让 JS 字符串字面量带 onclick 属性，但拼接出的 HTML 不能直接 onclick。
改为 data-copy 属性，配合事件委托。
"""
import re
from pathlib import Path

filepath = Path('/Users/qigangye/Mstar/WhatsApp Agent/收件箱-销售跟进中-PC.html')
html = filepath.read_text(encoding='utf-8')

# 用正则匹配问题行（允许任意空白和转义形式）
# 模式：return '<div class="script-item" onclick="navigator.clipboard && navigator.clipboard.writeText(\\' + s.body.replace(/'/g, '\\\'') + \\')">' +
pat = re.compile(
    r"return '<div class=\"script-item\" onclick=\"navigator\.clipboard && navigator\.clipboard\.writeText\([\\']+ \+ s\.body\.replace\(/'/g, '[\\']+\) \+ [\\']+\)\">' \+"
)
matches = pat.findall(html)
print(f"匹配数: {len(matches)}")

# 替代：使用 data-copy + 事件委托
new_replacement = "return '<div class=\"script-item\" data-copy=\"' + esc(s.body).replace(/\"/g, '&quot;') + '\">' +"
new_html, n = pat.subn(new_replacement, html, count=1)
print(f"替换次数: {n}")

if n > 0:
    filepath.write_text(new_html, encoding='utf-8')
    print("✅ 已更新文件")

# 验证 JS 语法
import subprocess
result = subprocess.run(
    ['node', '-e', '''
const fs = require('fs');
const html = fs.readFileSync('/Users/qigangye/Mstar/WhatsApp Agent/收件箱-销售跟进中-PC.html', 'utf-8');
const re = /<script>([\\s\\S]*?)<\\/script>/g;
const blocks = [];
let m;
while ((m = re.exec(html)) !== null) blocks.push(m[1]);
console.log('script 块数:', blocks.length);
let allOK = true;
blocks.forEach((code, i) => {
  try {
    new Function(code);
  } catch (e) {
    allOK = false;
    console.log('❌ block', i + 1, ':', e.message);
  }
});
if (allOK) console.log('✅ 所有 script 语法 OK');
'''],
    capture_output=True, text=True
)
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)