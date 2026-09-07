#!/usr/bin/env python3
"""
批次 7：所有 WhatsApp Agent HTML 的 Tab 切换条从 5 减为 4
- 删除每个文件中 <a href="AI 跟进概要-PC.html" class="wa-tab ...">...</a> 整段
- index.html 单独处理（不在 wa-tabbar 模式，单独匹配）
"""

import re
from pathlib import Path

ROOT = Path('/Users/qigangye/Mstar/WhatsApp Agent')

# 主 Tab 列表（7 个文件）
TARGETS = [
    'WhatsApp-Agent-PC.html',
    '知识库(cavi).html',
    '线索详情-PC.html',
    'AI 跟进概要-PC.html',
    '收件箱-销售跟进中-PC.html',
    '收件箱-待销售接管-PC.html',
    '收件箱-AI跟进中-PC.html',
    '统一客服收件箱-PC.html',
    '跟进策略-Skill-PC.html',
]

# 匹配模式：完整的 <a> 标签块（含 SVG + span + badge）
# 考虑格式上的差异（badge 可能不存在）
PATTERN = re.compile(
    r'<a href="AI 跟进概要-PC\.html" class="wa-tab[^"]*">.*?</a>\s*\n',
    re.DOTALL
)

results = []
for filename in TARGETS:
    filepath = ROOT / filename
    if not filepath.exists():
        print(f"⚠️  文件不存在：{filename}")
        continue
    html = filepath.read_text(encoding='utf-8')
    matches = PATTERN.findall(html)
    if matches:
        new_html = PATTERN.sub('', html, count=1)
        filepath.write_text(new_html, encoding='utf-8')
        results.append((filename, len(matches), len(html), len(new_html)))
        print(f"✅ {filename}：删除 {len(matches)} 个 AI 跟进概要 Tab")
    else:
        print(f"⚠️  {filename}：未找到匹配")

print(f"\n📊 处理文件数：{len(results)}/{len(TARGETS)}")