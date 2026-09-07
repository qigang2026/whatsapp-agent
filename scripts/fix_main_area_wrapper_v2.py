#!/usr/bin/env python3
"""修复 main-area 结构错位：把 <div class="main-area"> 移到 <nav class="wa-tabbar"> 之前"""

from pathlib import Path

filepath = Path('/Users/qigangye/Mstar/WhatsApp Agent/收件箱-销售跟进中-PC.html')
html = filepath.read_text(encoding='utf-8')

# 用字符串切片定位
# 1. 找到 </aside>
idx_aside_close = html.find('</aside>')
# 2. 找到 main-area 的开始位置
idx_main_area = html.find('<div class="main-area">', idx_aside_close)
# 3. 找到 nav 的开始位置（应该在 main-area 之前）
idx_nav = html.find('<nav class="wa-tabbar">', idx_aside_close)

print(f"aside close: {idx_aside_close}")
print(f"main-area: {idx_main_area}")
print(f"nav: {idx_nav}")

if idx_aside_close == -1 or idx_main_area == -1 or idx_nav == -1:
    print("⚠️  未找到关键标签")
    raise SystemExit(1)

if idx_main_area < idx_nav:
    print("✅ 结构已经正确")
    raise SystemExit(0)

# 当前错误顺序：aside_close ... nav ... </nav> ... <div class="main-area">
# 目标顺序：aside_close ... <div class="main-area"> ... nav ... </nav> ...

# 切片：
part1 = html[:idx_main_area]                       # 到 main-area 开始前
part2 = html[idx_main_area:idx_nav]                # main-area 开始标签 + 之间的内容 + nav 前
part3 = html[idx_nav:]                              # nav 一直到文件末尾

# 我们要把 <div class="main-area"> 移到 nav 之前
# 现在 part2 以 <div class="main-area"> 开头
# 但 part2 也包含了从 main-area 到 nav 之间的所有内容（这部分应该在 main-area 内、nav 外）
# 实际上 part2 的内容是 main-area 开头 + 一些内容
# 我们需要：保留 part1 + <div class="main-area"> + part3

# 等等，分析下：
# part1: html[:idx_main_area] —— aside_close ... 紧贴在 <div class="main-area"> 之前
# part2: html[idx_main_area:idx_nav] —— <div class="main-area"> ... （包括开标签和 nav 之间的内容）
# part3: html[idx_nav:] —— <nav class="wa-tabbar"> ... </body>

# 当前文件渲染: aside ... <nav>...</nav> <div class="main-area">... </div>
# 修复为: aside ... <div class="main-area"><nav>...</nav>...</div>

# 但是 part2 包括从 main-area 开始到 nav 之前的内容 —— 但当前 main-area 是在 nav 之后啊！
# 所以 part2 实际上是 nav 前的内容（紧接 aside 的内容） + <div class="main-area"> 字符串

# 实际更简单的方法：找到 <div class="main-area"> 字符串，把它移到 nav 之前
# part1: html[:idx_main_area] —— 包含 aside_close 和之间的注释
# part1 的最后是 "<div class=\"main-area\">" 之前的部分

# 修复方法：删除现有的 <div class="main-area">，然后在 nav 之前插入新的
# 但这样 main-area 的内容（part3 末尾的 </div></div></div>）会和 nav 错位
# 让我直接重写：以 </aside> 为锚点，到 main-area 结束（即末尾的 </div>）

# 找到 <div class="main-area"> 之后第一个匹配的 </div>
# 但因为有嵌套，我们得用平衡匹配
import re

# 找到 main-area 开始位置
main_area_start = idx_main_area

# 找到从 main-area 开始到下一个 </aside> 之前所有的内容（即 main-area 块的整个内容）
# 简化：在 main-area 开始后用平衡 div 匹配
def find_matching_div(text, start_pos):
    """从 start_pos 之后找匹配的 </div>"""
    depth = 1
    pos = start_pos + 1
    while pos < len(text) and depth > 0:
        next_open = text.find('<div', pos)
        next_close = text.find('</div>', pos)
        if next_close == -1:
            return -1
        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + 4
        else:
            depth -= 1
            pos = next_close + 6
    return pos - 6 if depth == 0 else -1

# 实际上更简单：main-area 块的结束就是文件 layout 闭合前
# 让我看 main-area 后面跟着什么
idx_after_main_area = html.find('\n  <div class="main-cols">', idx_main_area)
# main-area 在 line 1579 打开，里面先有 top-tabs nav
# 让我看实际层级
# 跳过简单方法：直接看哪里结束
# 找 </div><!-- /.main-area -->
idx_main_area_end = html.find('</div><!-- /.main-area -->')
print(f"main-area 结束: {idx_main_area_end}")

# 重写策略：
# 取 idx_aside_close 之后到 idx_main_area 之前的内容（这是 aside_close 到 main-area 之间，应该只有 nav + 注释）
between_aside_and_main = html[idx_aside_close:idx_main_area]
# 这个 between 包括：</aside>\n\n  <!-- 主区域注释 -->\n\n    <!-- Tab 注释 -->\n    <nav class="wa-tabbar">...</nav>\n\n
# 取 idx_main_area 到 idx_main_area_end 之后（包括 main-area 块到结束注释）
main_area_block = html[idx_main_area:idx_main_area_end + len('</div><!-- /.main-area -->')]

# 重组：
# html[:idx_aside_close] + </aside> + 注释 + <div class="main-area"> + 注释 + <nav>...</nav> + 其他 + </div>
# 但当前 main_area_block 已经是完整 main-area
# 我们需要在 main-area 块开头插入 nav + 注释

# 从 between_aside_and_main 提取 <nav class="wa-tabbar">...</nav>
import re
nav_pattern = re.compile(r'(<nav class="wa-tabbar">[\s\S]*?</nav>)', re.MULTILINE)
nav_match = nav_pattern.search(between_aside_and_main)
if not nav_match:
    print("⚠️  未找到 nav 块")
    raise SystemExit(1)

nav_text = nav_match.group(1)

# main-area 块开头通常是 <div class="main-area">\n\n    <!-- 顶级工作流 Tab -->
# 我们要在 main-area 之后插入 nav_text
# 但当前 main-area 块的第一个子元素是 <nav class="top-tabs">（会话状态 Tab）
# nav_text 应该放在 <nav class="top-tabs"> 之前

# main-area 内部第一个子元素是：
# <div class="main-area">

#     <!-- ========== 顶级工作流 Tab（4 个独立 HTML 之间互链） ========== -->
#     <nav class="top-tabs">
# 我们需要在 <div class="main-area"> 之后插入 nav_text，在 <nav class="top-tabs"> 之前

# 先看 main-area 块开头
ma_first_part_end = main_area_block.find('<nav class="top-tabs">')
if ma_first_part_end == -1:
    print("⚠️  未找到 top-tabs")
    raise SystemExit(1)

# 重组：
# 1. aside 闭合到 main-area 之间：去掉 nav
before_main_no_nav = between_aside_and_main.replace(nav_text, '')
# 2. main-area 开头到 top-tabs：保持
ma_start = main_area_block[:main_area_block.find('<nav class="top-tabs">')]
# 3. main-area top-tabs 之后：保持
ma_rest = main_area_block[main_area_block.find('<nav class="top-tabs">'):]

new_html = (
    html[:idx_aside_close] +
    before_main_no_nav +
    '<div class="main-area">\n\n' +
    ma_start.split('\n', 1)[1] if ma_start.startswith('<div class="main-area">\n') else ma_start[len('<div class="main-area">'):] +
    '\n    <!-- ========== 5 Tab 切换条（批次 5 · 统一全页面） ========== -->\n' +
    nav_text +
    '\n\n' +
    ma_rest +
    html[idx_main_area_end + len('</div><!-- /.main-area -->'):]
)

filepath.write_text(new_html, encoding='utf-8')

print(f"\n✅ 已重组")
print(f"   原文件: {len(html)} chars")
print(f"   新文件: {len(new_html)} chars")
"