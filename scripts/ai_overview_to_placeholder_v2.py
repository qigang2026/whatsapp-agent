#!/usr/bin/env python3
"""
批次 6 步骤 3（修正）：把 AI 跟进概要-PC.html 转为占位跳转页
- 保留侧栏 + topbar + 4 Tab 切换条（"工作台" Tab active）
- <section class="content"> 改为简洁占位
- 删除 ECharts CDN + 4 个图表初始化
"""

import re
from pathlib import Path

ROOT = Path('/Users/qigangye/Mstar/WhatsApp Agent')
TARGET = ROOT / 'AI 跟进概要-PC.html'

html = TARGET.read_text(encoding='utf-8')

# 1. 修改 <title>
html = re.sub(
    r'<title>[^<]+</title>',
    '<title>AI 跟进概要 · 已整合到工作台 · AutoCava CRM</title>',
    html
)

# 2. 修改 topbar breadcrumb
html = re.sub(
    r'<span class="current">AI 跟进概要</span>',
    '<span class="current">AI 跟进概要（已整合）</span>',
    html
)

# 3. 工作台 Tab 加 active
html = re.sub(
    r'(<a href="WhatsApp-Agent-PC\.html" class="wa-tab)(?: active)?(")',
    r'\1 active\2',
    html,
    count=1
)

# 4. 替换 <section class="content"> ... </section>（保留 main）
# 找 <section class="content"> 到 </section>
content_match = re.search(r'<section class="content">', html)
section_end_match = re.search(r'</section>', html)

if not content_match or not section_end_match:
    print("⚠️  未找到 content section")
    raise SystemExit(1)

placeholder = """<section class="content">
      <div class="empty-placeholder">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M3 3v18h18"/>
          <path d="M7 16l4-4 4 4 5-5"/>
        </svg>
        <h2>AI 跟进概要已整合到工作台首页</h2>
        <p>所有 KPI / 趋势图 / 漏斗 / SLA / 车型热度 / 异常会话数据均已迁移到「工作台」Tab 下，无需再访问此页。</p>
        <div class="empty-actions">
          <a href="WhatsApp-Agent-PC.html" class="btn-primary">前往工作台 →</a>
          <span class="empty-tip">此页保留为兼容入口，Tab 切换条已更新</span>
        </div>
      </div>
    </section>"""

# 替换原 content section
content_start = content_match.start()
content_end = section_end_match.end()

new_html = html[:content_start] + placeholder + html[content_end:]

# 5. 删除 ECharts CDN
new_html = re.sub(
    r'<script src="https://cdn\.jsdelivr\.net/npm/echarts@[^"]+"></script>\s*\n',
    '',
    new_html
)

# 6. 删除 ECharts 初始化 JS（trendChart, funnelChart, slaChart, carsChart 的 setOption 调用）
echarts_block_pattern = re.compile(
    r'const trendChart.*?carsChart\.setOption\(\{[\s\S]*?\}\);\s*',
    re.DOTALL
)
new_html = echarts_block_pattern.sub('', new_html)

# 7. 注入占位样式（如果有的话）
# 注入到 <style> 内
empty_css = """
  /* 占位页样式 */
  .empty-placeholder {
    max-width: 560px;
    margin: 80px auto;
    text-align: center;
    padding: 60px 40px;
    background: #fff;
    border: 1px solid var(--border-extra-light);
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  }
  .empty-placeholder svg {
    width: 64px;
    height: 64px;
    color: var(--primary);
    margin-bottom: 20px;
    opacity: 0.7;
  }
  .empty-placeholder h2 {
    font-size: 20px;
    color: var(--text-main);
    margin-bottom: 12px;
    font-weight: 600;
  }
  .empty-placeholder p {
    font-size: 14px;
    color: var(--text-secondary);
    line-height: 1.7;
    margin-bottom: 24px;
  }
  .empty-actions {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    flex-wrap: wrap;
  }
  .btn-primary {
    background: var(--primary);
    color: #fff;
    padding: 10px 24px;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 500;
    text-decoration: none;
    transition: background 0.15s;
  }
  .btn-primary:hover {
    background: var(--primary-hover);
  }
  .empty-tip {
    font-size: 12px;
    color: var(--text-placeholder);
  }
"""

if 'empty-placeholder' not in new_html or '.empty-placeholder {' not in new_html:
    new_html = new_html.replace('</style>', empty_css + '\n</style>', 1)

TARGET.write_text(new_html, encoding='utf-8')

print(f"✅ 已替换为占位页")
print(f"原文件：{len(html)} chars")
print(f"新文件：{len(new_html)} chars")

# 验证
if 'empty-placeholder' in new_html:
    print("✅ 占位元素存在")
if '前往工作台' in new_html:
    print("✅ 跳转按钮存在")
if 'echarts.min.js' not in new_html:
    print("✅ ECharts CDN 已删除")
if 'setOption' not in new_html:
    print("✅ ECharts 初始化代码已删除")
if 'wa-tab active' in new_html:
    print("✅ Tab active 状态已切换到工作台")